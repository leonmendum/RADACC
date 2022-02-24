import React, { useState } from "react";
import MqttConnect from "../components/MqttClient";
import { debugRooms, Room } from "../types/Room";
import mqtt from 'mqtt'
import Color from "color";

export type RoomContext = {
  rooms: Room[];
  view: boolean;
  actions: {
    fetchRoom: () => Promise<void>;
    setRoom: (rooms: Room[]) => Promise<void>;
    setView: (foo: boolean) => Promise<void>;
  }
}

export const initialRoomContext = {
  rooms: [],
  view: true,
  actions: {
    fetchRoom: async () => {},
    setRoom: async (rooms: Room[]) => {},
    setView: async (foo: boolean) => {},
  }
}

export const roomContext = React.createContext<RoomContext>(initialRoomContext);

export const RoomProvider: React.FC = ({ children }) => {
  const [rooms, setRooms] = useState<Room[]>([]);
  const [viewBool, setViewBool] = useState<boolean>(true);

  const setRoom = async (rooms: Room[]) => {
    var currentRooms = rooms.slice();
    await setRooms(currentRooms);
  }

  const onMessage = (topic: string, message: string) => {
    try {
      console.log(topic, message);
      const obj = JSON.parse(message);
      const parts = topic.split('/');
      const topicType = parts[2];

      switch(topicType) { 
        case 'cam': { 
            camMessage(rooms, parts, obj, setRoom); 
          break; 
        } 
        case 'radar': {
          if(obj.speed !== 0) {
            radarMessage(rooms, parts, obj, setRoom);
          }
          break; 
        } 
        default: { 
           console.log('unknown Topic', topicType)
          break; 
        } 
     }

    } catch (e) {
      //console.log(e);
    }
  }

  const fetchRoom = async () => {
    try {
      const roomRequest = await fetch("http://localhost:4000/room");
      console.log("request:",roomRequest);
      if (roomRequest.status === 200) {
        const roomJson = await roomRequest.json();
        console.log("json:",roomJson);
        await setRooms(roomJson.data);
        
      }
    } catch {
      console.log("Fetching faild loading debug rooms.")
      await setRooms(debugRooms);
    }
  };

  const setView = async (foo: boolean) => {
    setViewBool(foo);
  };

  MqttConnect({url: "ws://broker.mqttdashboard.com:8000/mqtt", topic: "radacc/#", onMessage: onMessage});

  return <roomContext.Provider value={{
    rooms:rooms,
    view:viewBool,
    actions:{
      fetchRoom,
      setRoom,
      setView,
    }
  }}>
    {children}
  </roomContext.Provider>
}

function camMessage(rooms: Room[], parts: string[], obj: any, setRoom: (rooms: Room[]) => Promise<void>) {
  const room = rooms.find(element => element.id === parseInt(parts[1]));
  if (room) {
    room.currentInRoom = parseInt(obj.totalDetected);
    room.status = room.currentInRoom < room.maxPeople ? room.currentInRoom / room.maxPeople : 1;
    room.color = room.status === undefined ? '#888' : Color.hsv((120 - room.status * 120), 100, 100).hex();
    setRoom(rooms);
    //console.log(message);
  }
}

function radarMessage(rooms: Room[], parts: string[], obj: any, setRoom: (rooms: Room[]) => Promise<void>) {
  const room = rooms.find(element => element.id === parseInt(parts[1]));
  if (room) {
      room.speed = parseFloat(obj.speed);
      setRoom(rooms);
  }
}
