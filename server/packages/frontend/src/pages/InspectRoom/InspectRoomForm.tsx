import { useEffect, useState } from "react";
import MqttConnect, { MqttDisconnect } from "../../components/MqttClient";
import { Room } from "../../types/Room";

export const InspectRoomForm: React.FC<{
  afterSubmit: () => void;
  room: Room;
}> = ({ afterSubmit, room }) => {
  const [values, setValues] = useState({
    id: room.id,
    name: room.name,
    maxPeople: room.maxPeople,
    longitude1: room.latitude1,
    latitude1: room.latitude1,
    longitude2: room.longitude2,
    latitude2: room.latitude2,
  });

  useEffect(() => {
    MqttConnect({url: "ws://broker.mqttdashboard.com:8000/mqtt", topic: `radacc/${values.id}/cam`});
    MqttConnect({url: "ws://broker.mqttdashboard.com:8000/mqtt", topic: `radacc/${values.id}/radar`});
  }, []);

  useEffect( () => () => MqttDisconnect(), [] );

  return (
    <div
      style={{
        display: "flex",
        flexDirection: "column",
      }}
    >
      <p>{`id: ${values.id}`}</p>  
      <p>{`name: ${values.name}`}</p> 
      <p>{`amount: ${values.maxPeople}`}</p> 
      <p>{`cords: ${values.latitude1} ${values.longitude1}`}</p>
      <p>{`cords: ${values.longitude2} ${values.longitude2}`}</p>  
    </div>
  );
};
