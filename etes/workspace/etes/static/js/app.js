//Middleware
var express = require('express');
var app = express();

app.set('port', 3000);

/**
	Req = Request
	Res = Response
**/
app.get('/', function(req, res) {
	console.log('GET the homepage');
	res.send("EXPRESS YOURSELF");
});

var server = app.listen(app.get('port'), function() {
	var port = server.address().port; //gets the port number
	console.log("Magic happens on port " + port);
}); //port 3000 of Mean Stack server
console.log("Me first!")