import mqtt from 'mqtt';

export class MqttHandler {
  mqttClient: any;
  topic: string;
  onMessage?: (topic: string, message: string) => void;

  constructor(topic: string, onMessage?: (topic: string, message: string) => void) {
    this.mqttClient = null;
    this.topic = topic;
    this.onMessage = onMessage;
  }

  connect() {
    // Connect mqtt with credentials (in case of needed, otherwise we can omit 2nd param)
    this.mqttClient = mqtt.connect('mqtt://broker.hivemq.com');

    // Mqtt error calback
    this.mqttClient.on('error', (err: any) => {
      console.log(err);
      this.mqttClient.end();
    });

    // Connection callback
    this.mqttClient.on('connect', () => {
      console.log(`mqtt client connected to: ${this.topic}`);
      console.log('----------------------------------------------------------------------');
    });

    // mqtt subscriptions
    this.mqttClient.subscribe(this.topic, { qos: 0 });

    // When a message arrives, console.log it
    // First parameter is the topic
    this.mqttClient.on('message', (topic: any, message: any) => {
      try {
        this.onMessage === undefined ? console.log(message.toString()) : this.onMessage(topic, message);
      } catch (e) {
        console.log(e);
      }
    });

    this.mqttClient.on('close', () => {
      console.log(`mqtt client disconnected`);
    });
  }

  // Sends a mqtt message to topic: mytopic
  sendMessage(message: any) {
    this.mqttClient.publish(this.topic, message);
  }
}
