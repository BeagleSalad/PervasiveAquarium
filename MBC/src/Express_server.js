const express = require('express');
const { Pool } = require('pg');
const cors = require('cors');
const bodyParser = require('body-parser');

const app = express();
const port = 8000;

// PostgreSQL connection pool
const pool = new Pool({
    user: 'postgres',
    host: 'localhost',
    database: 'aquarium_db',
    password: 'Kvbopf860a',
    port: 5432,
});

// Middleware
app.use(cors());
app.use(bodyParser.json());

// Get current temperature
app.get('/aquariums/:id/current-temperature', async (req, res) => {
    const aquariumId = parseInt(req.params.id);
    try {
        const result = await pool.query(
            'SELECT temperature FROM temperatures WHERE aquarium_id = $1 ORDER BY recorded_at DESC LIMIT 1',
            [aquariumId]
        );
        res.json({ temperature: result.rows[0]?.temperature || null });
    } catch (error) {
        console.error(error);
        res.status(500).json({ detail: 'Error fetching current temperature' });
    }
});

// Set new temperature
app.post('/aquariums/:id/thermostat/set-temperature', async (req, res) => {
    const aquariumId = parseInt(req.params.id);
    const { temperature } = req.body;

    try {
        await pool.query('INSERT INTO temperatures (aquarium_id, temperature) VALUES ($1, $2)', [aquariumId, temperature]);
        res.status(201).json({ detail: 'Temperature set successfully' });
    } catch (error) {
        console.error(error);
        res.status(500).json({ detail: 'Error setting temperature' });
    }
});

// Get temperature logs
app.get('/aquariums/:id/temperature-logs', async (req, res) => {
    const aquariumId = parseInt(req.params.id);
    try {
        const result = await pool.query('SELECT * FROM temperature_logs WHERE aquarium_id = $1 ORDER BY timestamp DESC', [aquariumId]);
        res.json(result.rows);
    } catch (error) {
        console.error(error);
        res.status(500).json({ detail: 'Error fetching logs' });
    }
});

// Start the server
app.listen(port, () => {
    console.log(`Server running at http://localhost:${port}`);
});
