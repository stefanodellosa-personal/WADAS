import * as React from 'react';
import {useState} from "react";
import {Badge, Button, Card} from "react-bootstrap";
import "bootstrap/dist/css/bootstrap.min.css";
import "../styles/App.css"
import {Camera} from "../types/types";
import {useNavigate} from "react-router-dom";

// @ts-ignore
import {ReactComponent as CameraIcon} from "../assets/camera_circle.svg";


const CameraCard = (props: { camera: Camera, onActuatorsClick: (camera: Camera) => void }) => {
    const visibleActuators = props.camera.actuators.slice(0, 3);
    const navigate = useNavigate();

    const handleDetectionClick = () => {
        navigate("/detections", {state: {selectedCamera: props.camera}});
    };

    return (
        <Card className="h-100 thin-solid-grey-border m-3">
            <Card.Body className="d-flex flex-column" style={{padding: "1.7rem"}}>
                <Card.Title className="d-flex align-items-center mb-4">
                    <CameraIcon
                        style={{width: "40px", height: "40px"}}
                    />
                    <div className="ms-auto">
                        <span className="d-block mb-2">{props.camera.name}</span>
                        <span className="d-block card-subtitle">{props.camera.type}</span>
                    </div>
                </Card.Title>
                <hr/>
                <Card.Text className="mb-2">
                    <span style={{fontWeight: 600}}>Actuators: {props.camera.actuators.length}</span>
                </Card.Text>

                <div className="mb-3">
                    {visibleActuators.map((actuator, index) => (
                        <Badge key={index} className="me-2 mb-2 custom-badge">
                            {actuator.name}
                        </Badge>
                    ))}
                    {props.camera.actuators.length > 3 && (
                        <Button
                            variant="link"
                            className="p-0 custom-link-mid"
                            style={{fontWeight: 500}}
                            onClick={() => props.onActuatorsClick(props.camera)}
                        >
                            show more..
                        </Button>
                    )}
                </div>
                <hr/>

                <div className="d-flex justify-content-end mt-auto">
                    <Button variant="primary" className="custom-button dark-background" onClick={handleDetectionClick}>
                        Detection Events
                    </Button>
                </div>
            </Card.Body>
        </Card>
    );
};

export default CameraCard;
