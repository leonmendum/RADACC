import { getRepository } from 'typeorm';
import { Request, Response } from 'express';
import { Entry } from '../entity/entry';

export const getEntries = async (_: Request, res: Response) => {
  const entryRepository = await getRepository(Entry);
  const entries = await entryRepository.find();

  res.setHeader('content-type', 'application/json');
  res.setHeader('charset', 'UTF-8');

  res.send({
    data: entries,
  });
};
