import * as React from "react";
import {useEffect, useState} from "react";
import {Alert, Button, Col, Container, Row} from "react-bootstrap";
import "bootstrap/dist/css/bootstrap.min.css";
import CustomNavbar from "./components/CustomNavbar";
import Select, {MultiValue} from "react-select";
import DatePick from "./components/DatePick";
import {tryWithRefreshing} from "./lib/utils";
import DetectionsScrollableTable from "./components/DetectionsScrollableTable";
import {useLocation, useNavigate} from 'react-router-dom';
import CustomSpinner from "./components/CustomSpinner";
import {AnimalsResponse, Camera, CamerasResponse, DetectionEvent, DetectionEventResponse} from "./types/types";
import {fetchAnimalsNames, fetchCameras, fetchDetectionEvents, fetchExportDetectionEvents} from "./lib/api";
import DetailsContainer from "./components/DetailsContainer";


type CameraOption = {
    value: string;
    label: string;
}

type AnimalOption = {
    value: string;
    label: string;
}

const DetectionEvents = () => {
    const pageSize = 20;
    const location = useLocation();
    const [prevClickedCamera, setPrevClickedCamera] = useState(null);
    const [optionsCameras, setOptionsCameras] = useState<CameraOption[]>([]);
    const [optionsAnimals, setOptionsAnimals] = useState<AnimalOption[]>([]);
    const [cameras, setCameras] = useState<Camera[]>([]);
    const [detections, setDetections] = useState<DetectionEvent[]>([]);
    const [loading, setLoading] = useState<boolean>(true);
    const [exportLoading, setExportLoading] = useState<boolean>(false);
    const [selectedCameras, setSelectedCameras] = useState<MultiValue<CameraOption>>([]);
    const [selectedAnimals, setSelectedAnimals] = useState<MultiValue<AnimalOption>>([]);
    const [error, setError] = useState<string | null>(null);
    const [exportError, setExportError] = useState<string | null>(null);
    const [currentPage, setCurrentPage] = useState(1);
    const [totalPages, setTotalPages] = useState(1);
    const navigate = useNavigate();
    const [startDate, setStartDate] = useState<Date | null>(null);
    const [endDate, setEndDate] = useState<Date | null>(null);
    const [currentEvent, setCurrentEvent] = useState<DetectionEvent | null>(null)


    const updateDateRange = (dates: [Date | null, Date | null]) => {
        const [start, end] = dates;
        setStartDate(start);
        setEndDate(end);
    };

    const updateDetectionData = async (page = 1) => {
        try {
            const offset = (page - 1) * pageSize;
            const detectionsResponse: DetectionEventResponse = await tryWithRefreshing(() =>
                fetchDetectionEvents(
                    offset,
                    selectedCameras.map(cam => cam.value),
                    selectedAnimals.map(animal => animal.value),
                    startDate,
                    endDate
                )
            );
            setDetections(detectionsResponse.data)
            setTotalPages(Math.ceil(detectionsResponse.total / pageSize));
            setCurrentPage(page);
            setCurrentEvent(null);
            setLoading(false);
        } catch (e) {
            if (e instanceof Error && e.message.includes("Unauthorized")) {
                console.error("Refresh token failed, redirecting to login...");
                navigate("/");
            } else {
                setError("Generic Error. Please contact the administrator.");
                setLoading(false);
            }
        }
    };

    useEffect(() => {
        if (location.state?.selectedCamera) {
            const clickedCamera = location.state?.selectedCamera;
            setPrevClickedCamera(clickedCamera);
            setSelectedCameras([{value: clickedCamera.id.toString(), label: clickedCamera.name}]);
            location.state.selectedCamera = null;
        }

        const fillCamerasOptions = async () => {
            try {
                const cameraResponse: CamerasResponse = await tryWithRefreshing(fetchCameras);
                let optionsArray = cameraResponse.data.map(camera => ({
                    value: camera.id.toString(),
                    label: camera.name
                }));

                setCameras(cameraResponse.data);
                setOptionsCameras(optionsArray)
                setLoading(false);
            } catch (e) {
                if (e instanceof Error && e.message.includes("Unauthorized")) {
                    console.error("Refresh token failed, redirecting to login...");
                    navigate("/");
                } else {
                    setError("Generic Error. Please contact the administrator.");
                }
            }
        };

        const fillAnimalsOptions = async () => {
            try {
                const animalsResponse: AnimalsResponse = await tryWithRefreshing(fetchAnimalsNames);
                let optionsArray = animalsResponse.data.map(animalName => ({
                    value: animalName,
                    label: animalName
                }));

                setOptionsAnimals(optionsArray)
                setLoading(false);
            } catch (e) {
                if (e instanceof Error && e.message.includes("Unauthorized")) {
                    console.error("Refresh token failed, redirecting to login...");
                    navigate("/");
                } else {
                    setError("Generic Error. Please contact the administrator.");
                }
            }
        };

        fillCamerasOptions();
        fillAnimalsOptions();
        updateDetectionData();
        // eslint-disable-next-line react-hooks/exhaustive-deps
    }, [prevClickedCamera]);

    // Gestore del cambio di selezione
    const handleChangeCameras = (selected: MultiValue<CameraOption>) => {
        setSelectedCameras(selected);
    };

    const handleChangeAnimals = (selected: MultiValue<AnimalOption>) => {
        setSelectedAnimals(selected);
    };


    const exportResults = () => async () => {
        setExportLoading(true);
        try {
            const responseBlob: Blob = await tryWithRefreshing(() =>
                fetchExportDetectionEvents(
                    selectedCameras.map(cam => cam.value),
                    selectedAnimals.map(animal => animal.value),
                    startDate,
                    endDate
                )
            );

            const url = window.URL.createObjectURL(responseBlob);
            const a = document.createElement("a");
            a.href = url;
            a.download = "detection_events.csv";
            document.body.appendChild(a);
            a.click();
            document.body.removeChild(a);
            window.URL.revokeObjectURL(url);
        } catch (e) {
            if (e instanceof Error && e.message.includes("Unauthorized")) {
                console.error("Refresh token failed, redirecting to login...");
                navigate("/");
            } else {
                setExportError("Problem exporting data");
            }
        } finally {
            setExportLoading(false);
        }
    }

    const showDetails = (event: DetectionEvent) => {
        setCurrentEvent(event);
    }

    return (
        <div className={"padded-div"}>
            <CustomNavbar/>
            <Container className={"mt-1"}>
                {loading ? (
                    <Container style={{flex: 1, display: "flex", flexDirection: "column"}}>
                        <CustomSpinner/>
                    </Container>
                ) : error ? (
                    <Alert variant="danger">{error}</Alert>
                ) : (
                    <Container style={{flex: 1, display: "flex", flexDirection: "column"}}>
                        <Container style={{height: "45vh", display: "flex", flexDirection: "column"}}>
                            <Container className="mt-3">
                                <Row className="mb-3">
                                    <Col md={3}>
                                        <Select
                                            id="multi-select"
                                            isMulti
                                            options={optionsCameras}
                                            value={selectedCameras}
                                            onChange={handleChangeCameras}
                                            placeholder={<div className={"custom-placeholder"}>select
                                                cameras...</div>}
                                        />
                                    </Col>
                                    <Col md={3}>
                                        <Select
                                            id="multi-select"
                                            isMulti
                                            options={optionsAnimals}
                                            value={selectedAnimals}
                                            onChange={handleChangeAnimals}
                                            placeholder={<div className={"custom-placeholder"}>select
                                                animals...</div>}
                                        />
                                    </Col>
                                    <Col md={3}>
                                        <DatePick
                                            startDate={startDate}
                                            endDate={endDate}
                                            onDateChange={updateDateRange}
                                        />
                                    </Col>
                                    <Col md={1}>
                                        <Button
                                            variant="primary"
                                            className="custom-button dark-background"
                                            onClick={() => updateDetectionData(1)}>
                                            Apply
                                        </Button>
                                    </Col>

                                    <Col md={2} className="d-flex">
                                        {exportLoading ? (
                                            <CustomSpinner className={"mt-1 ms-auto me-5"} />
                                        ) : exportError ? (
                                            <Alert variant="danger" className={"m-0 p-2"} style={{fontSize:"12px"}}>{exportError}</Alert>
                                        ) : (
                                            <Button
                                                variant="primary"
                                                className="custom-button ms-auto"
                                                onClick={exportResults()}>
                                                Export results
                                            </Button>)
                                        }
                                    </Col>
                                </Row>
                            </Container>

                            <Container style={{flex: 1, overflow: "hidden"}}>
                                <DetectionsScrollableTable
                                    detections={detections}
                                    knownCameras={cameras}
                                    currentPage={currentPage}
                                    totalPages={totalPages}
                                    onPageChange={updateDetectionData}
                                    onRowSelected={showDetails}
                                />
                            </Container>
                        </Container>

                        <Container className="my-2">
                            <hr/>
                        </Container>

                        <DetailsContainer currentEvent={currentEvent} cameras={cameras}/>
                    </Container>
                )}
            </Container>

        </div>
    );
};

export default DetectionEvents;
