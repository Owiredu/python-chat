import eventlet
import socketio

sio = socketio.Server() # socketio.Server(logger=True, engineio_logger=True)
app = socketio.WSGIApp(sio, static_files={
    '/': {'content_type': 'text/html', 'filename': 'server/index.html'}
})
num_of_clients_connected = 0
database = dict() # (phone[key], sid, status [whether online{connected} or offline{disconnected}], stored_messages_queue)

@sio.event(namespace='/chat')
def connect(sid, environ):
    global num_of_clients_connected
    num_of_clients_connected += 1
    print('\n', '-' * 30)
    print('Client connected:', sid)
    print('Number of clients connected:', num_of_clients_connected)
    print('-' * 30, '\n')


@sio.event(namespace='/chat')
def receive(sid, data):
    print('\n', '-' * 30)
    print('\nFROM:', sid, '\nMESSAGE: ', data)
    print('-' * 30, '\n')
    # sio.emit('receive', 'Server response', namespace='/chat', room=sid)


@sio.event(namespace='/chat')
def disconnect(sid):
    global num_of_clients_connected
    num_of_clients_connected -= 1
    print('\n', '-' * 30)
    print('Client disconnected:', sid)
    print('Number of clients connected:', num_of_clients_connected)
    print('-' * 30, '\n')
    

if __name__ == '__main__':
    eventlet.wsgi.server(eventlet.listen(('', 5000)), app)