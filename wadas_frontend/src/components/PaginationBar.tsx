import * as React from 'react';
import {Container, Pagination} from "react-bootstrap";
import "bootstrap/dist/css/bootstrap.min.css";
import "../styles/App.css"


const PaginationBar = (props: { currentPage: number, totalPages: number, onPageChange: (number) => void }) => {
    return (
        <Container className="d-flex justify-content-center mt-3" style={{height: "15%"}}>
            <Pagination>
                <Pagination.Prev
                    onClick={() => props.onPageChange(props.currentPage - 1)}
                    disabled={props.currentPage === 1}
                />
                {Array.from({length: props.totalPages}).map((_, index) => (
                    <Pagination.Item
                        key={index}
                        active={props.currentPage === index + 1}
                        onClick={() => {
                            if (props.currentPage !== (index + 1)) {
                                props.onPageChange(index + 1);
                            }
                        }}
                    >
                        {index + 1}
                    </Pagination.Item>
                ))}
                <Pagination.Next
                    onClick={() => props.onPageChange(props.currentPage + 1)}
                    disabled={props.currentPage === props.totalPages}
                />
            </Pagination>
        </Container>
    );
};

export default PaginationBar;