const express = require('express');
const { Pool } = require('pg');
const app = express();
const port = 4000;

// Enable JSON parsing for incoming requests
app.use(express.json());

// Database configuration
const pool = new Pool({
    user: process.env.USER,
    host: 'localhost',
    database: 'myappdb',
    port: 5432,
});

// Test database connection
pool.query('SELECT NOW()', (err, res) => {
    if (err) {
        console.error('Database connection error:', err);
    } else {
        console.log('Database connected successfully');
    }
});

// Basic routes for testing
app.get('/', (req, res) => {
    res.send('<html><body style="background: white;"><h1>Server is running with Database!</h1></body></html>');
});

// Example API endpoints
app.post('/api/users', async (req, res) => {
    try {
        const { name, email } = req.body;
        const result = await pool.query(
            'INSERT INTO users (name, email) VALUES ($1, $2) RETURNING *',
            [name, email]
        );
        res.json(result.rows[0]);
    } catch (err) {
        res.status(500).json({ error: err.message });
    }
});

app.get('/api/users', async (req, res) => {
    try {
        const result = await pool.query('SELECT * FROM users');
        res.json(result.rows);
    } catch (err) {
        res.status(500).json({ error: err.message });
    }
});

app.post('/api/posts', async (req, res) => {
    try {
        const { user_id, title, content } = req.body;
        const result = await pool.query(
            'INSERT INTO posts (user_id, title, content) VALUES ($1, $2, $3) RETURNING *',
            [user_id, title, content]
        );
        res.json(result.rows[0]);
    } catch (err) {
        res.status(500).json({ error: err.message });
    }
});

app.get('/api/posts', async (req, res) => {
    try {
        const result = await pool.query(`
            SELECT posts.*, users.name as author_name 
            FROM posts 
            JOIN users ON posts.user_id = users.id
        `);
        res.json(result.rows);
    } catch (err) {
        res.status(500).json({ error: err.message });
    }
});

app.listen(port, () => {
    console.log(`Server running at http://localhost:${port}`);
});
