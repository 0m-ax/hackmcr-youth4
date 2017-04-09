var app = require('express')();
var server = require('http').Server(app);
var io = require('socket.io')(server);

server.listen(8080);

app.get('/', function (req, res) {
    res.sendfile(__dirname + '/index.html');
});

io.on('connection', function (socket) {
    socket.on('faces',(faces)=>{
        console.log(faces)
        var info = faces
            .filter((face)=>face.conf < 100)
            .map((match)=>{
                return {
                    "info":require('./photos/'+match.id+'/about.json'),
                    "id":match.id,
                    "conf":match.conf
                }
            })
            console.log(info)
        socket.broadcast.emit('faces-info',info)
    })
});