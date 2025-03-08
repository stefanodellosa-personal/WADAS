import * as React from 'react';
import {useEffect} from 'react';
import {Container, Nav, Navbar} from "react-bootstrap";
import "../styles/App.css";
import {useNavigate, useLocation} from "react-router-dom";
// @ts-ignore
import logo from "../assets/wadas_logo.png";

const CustomNavbar = () => {
    const navigate = useNavigate();
    const location = useLocation();
    const [currentPath, setCurrentPath] = React.useState<string>(location.pathname);

    useEffect(() => {
        setCurrentPath(location.pathname);
    }, [location.pathname]);

    return (
        <Container>
            <Navbar bg="white" expand="lg" fixed="top" style={{padding: "0px"}}>
                <Container className="solid-grey-bottom-border" style={{padding: "8px"}}>
                    <Navbar.Brand href="/homepage" className="d-flex align-items-center" style={{fontWeight: "600"}} >
                        <img
                            src={logo}
                            alt="Logo"
                            style={{height: "40px", width: "40px", marginRight: "30px"}}
                        />
                        WADAS
                    </Navbar.Brand>
                    <Navbar.Toggle aria-controls="basic-navbar-nav"/>
                    <Nav className="me-auto">
                        <Nav.Link
                            onClick={() => navigate("/homepage")}
                            className={currentPath === "/homepage" || currentPath === "/" ? "selected-menu-item" : ""}
                        >
                            CAMERAS
                        </Nav.Link>
                        <Nav.Link
                            onClick={() => navigate("/detections")}
                            className={currentPath === "/detections" ? "selected-menu-item" : ""}
                        >
                            DETECTION EVENTS
                        </Nav.Link>
                        <Nav.Link
                            onClick={() => navigate("/actuations")}
                            className={currentPath === "/actuations" ? "selected-menu-item" : ""}
                        >
                            ACTUATION EVENTS
                        </Nav.Link>
                    </Nav>
                </Container>
            </Navbar>
        </Container>
    );
}

export default CustomNavbar;
