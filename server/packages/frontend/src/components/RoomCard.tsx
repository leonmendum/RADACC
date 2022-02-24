import { Avatar, Button, Card, CardContent, CardHeader, IconButton, makeStyles, Typography } from '@material-ui/core';
import { DeleteOutlined } from '@material-ui/icons';
import CircleIcon from '@mui/icons-material/Circle';
import React from 'react'
import { Room } from '../types/Room';
import SearchIcon from '@mui/icons-material/Search';
import Color from 'color';

const useStyles = makeStyles({
  border: {
    border: (room : Room) => {
      return `2px solid ${room.color === undefined ? '#888' : room.color}`;
    }
  },
  text: {
    color: (room : Room) => {
      return `${room.color === undefined ? '#888' : room.color}`;
    }
  }
})

export const RoomCard = ({ room, onClickFunc } : { room: Room, onClickFunc: (room: Room) => void }) => {
  const classes = useStyles(room);

  return (
    <div>
      <Card elevation={1} className={classes.border}>
        <CardHeader 
          action={
            <Button onClick={() => onClickFunc(room)}>
              <SearchIcon />
            </Button >
          }
          title={room.name}
          subheader={
          <Typography display="inline">
            People:  
            <Typography display="inline" className={classes.text}>
              &nbsp; {room.currentInRoom === undefined ? 0 : room.currentInRoom}/{room.maxPeople}
            </Typography>
            <Typography display="inline">
              &nbsp;| Avg. Speed: 
            </Typography>
            <Typography display="inline" className={classes.text}>
              &nbsp; {room.speed === undefined ? 0 : room.speed} m/s
            </Typography>
          </Typography>
          }
        />
        <CardContent>
          <Typography variant='body2' color="textSecondary">
            {`cords: ${room.latitude1} ${room.longitude1} `} 
            {`cords: ${room.latitude2} ${room.longitude2} `}
          </Typography>
        </CardContent>
      </Card>
    </div>
  )
}

export default RoomCard;
