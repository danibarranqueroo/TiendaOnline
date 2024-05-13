import { useState, useEffect } from 'react';
import { PrimeReactProvider, PrimeReactContext } from 'primereact/api';
import Navegacion from './components/Navegacion.jsx';
import Resultados from './components/Resultados.jsx';
import './App.css';

const App = () => {
  const [productos, setProductos] = useState([]);
  const [productosF, setProductosF] = useState([]);
  const [categorias, setCategorias] = useState([]);

  const fetchProductos = async () => {
    const response = await fetch("http://localhost/api/productos?desde=0&hasta=100");
    const prods = await response.json();
    setProductos(prods);
    const uniqueCategorias = Array.from(new Set(prods.map((producto) => producto.category)));
    setCategorias(uniqueCategorias);
    setProductosF(prods);
  };

  useEffect(() => {
    fetchProductos();
  }, []);

  const handleSearchChange = (evento) => {
    const value = evento.target.value;
    const filteredProductos = value !== "" ? productos.filter((producto) => producto.title.includes(value)) : productos;
    setProductosF(filteredProductos);
    console.log(value);
  };

  const handleCategoryChange = (evento) => {
    const value = evento.target.value;
    const filteredProductos = value !== "" ? productos.filter((producto) => producto.category.includes(value)) : productos;
    setProductosF(filteredProductos);
    console.log(value);
  };

  return (
    <>
      <Navegacion cambiado={handleSearchChange} categorias={categorias} cambiadoCat={handleCategoryChange}/>
      <Resultados productos={productosF}/>
    </>
  );
};

export default App;