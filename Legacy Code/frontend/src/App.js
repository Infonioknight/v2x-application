import React, { useState, useEffect } from 'react'
import './App.css'
// import ReactDOM from "react-dom/client";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import Table from './Pages/Table'
import Mapper from './Pages/Mapper'
// import Test2 from './Pages/Test2'
import Navbar from './Pages/Navbar'


function App() {
  const [data, setData] = useState([{}])

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await fetch('/vehicle');
        if (!response.ok) {
          throw new Error('Failed to fetch data');
        }
        const result = await response.json();
        setData(result)

      } catch (error) {
        console.log(error)
      }
    };
    fetchData();
    const interval = setInterval(fetchData, 5000);

    return () => clearInterval(interval);
  }, []);
    
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Navbar />}>
          <Route index element={<Table data={data} />} />
          <Route path="map" element={<Mapper coords={data}/>} />
          {/* <Route path="table" element={<Table data={data}/>} /> */}
        </Route>
      </Routes>
    </BrowserRouter>
  )
}

export default App