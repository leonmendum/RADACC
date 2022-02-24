import { Router, Request, Response } from 'express';
import { entryRouter } from './entry.router';
import { roomRouter } from './room.router';

export const globalRouter = Router({ mergeParams: true });

globalRouter.get('/', async (_: Request, res: Response) => {
  res.send({
    message: 'Hello World',
  });
});

globalRouter.use('/entry', entryRouter);
globalRouter.use('/room', roomRouter);
