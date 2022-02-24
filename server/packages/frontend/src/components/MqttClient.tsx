import mqtt, { MqttClient } from 'mqtt'
import { MessageRoom } from '../types/Message';

let client: MqttClient; 
export const MqttConnect = ({
  url,
  topic,
  onMessage,
} : {
  url: string,
  topic: string,
  onMessage?: (topic: string, message: string) => void,
}) => {
  client = mqtt.connect(url);
  //console.log("connected to: ", client.options);
  client.on("connect", function() {
    //console.log("connected");
    client.subscribe(topic, error => {
      if (error) console.error(error);
      else {
        //console.log("subscribe");
      }
    });
  });

  client.on("message", (topic, message) => {
    try {
      onMessage === undefined ? console.log(topic, message.toString()) : onMessage(topic, message.toString());
    } catch (e) {
      console.log(e);
    }
    client.end();
  });
} 

export const MqttSend = ({
  url,
  topic,
  message,
} : {
  url: string,
  topic: string,
  message: MessageRoom,
}) => {
  client = mqtt.connect(url);
  //console.log("connected to: ", client.options);
  client.on("connect", function() {
    //console.log("connected");
    client.subscribe(topic, error => {
      if (error) console.log(error);
      else {
        client.publish(topic, JSON.stringify(message));
      }
    })
  });
} 

export const MqttDisconnect = () => {
  console.log("disconnecting");
  client.end();
}

export default MqttConnect; 