#!/usr/bin/env python3
from flask import Flask, send_from_directory
from flask_sockets import Sockets

app = Flask(__name__)
sockets = Sockets(app)

clients = []

@sockets.route('/echo')
def echo_socket(ws):
    print("Hey cool a client")
    clients.append(ws)
    while not ws.closed:
        message = ws.receive()
        for client in clients:
            if client is not ws:
                try:
                    client.send(message)
                except:
                    print("Found a dead client")

    clients.remove(ws)


@app.route('/')
def hello():
    return 'Hello world!'

@app.route('/app')
def send_app():
    return send_from_directory('static', 'index.html')

@app.route('/app/<path:path>')
def send_static(path):
    return send_from_directory('static', path)

@app.after_request
def add_header(r):
    r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    r.headers["Pragma"] = "no-cache"
    r.headers["Expires"] = "0"
    r.headers['Cache-Control'] = 'public, max-age=0'
    return r


if __name__ == "__main__":
    from gevent import pywsgi
    from geventwebsocket.handler import WebSocketHandler
    server = pywsgi.WSGIServer(('', 5005), app, handler_class=WebSocketHandler)
    server.serve_forever()
