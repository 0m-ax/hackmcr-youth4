#!/usr/bin/python
from socketIO_client import SocketIO, LoggingNamespace

with SocketIO('localhost', 8080, LoggingNamespace) as socketIO:
    socketIO.emit('faces',[
        {
            "id":1,
            "conf":5
        },
        {
            "id":2,
            "conf":4.1
        }
    ])