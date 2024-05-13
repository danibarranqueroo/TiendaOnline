import React from 'react';
import { Button, Container, Form, Navbar, NavDropdown } from 'react-bootstrap';

export default function Navegacion({ cambiado, categorias, cambiadoCat }) {
    return (
        <Navbar bg="light" expand="lg" fixed="top">
            <Container fluid>
                <Navbar.Brand href="#">Tienda DAI</Navbar.Brand>
                <Navbar.Toggle aria-controls="navbarScroll" />
                <Navbar.Collapse id="navbarScroll">
                    <Form className="d-flex ms-auto">
                        <Form.Group className="me-2">
                            <Form.Select aria-label="Categorías" onChange={(evento) => cambiadoCat(evento)}>
                                <option value="">Categories</option>
                                {categorias.map((categoria, index) => (
                                    <option key={index} value={categoria}>{categoria}</option>
                                ))}
                            </Form.Select>
                        </Form.Group>
                        <Form.Group className="me-2">
                            <Form.Control type="search" placeholder="Search" aria-label="Search" onChange={(evento) => cambiado(evento)} />
                        </Form.Group>
                        <Button variant="outline-success" className="mt-2">Search</Button>
                    </Form>
                </Navbar.Collapse>
            </Container>
        </Navbar>
    );
}