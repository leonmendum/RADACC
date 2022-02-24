import {
  Box,
  Button,
  Container,
  Grid,
  makeStyles,
  Paper,
  TextField,
} from '@material-ui/core';
import { KeyboardArrowRight } from '@material-ui/icons';
import React, { useContext, useState, useEffect } from 'react';
import styled from 'styled-components/macro';
import RadaccMap from '../../components/RadaccMap';
import { debugRooms, Room } from '../../types/Room';
import RoomCard from '../../components/RoomCard'
import { InspectRoomForm } from '../InspectRoom/InspectRoomForm';
import { Modal } from "../../components/Modal";
import { roomContext } from '../../contexts/RoomContext';
import { height } from '@mui/system';

// <RadaccMap items={context.rooms} onClickFunc={inspectRoomToggle}></RadaccMap>

const useStyles = makeStyles({
  field: {
    marginTop: 20,
    marginBottom: 20,
    display: 'block',
  },
});

export const DashboardPage = () => {
  const classes = useStyles();
  const context = useContext(roomContext);
  const [inspectRoom, setInspectRoom] = useState<Room | null>(null);

  const inspectRoomToggle = (room: Room) => {
    setInspectRoom(room);
  }
  
  return (
    <>

      <Grid container spacing={3}>
        {context.rooms.map(room => (
          <Grid item key={room.id} xs={12} md={6} lg={4}>
            <RoomCard room={room} onClickFunc={inspectRoomToggle}/>
          </Grid>
        ))}
      </Grid>

      <div style={{
        height: "2vh",
        width: "100%"
      }}>
      </div>

      {!context.view && (
        <div style={{
           margin: "0 auto",
            width: "70%"
        }}>

            <RadaccMap items={context.rooms} onClickFunc={inspectRoomToggle}></RadaccMap>
        </div>

      )}


      {inspectRoom && (
        <Modal title={"Inspect Room"} onCancel={() => setInspectRoom(null)}>
          <InspectRoomForm
            room={inspectRoom}
            afterSubmit={() => {
              setInspectRoom(null);
            }}
          />
        </Modal>
      )}
    </>
  );
};

export default DashboardPage;
