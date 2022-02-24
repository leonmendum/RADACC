import React, { useEffect, useState } from "react";
import styled from "styled-components";
import RadaccMap from "../../components/RadaccMap";
import { debugRooms, Room } from "../../types/Room";
import mqtt from "mqtt";
import { Modal } from "../../components/Modal";
import { InspectRoomForm } from "../InspectRoom/InspectRoomForm";
import List from '@mui/material/List';
import ListItem from '@mui/material/ListItem';
import ListItemIcon from '@mui/material/List';
import ListItemText from '@mui/material/List';
import { ListItemButton, makeStyles } from "@mui/material";
import DraftsIcon from '@mui/icons-material/Circle';
import Color from 'color';

const FlexContainer = styled.div`
  height: 100%;
  width: 100%;
  display: flex;
  flex-direction: row;
`;

const Column = styled.div`
  display: flex;
  flex-direction: column;
  flex-basis: 100%;
  flex: 2;
  background-color: #999;
`;

const Column1 = styled.div`
  display: flex;
  flex-direction: column;
  flex-basis: 100%;
  flex: 1;
  background-color: #bbb;
`;  

const Row = styled.div`
  display: flex;
  flex-direction: row;
  flex-wrap: wrap;
  width: 100%;
`; 

const Text = ({items, name}:{items: any, name: string}) => {
  return (
      <div className={name} style={{
        height: "100%", 
        width: "100%"
      }}>
          <textarea
              className="form-control"
              style={{
                  height: "100%",
                  width: "100%",
                  resize: "none"
              }}
              value={
                  items.map((item: any) => JSON.stringify(item, undefined, 2))
              }
          />
      </div>
  );
};

export const DashboardPage = () => {
  const [rooms, setRooms] = useState<Room[]>([]);
  const [inspectRoom, setInspectRoom] = useState<Room | null>(null);

  const fetchRoom = async function () {
    try {
      const roomRequest = await fetch("http://localhost:4000/room");
      console.log("request:",roomRequest);
      if (roomRequest.status === 200) {
        const roomJson = await roomRequest.json();
        console.log("json:",roomJson);
        setRooms(roomJson.data);
      }
    } catch {
      console.log("Make sure the backend is running.")
    }
  };

  useEffect(() => {
    fetchRoom();
  }, []);

  const clickHandler2 = () => {
    const a = rooms.pop();
    var currentRooms = rooms.slice();
    setRooms(currentRooms);
  }

  const clickHandler3 = (room: Room) => {
    setInspectRoom(room);
  }

  return (  
    <>
      <Column1>
      <List>
        {debugRooms.map(item => (
          <ListItemButton key={item.name} onClick={() => {clickHandler3(item)}}>
            <ListItemIcon>{<DraftsIcon htmlColor={item.status === undefined ? '#888' : Color.hsv((120 - item.status * 120), 100, 100).hex()}></DraftsIcon>}</ListItemIcon>
            <ListItemText>{item.name}</ListItemText>
          </ListItemButton>
        ))}
      </List>  
      </Column1>
      <Column>
        <div style={{
          height: "80%", 
          width: "100%"
        }} 
        >
          <RadaccMap items={debugRooms} onClickFunc={clickHandler3}></RadaccMap>
        </div>
        <div style={{
          height: "20%", 
          width: "100%"
        }} >
          <Text items={rooms} name={"rooms"}/>
        </div>
      </Column>

      {inspectRoom && (
        <Modal title={"Inspect Room"} onCancel={() => setInspectRoom(null)}>
          <InspectRoomForm
            room={inspectRoom}
            afterSubmit={() => {
              setInspectRoom(null);
              fetchRoom();
            }}
          />
        </Modal>
      )}
      
    </>
  );
};
