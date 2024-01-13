const http = require('http');
const express = require('express');

const PORT = 5000;

const app = express();

app.get('/', (req, res) => {
    res.sendFile(__dirname + '/index.html');
});

app.get('/client.js', (req, res) => {
    res.sendFile(__dirname + '/client.js');
})

app.listen(PORT, () => {
    console.log(`Server is running on port ${PORT}`);
});