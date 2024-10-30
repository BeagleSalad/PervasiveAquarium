import React, { useState, useEffect } from "react";
import './index.css'; // Ensure this stylesheet exists

const API_BASE_URL = 'http://localhost:8000'; // Adjust according to your backend

const AquariumThermostat = () => {
  const [aquariumID, setAquariumID] = useState("");
  const [currentTemp, setCurrentTemp] = useState("Loading...");
  const [desiredTemp, setDesiredTemp] = useState("");
  const [statusMsg, setStatusMsg] = useState("");
  const [logs, setLogs] = useState([]);

  // Fetch the current temperature when aquariumID changes
  useEffect(() => {
    const getCurrentTemperature = async () => {
      if (!aquariumID) return; // Prevent API call if aquariumID is empty

      try {
        const response = await fetch(`${API_BASE_URL}/aquariums/${aquariumID}/current-temperature`);
        const data = await response.json();
        console.log("Fetched current temperature:", data); // Debug log
        setCurrentTemp(data.temperature);
      } catch (error) {
        console.error('Error fetching temperature:', error);
        setCurrentTemp('Error');
      }
    };

    getCurrentTemperature();
  }, [aquariumID]); // Dependency array ensures this runs when aquariumID changes

  const setTemperature = async () => {
    console.log("Set Temperature button clicked"); // Debug log
    if (!desiredTemp || !aquariumID) {
      setStatusMsg('Please enter both Aquarium ID and desired temperature.');
      return;
    }

    try {
      const response = await fetch(`${API_BASE_URL}/aquariums/${aquariumID}/thermostat/set-temperature`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ temperature: parseFloat(desiredTemp) }),
      });

      if (response.ok) {
        setStatusMsg(`Temperature set to ${desiredTemp} °C successfully.`);
        setCurrentTemp(desiredTemp);
      } else {
        const errorData = await response.json(); // Capture error message from backend
        setStatusMsg(`Failed to set temperature: ${errorData.detail || 'Unknown error'}`);
      }
    } catch (error) {
      setStatusMsg('Error communicating with the backend.');
      console.error('Error setting temperature:', error);
    }
  };

  const getTemperatureLogs = async () => {
    console.log("Get Temperature Logs button clicked"); // Debug log
    if (!aquariumID) {
      setStatusMsg('Please enter an Aquarium ID.');
      return;
    }

    try {
      const response = await fetch(`${API_BASE_URL}/aquariums/${aquariumID}/temperature-logs`);
      if (response.ok) {
        const logs = await response.json();
        console.log("Fetched logs:", logs); // Debug log
        setLogs(logs);
        setStatusMsg(''); // Clear status message if logs fetched successfully
      } else {
        const errorData = await response.json();
        setStatusMsg(`Failed to fetch logs: ${errorData.detail || 'Unknown error'}`);
      }
    } catch (error) {
      setStatusMsg('Error fetching temperature logs.');
      console.error('Error fetching temperature logs:', error);
    }
  };

  return (
    <div className="container"> {/* Add the container class */}
      <h1>Aquarium Thermostat Control</h1>

      {/* Input for Aquarium ID */}
      <label htmlFor="aquarium-id">Select Aquarium ID:</label>
      <input
        type="number"
        id="aquarium-id"
        value={aquariumID}
        onChange={(e) => setAquariumID(e.target.value)}
        placeholder="Enter Aquarium ID"
      />

      {/* Display current temperature */}
      <p>
        Current Temperature: <span>{currentTemp}</span> °C
      </p>

      {/* Input for desired temperature */}
      <label htmlFor="desired-temp">Set Desired Temp (°C):</label>
      <input
        type="number"
        id="desired-temp"
        value={desiredTemp}
        onChange={(e) => setDesiredTemp(e.target.value)}
        placeholder="Set Desired Temp (°C)"
        min="18"
        max="30"
        step="0.1"
      />

      {/* Button to Set Temperature */}
      <div className="button-container">
        <button onClick={setTemperature}>Set Temperature</button>
      </div>

      {/* Status Message */}
      <p>{statusMsg}</p>

      {/* Temperature Logs */}
      <h3>Temperature Logs</h3>
      <div className="button-container">
        <button onClick={getTemperatureLogs}>View Logs</button>
      </div>

      {/* List Temperature Logs */}
      <ul>
        {logs.length > 0 ? (
          logs.map((log, index) => (
            <li key={index}>
              Date: {log.timestamp}, Temp: {log.temperature} °C
            </li>
          ))
        ) : (
          <p>No logs found</p>
        )}
      </ul>
    </div>
  );
};

export default AquariumThermostat;
