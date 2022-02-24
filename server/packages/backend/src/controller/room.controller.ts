import { getRepository } from 'typeorm';
import { Request, Response } from 'express';
import { Room } from '../entity/room';

export const getRooms = async (_: Request, res: Response) => {
  const entryRepository = await getRepository(Room);
  const rooms = await entryRepository.find();

  res.setHeader('content-type', 'application/json');
  res.setHeader('charset', 'UTF-8');

  res.send({
    data: rooms,
  });
};
