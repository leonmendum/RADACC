// tslint:disable-next-line: no-var-requires
require('dotenv-safe').config();
import 'reflect-metadata';
import express from 'express';
import { createDatabaseConnection } from './util/createDatabaseConnection';
import * as bodyParser from 'body-parser';
import { globalRouter } from './router/global.router';
import morgan from 'morgan';
import { MqttHandler } from './util/mqtt_handler';
const cors = require("cors")
// import { getRepository } from 'typeorm';
// import { Entry } from './entity/entry';

const port: number = Number(process.env.PORT);

/*
const onMessage = async (_: string, message: string) => {
  const entry: Entry = JSON.parse(message);
  const repository = getRepository(Entry);

  await repository.save(entry);

  console.log(
    `created new Entry : {${entry.id}, ${entry.totalDetected}, ${entry.totalEnter}, ${entry.totalExit}, ${entry.totalInRoom}}`,
  );
};
*/

export const startServer = async () => {
  try {
    const app = express();
    const dbConnection = await createDatabaseConnection();

    const mqttClient = new MqttHandler('radacc/#');
    mqttClient.connect();

    app.use((_, res, next) => {
      res.header('Access-Control-Allow-Origin', '*');
      res.header('Access-Control-Allow-Headers', 'X-Requested-With');
      next();
    });

    app.use(morgan('combined'));
    app.use(cors());
    app.use(bodyParser.json());
    app.use('/', globalRouter);

    const server = app.listen(port, () => console.log(`Server is now running on port: ${port}`));
    return { server, dbConnection };
  } catch (e) {
    console.log(e);
    throw e;
  }
};

// tslint:disable-next-line: no-floating-promises
startServer();
