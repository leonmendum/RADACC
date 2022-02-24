export enum PublisherType {
  CAM = "cam",
  RADAR = "radar",
}

export type Publisher = {
  id: string;
  name: string;
  type: PublisherType;
};
