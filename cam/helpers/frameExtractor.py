import cv2.cv2 as cv
import numpy as np

# Create a VideoCapture object
cap = cv.VideoCapture('../videos/flurVideo2.mp4')

# Check if camera opened successfully
if not cap.isOpened():
    print("Unable to read camera feed")

# Default resolutions of the frame are obtained.The default resolutions are system dependent.
# We convert the resolutions from float to integer.
frame_width = int(cap.get(3))
frame_height = int(cap.get(4))

# Define the codec and create VideoWriter object.The output is stored in 'outpy.avi' file.
out = cv.VideoWriter('../videos/cuttedFlur2.mp4', cv.VideoWriter_fourcc('m', 'p', '4', 'v'), 10,
                     (frame_width, frame_height))
frameCount = 0
while True:
    ret, frame = cap.read()

    if ret:

        if frameCount % 15 == 0:
            # Write the frame into the file 'output.avi'
            out.write(frame)

            # Display the resulting frame
            cv.imshow('frame', frame)
            print(f"saved frame {frame_width}")

        frameCount += 1
        print(f"frameCount: {frameCount}")

        # Press Q on keyboard to stop recording
        if cv.waitKey(1) & 0xFF == ord('q'):
            break

    # Break the loop
    else:
        break

    # When everything done, release the video capture and video write objects
cap.release()
out.release()

# Closes all the frames
cv.destroyAllWindows()
