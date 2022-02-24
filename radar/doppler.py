# ===========================================================================
# Copyright (C) 2021 Infineon Technologies AG
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice,
#    this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in the
#    documentation and/or other materials provided with the distribution.
# 3. Neither the name of the copyright holder nor the names of its
#    contributors may be used to endorse or promote products derived from
#    this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.
# ===========================================================================

import os
import argparse

import numpy as np
from scipy import signal
from scipy.interpolate import interp1d

from ifxRadarSDK import *
from fft_spectrum import *
from publisher import Publisher
from util import dump_matrix

# -------------------------------------------------
# Computation
# -------------------------------------------------
class DopplerAlgo:
    # Doppler algorithm for raw data

    def __init__(self, cfg, num_ant):
        # Initiate common values for all computation
        # cfg:      dictionary with configuration for device used by set_config() as input
        # num_ant:  number of available antennas

        self._numchirps = cfg["num_chirps_per_frame"]
        chirpsamples = cfg["num_samples_per_chirp"]

        # compute Blackman-Harris Window matrix over chirp samples(range)
        self._range_window = signal.blackmanharris(chirpsamples).reshape(
            1, chirpsamples
        )

        # compute Blackman-Harris Window matrix over number of chirps(velocity)
        self._doppler_window = signal.blackmanharris(self._numchirps).reshape(
            1, self._numchirps
        )

        self._moving_avg_alpha = 0.8
        self._mti_alpha = 1.0
        # initialize doppler averages for all antennae
        self._dopp_avg = np.zeros(
            (chirpsamples, self._numchirps * 2, num_ant), dtype=complex
        )

    def compute_doppler_map(self, data, i_ant):
        # Computation of doppler map for drawing
        # with middle value with speed of 0 and distance on column
        # number
        # data:     single chirp raw data for single antenna
        # i_ant:    antenna number that data is related to

        # Step 1 -  calculate fft spectrum for the frame
        fft1d = fft_spectrum(data, self._range_window)

        # prepare for doppler FFT

        # Transpose
        # Distance is now indicated on y axis
        fft1d = np.transpose(fft1d)

        # Step 2 - Windowing the Data in doppler
        fft1d = np.multiply(fft1d, self._doppler_window)

        zp2 = np.pad(fft1d, ((0, 0), (0, self._numchirps)), "constant")
        fft2d = np.fft.fft(zp2) / self._numchirps

        # MTI processing
        # needed to remove static objects
        # step 1 moving average
        # multiply history by (mti_alpha)
        fft2d_mti = fft2d - (self._dopp_avg[:, :, i_ant] * self._mti_alpha)

        # update moving average
        self._dopp_avg[:, :, i_ant] = (fft2d * self._moving_avg_alpha) + (
            self._dopp_avg[:, :, i_ant] * (1 - self._moving_avg_alpha)
        )

        # re-arrange fft result for zero speed at centre
        dopplerfft = np.fft.fftshift(fft2d_mti, (1,))

        return 20 * np.log10(abs(np.fliplr(dopplerfft)))


# -------------------------------------------------
# Main logic
# -------------------------------------------------
def main():
    name = os.getenv("RADAR_NAME", "radar")
    broker = os.getenv("RADAR_BROKER_HOST", "broker.mqttdashboard.com")
    port = os.getenv("RADAR_BROKER_PORT", 1883)
    publisher = Publisher(name, broker, port)

    with Device() as device:
        # activate all available antennas
        num_rx_antennas = device.get_device_information()["num_rx_antennas"]
        rx_mask = (1 << num_rx_antennas) - 1

        metric = {
            "sample_rate_Hz": 1_000_000,
            "range_resolution_m": 0.15,
            "max_range_m": 4.8,
            "max_speed_m_s": 2.45,
            "speed_resolution_m_s": 0.2,
            "frame_repetition_time_s": 1 / 5,
            "center_frequency_Hz": 60_750_000_000,
            "rx_mask": rx_mask,
            "tx_mask": 1,
            "tx_power_level": 31,
            "if_gain_dB": 33,
        }

        cfg = device.translate_metrics_to_config(**metric)

        device.set_config(**cfg)

        frame = device.create_frame_from_device_handle()
        num_ant = frame.get_num_rx()

        firmware_information = device.get_firmware_information()
        device_information = device.get_device_information()

        doppler = DopplerAlgo(cfg, num_ant)
        inter = interp1d([0, 64], [metric["max_speed_m_s"], -metric["max_speed_m_s"]])

        while True:
            device.get_next_frame(frame)

            mean_velocities = []

            for i_ant in range(0, num_ant):  # For each antenna
                mat = frame.get_mat_from_antenna(i_ant)
                doppler_map = doppler.compute_doppler_map(mat, i_ant)

                values = np.where(doppler_map > -70)

                mean_velocities.extend([inter(x) for x in values[1]])

            mean_velocity = np.array(mean_velocities).flatten().mean()
            temperature = device.get_temperature()

            print(f"Mean Velocity: {mean_velocity:>2.2f} m/s")
            publisher.createAndSendMessage(
                mean_velocity, temperature, firmware_information, device_information
            )


if __name__ == "__main__":
    main()
