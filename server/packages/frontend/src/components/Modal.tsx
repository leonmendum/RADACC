import React from "react";
import ReactDOM from "react-dom";
import styled from "styled-components/macro";

//Z-index causes the Modal to be rendered ontop of the Map
//without the map would obscure the popup
const ModalHolder = styled.div`
  position: fixed;
  top: 0px;
  left: 0px;
  height: 100%;
  width: 100%;
  background-color: rgba(0, 0, 0, 0.4);
  z-index: 1000;
`;

export const ModalMask = styled.div`
  border: solid;
  border-radius: 8px;
  padding: 20px 16px;
  box-shadow: 0 4px 5px rgba(0, 0, 0, 0.075);
  background-color: #ffffff;
  display: flex;
  flex-direction: column;
  align-items: stretch;
  justify-content: flex-start;
  width: 60%;
  height: 80%;
  line-height: 25.2px;
`;
export const ModalMaskHolder = styled.div`
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: inherit;
  height: 100%;
  color: #000;
`;

const ModalHeader = styled.div`
  display: flex;
  width: 100%;
`;

const ModalTitle = styled.h3`
  flex: 1;
`;

const ModalCloseButton = styled.button`
  all: unset;
  color: #000;
  cursor: pointer;
`;

export const Modal: React.FC<{
  title: string;
  onCancel: () => void;
}> = ({ children, title, onCancel }) => {
  const modalRoot = document.getElementById("modal-root");
  return ReactDOM.createPortal(
    <ModalHolder>
      <ModalMaskHolder>
        <ModalMask>
          <ModalHeader>
            <ModalTitle>{title}</ModalTitle>{" "}
            <ModalCloseButton onClick={onCancel}>close</ModalCloseButton>{" "}
          </ModalHeader>{" "}
          {children}
        </ModalMask>
      </ModalMaskHolder>
    </ModalHolder>,
    // @ts-ignore
    modalRoot
  );
};
