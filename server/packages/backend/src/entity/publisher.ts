import { Column, Entity, ManyToOne, OneToMany, PrimaryGeneratedColumn } from 'typeorm';
import { Entry } from './entry';
import { Room } from './room';

@Entity()
export class Publisher {
  @PrimaryGeneratedColumn('uuid')
  id: number;

  @Column()
  name: string;

  @Column({
    default: 'camera',
  })
  type: 'camera' | 'radar';

  @OneToMany(() => Entry, (entry) => entry.publisher)
  entries?: Entry[];

  @ManyToOne(() => Room, (room) => room.publisher)
  room?: Room;
}
