import { Router } from 'express';
import { getRooms } from '../controller/room.controller';

export const roomRouter = Router({ mergeParams: true });

// get all rooms
roomRouter.get('/', getRooms);
