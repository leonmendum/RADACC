import { Publisher, PublisherType } from "./Publisher";

export type Room = {
  id: number;
  name: string;
  maxPeople: number;
  longitude1: number;
  latitude1: number;
  longitude2: number;
  latitude2: number;
  status?: number;
  color?: string;
  speed?: number;
  currentInRoom?: number;
  publisher?: Publisher[];
};

export const debugRooms: Room[] = [
  {
    id: 1,
    name: "Bereich 1",
    maxPeople: 15,
    longitude1: 100,
    latitude1: 100,
    longitude2: 1000,
    latitude2: 2500,
    publisher: [  
      {
        id: "1",
        name: "Test",
        type: PublisherType.CAM,
      },
    ],
  },
  {
    id: 2,
    name: "Bereich 2",
    maxPeople: 15,
    longitude1: 1000,
    latitude1: 1500,
    longitude2: 3500,
    latitude2: 3250,
  },
  {
    id: 3,
    name: "Bereich 3",
    maxPeople: 30,
    longitude1: 1000,
    latitude1: 250,
    longitude2: 2500,
    latitude2: 1500,
  },
  // {
  //   id: 4,
  //   name: "Bereich 4",
  //   maxPeople: 10,
  //   longitude1: 250,
  //   latitude1: 2500,
  //   longitude2: 1000,
  //   latitude2: 3750,
  // },
];
