import { Column, Entity, OneToMany, PrimaryGeneratedColumn } from 'typeorm';
import { Publisher } from './publisher';

@Entity()
export class Room {
  @PrimaryGeneratedColumn()
  id: number;

  @Column({ unique: true })
  name: string;

  @Column()
  maxPeople: number;

  @Column()
  longitude1: number;

  @Column()
  latitude1: number;

  @Column()
  longitude2: number;

  @Column()
  latitude2: number;

  @OneToMany(() => Publisher, (publisher) => publisher.room)
  publisher?: Publisher[];
}
