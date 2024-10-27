import React from 'react';
import { Route, Routes } from 'react-router-dom';
import Home from './pages/Home.jsx';
import './App.css';

function App() {
  return (
    <Routes>
      {/* Default page is Home */}
      <Route path="/" element={<Home />} />
      <Route path="/home" element={<Home />} />
    </Routes>
  );
}

export default App;
// add this to the react app because the api requests go through express
export const fetchData = async () => {
  const response = await fetch('/api/endpoint'); // No need to include the domain
  const data = await response.json();
  return data;
};

// would also need to run the app and create a build directory