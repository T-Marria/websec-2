const express = require("express");
const app = express();
const port = 3000;
const path = require('path');

app.use(express.static(__dirname));

app.get('/', function(request, response) {
    response.sendFile(__dirname + '/index.html');
});

app.get('/groups', function(request, response) {
	response.sendFile(__dirname + '/GroupsInfo.json');
});

app.get('/teachers', function(request, response) {
	response.sendFile(__dirname + '/TeachersInfo.json');
});

app.get('/schedule', function(request, response) {
	response.sendFile(__dirname + '/Schedule.json');
});

const server = app.listen(port, (error) => {
    if (error) return console.log(`Error: ${error}`);
    console.log(`Server listening on port ${server.address().port}`);
    console.log(`http://localhost:${port}`)
}); 