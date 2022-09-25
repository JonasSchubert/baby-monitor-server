const express = require('express');
const { useClimate } = require('./climate/route');
const { useStream } = require('./stream/route');

const app = express();
app.get('/', (_, response) => response.sendFile(__dirname + '/index.html'));
useClimate(app);
useStream(app);
app.listen(8000, ()=> console.log('Listening on port 8000!'));
