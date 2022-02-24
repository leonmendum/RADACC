import { AppBar, Button, Divider, makeStyles, styled, Toolbar } from "@material-ui/core";
import React, { useContext, useEffect, useState } from "react";
import Drawer from "@mui/material/Drawer";
import Typography from "@mui/material/Typography";
import List from "@mui/material/List";
import ListItem from "@mui/material/ListItem";
import ListItemIcon from "@mui/material/ListItemIcon";
import ListItemText from "@mui/material/ListItemText";
import { debugRooms, Room } from "../types/Room";
import { ListItemButton } from "@mui/material";
import CircleIcon from '@mui/icons-material/Circle';
import DeleteIcon from '@mui/icons-material/Delete';
import Color from 'color';
import { InspectRoomForm } from "../pages/InspectRoom/InspectRoomForm";
import { Modal } from "./Modal";
import { roomContext } from "../contexts/RoomContext";
import { color } from "@mui/system";
import EmailIcon from '@mui/icons-material/Email';
import { MqttSend } from "./MqttClient";

const drawerWidth = 240;
let roomCounter = 0;

function getRandomInt(max: number) {
  return Math.floor(Math.random() * max) + 1;
}

function getRandomFloat() {
  return parseFloat((Math.random() * (5.00 - 0.20) + 0.20).toFixed(2))
}

const useStyles = makeStyles((theme) => {
  return {
  page: {
    width: '100%',
    height: '100%',
    minHeight: '90vh',
    padding: theme.spacing(0),
  },
  drawer: {
    width: drawerWidth,
  },
  drawerPaper: {
    width: drawerWidth,
  },
  root: {
    display: 'flex',
    "& .MuiPaper-root": {
      background: '#121212',
      color: '#fff',
    }
  },
  title: {
    padding: theme.spacing(2),
    flex: 'auto',
  },
  appbar: {
    width: `calc(100% - ${drawerWidth}px)`,
    height: '0px',
  },
  toolbar: theme.mixins.toolbar,
  }
})

export const Layout: React.FC = ({ children }) => {
  const classes = useStyles();
  const context = useContext(roomContext);
  const [inspectRoom, setInspectRoom] = useState<Room | null>(null);
  const [open, setOpen] = useState(false);

  const handleDrawerOpen = () => {
    setOpen(true);
  };

  const handleDrawerClose = () => {
    setOpen(false);
  };

  const inspectRoomToggle = async (room: Room) => {
    await setInspectRoom(null);
    setInspectRoom(room);
  }

  const toggleMap = async () => {
    await context.actions.setView(!context.view);
  }

  useEffect(() => {
    context.actions.fetchRoom();
  }, []);

  return (
    <>
    <div className={classes.root}>
      {/* app bar */}

      <AppBar className={classes.appbar} elevation={0}>
        <Toolbar>
          <Typography className={classes.title}>
            Radacc
          </Typography>
          <Button variant="contained" onClick={() => {
            toggleMap()
          }}>Toggle Map</Button>
        </Toolbar>
      </AppBar>

      {/*left side drawer */}
      <Drawer
        className={classes.drawer}
        classes={{ paper: classes.drawerPaper }}
        variant="permanent"
        anchor="left"
      >
        <div>
          <Typography variant="h5" className={classes.title}>
            Rooms
          </Typography>  
        </div> 

        <List>
          {context.rooms.map(item => (
            <ListItemButton key={item.name} onClick={() => {inspectRoomToggle(item)}}>
              <ListItemIcon>{<CircleIcon htmlColor={item.status === undefined ? '#888' : Color.hsv((120 - item.status * 120), 100, 100).hex()}></CircleIcon>}</ListItemIcon>
              <ListItemText primary={item.name} />
            </ListItemButton>
          ))}
        </List>

        <Divider />

        <List>
          <ListItemButton key={'Send Message !'} onClick={() => {
            MqttSend({url: "ws://broker.mqttdashboard.com:8000/mqtt", topic: `radacc/${(roomCounter % 3) + 1}/cam`, message: {
              totalDetected: getRandomInt(30),
            }});
            MqttSend({url: "ws://broker.mqttdashboard.com:8000/mqtt", topic: `radacc/${(roomCounter % 3) + 1}/radar`, message: {
              speed: getRandomFloat(),
            }});
            roomCounter = roomCounter + 1;
          }}>
            <ListItemIcon>{<EmailIcon htmlColor={'white'}></EmailIcon>}</ListItemIcon>
            <ListItemText primary={'Send Test Message !'} />
          </ListItemButton>        
        </List>
          
      </Drawer>
      
      <div className={classes.page} >
        <div className={classes.toolbar} />
        {children}
      </div>
    </div>

    {inspectRoom && (
      <Modal title={"Inspect Room"} onCancel={() => setInspectRoom(null)}>
        <InspectRoomForm
          room={inspectRoom}
          afterSubmit={() => {
            setInspectRoom(null);
          }}
        />
      </Modal>
    )}
    </>
  );
};

export default Layout;
