import { useState, useEffect } from 'react'
import './App.css'

function App() {


  useEffect(() => {
    fetch("http://127.0.0.1:8000/trips").then();
  }, []);

  return (
    <h1>RideQ</h1>
  )
}

export default App
