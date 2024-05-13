import React from 'react';
import Card from 'react-bootstrap/Card';
import CardGroup from 'react-bootstrap/CardGroup';
import Col from 'react-bootstrap/Col';
import Row from 'react-bootstrap/Row';
import Button from 'react-bootstrap/Button';
import { Rating } from 'primereact/rating';

export default function Resultados({ productos }) {
    return (
        <Row xs={1} sm={1} md={2} lg={3} xl={4} className="g-4">
            {productos.map((producto) => (
                <Col key={producto.id}>
                    <Card>
                        <Card.Img variant="top" src={`${producto.image}`} />
                        <Card.Body>
                            <Card.Title>{producto.title}</Card.Title>
                            <Card.Text>{producto.description}</Card.Text>
                        </Card.Body>
                        <div className="d-flex justify-content-center align-items-center">
                            <Rating value={producto.rating.rate} readOnly cancel={false} className="mr-2" />
                            <p style={{ paddingLeft: '20px' }} className="m-0">{producto.price} €</p>
                        </div>
                    </Card>
                </Col>
            ))}
        </Row>
    );
}