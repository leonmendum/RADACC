import { Column, Entity, ManyToOne, PrimaryGeneratedColumn } from 'typeorm';
import { Publisher } from './publisher';

@Entity()
export class Entry {
  @PrimaryGeneratedColumn()
  id: number;

  @Column()
  datetimePicture: string;

  @Column()
  timestampPicture: string;

  @Column()
  datetimeSend: string;

  @Column()
  timestampSend: string;

  @Column()
  totalFrames: number;

  @Column()
  totalDetected: number;

  @Column()
  totalEnter: number;

  @Column()
  totalExit: number;

  @Column()
  totalInRoom: number;

  @ManyToOne(() => Publisher, (publisher) => publisher.entries)
  publisher?: Publisher;
}
