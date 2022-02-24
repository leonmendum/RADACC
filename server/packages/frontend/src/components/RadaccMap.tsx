import L, {LatLngBounds, Map, CRS, map, DivIcon, LatLngExpression} from 'leaflet';
import React, { useContext, useEffect, useMemo, useRef, useState } from 'react';
import background from '../assets/backgroundMap.png';
import {
  MapContainer,
  TileLayer,
  Marker,
  Popup,
  ImageOverlay,
  useMap,
  Rectangle,
  useMapEvents,
  MapConsumer,
  Tooltip,
} from 'react-leaflet';
import '../css/App.css';
import { Room } from '../types/Room';
import Color from 'color';
import { roomContext } from '../contexts/RoomContext';

const bounds = new L.LatLngBounds([
  [0, 0],
  [4000, 4000],
]);

const RadaccMap = ({ items, onClickFunc }: { items: Room[], onClickFunc: (item: Room) => void }) => {
  const context = useContext(roomContext)
  let pr = L.extend({}, L.CRS.Simple, {
    transformation: new L.Transformation(1, 0, 1, 0),
  });

  console.log(items);

  return (

    <div style={{
      height: "70vh",
    }} 
    >
      <MapContainer
        center={[0, 0]}
        zoom={5}
        scrollWheelZoom={true}
        crs={pr}
        maxZoom={30}
        minZoom={-5}
        maxBounds={bounds}
      >
        <ImageOverlay url={background} bounds={bounds} opacity={1} zIndex={10} />
        <MapConsumer>
          {(map) => {
            map.fitBounds(bounds);
            return null;
          }}
        </MapConsumer>
        {items.map((item: Room) => (
          <Rectangle
            key={item.id}
            bounds={
              new LatLngBounds(
                [item.longitude2, item.latitude2],
                [item.longitude1, item.latitude1]
              )
            }
            color={'#000000'}
            fillColor={item.color === undefined ? '#888' : item.color}
            fillOpacity={0.99}
          >

              <Marker
                  position={ 
                    L.polygon([[item.longitude2 - (item.name.length*5), item.latitude2 - (item.name.length*20)],
                              [item.longitude2 - (item.name.length*5), item.latitude1 - (item.name.length*20)],
                              [item.longitude1 - (item.name.length*5), item.latitude1 - (item.name.length*20)],
                              [item.longitude1 - (item.name.length*5), item.latitude2 - (item.name.length*20)]]).getBounds().getCenter()
                    }
                  icon={L.divIcon({
                        html: "<i style='position: absolute; width:1000px; font-size:14px; " +
                        "font-family: Helvetica Neue, Helvetica, Arial, sans-serif; color: #121212'>" + item.name + "</i>",
                        className: 'dummy'
                      })
                  }

              />

            <Popup>
              <p>{`Id: ${item.id}`}</p>
              <p>{`Name: ${item.name}`}</p>
              <p>{`Max People: ${item.maxPeople}`}</p>
              <p>{`Cords1: (${item.latitude1} , ${item.longitude1})`}</p>
              <p>{`Cords2: (${item.latitude2} , ${item.longitude2})`}</p>
              <p>{`status: ${item.status}`}</p>
              <button onClick={() => onClickFunc(item)}>Inspect </button>
            </Popup>
          </Rectangle>
        ))};
      </MapContainer>
    </div>
  );
};

export default RadaccMap;


