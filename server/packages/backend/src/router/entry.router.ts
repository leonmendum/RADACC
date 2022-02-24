import { Router } from 'express';
import { getEntries } from '../controller/entry.controller';

export const entryRouter = Router({ mergeParams: true });

// get all entries
entryRouter.get('/', getEntries);
