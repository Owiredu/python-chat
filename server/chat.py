import eventlet
from queue import Queue
import socketio
from pyisemail import is_email
from constants import (ACTIVE, CHAT_PORT, OFFLINE, STATUS_UPDATE, ONLINE, NORMAL, ERROR, SUCCESS, SERVER_NAME)
from database import db_conn, users_table


sio = socketio.Server() # socketio.Server(logger=True, engineio_logger=True)
app = socketio.WSGIApp(sio, static_files={
    '/': {'content_type': 'text/html', 'filename': 'server/templates/index.html'}
})

# track number of user connected
num_of_clients_connected = 0

# create the status update queue
status_update_queue = Queue()


@sio.event(namespace='/chat')
def connect(sid, environ):
    """
    Handle client connections 
    """
    # print connected user count
    global num_of_clients_connected    
    num_of_clients_connected += 1
    print('\n' + '-' * 30)
    print('Client disconnected:', sid)
    print('Number of clients connected:', num_of_clients_connected)
    print('-' * 30, '\n')


@sio.event(namespace='/chat')
def receive(sid, data):
    """
    Handle messages from clients
    """
    if data['msg_type'] == STATUS_UPDATE:
        if data['message'] == ONLINE:
            # update the status to online
            status_update_queue.put((sid, data['_from']['email'], ONLINE))
        else:
            # change the user's status to offline
            status_update_queue.put((sid, None, OFFLINE))
    if data['msg_type'] == NORMAL:
        # forward the message to the addressed recipient
        select_sid_query = users_table.select().where(users_table.c.email==data['to'])
        user_data = db_conn.execute(select_sid_query).fetchone()
        if user_data and user_data[8] == ACTIVE:
            if user_data[4] == ONLINE:
                sio.emit('receive', data, namespace='/chat', room=user_data[6])
            else:
                # TODO: store the message when the client is offline
                print(data['to'], 'is offline')


@sio.event(namespace='/chat')
def disconnect(sid):
    """
    Handle disconnection of clients
    """
    # change the user's status to offline
    status_update_queue.put((sid, None, OFFLINE))
    # print connected user count
    global num_of_clients_connected
    num_of_clients_connected -= 1
    print('\n' + '-' * 30)
    print('Client connected:', sid)
    print('Number of clients connected:', num_of_clients_connected)
    print('-' * 30, '\n')  


def update_connection_status():
    """
    Updates the connection status of a user
    """
    while True:
        sio.sleep(0)
        if not status_update_queue.empty():
            try:
                sid, email, new_status = status_update_queue.get()
                if new_status == ONLINE:
                    update_status_query = users_table.update().where(users_table.c.email==email).values(sid=sid, connection_status=new_status)
                    db_conn.execute(update_status_query)
                else:
                    update_status_query = users_table.update().where(users_table.c.sid==sid).values(sid=None, connection_status=new_status)
                    db_conn.execute(update_status_query)
            except Exception as e:
                print(e)
    

if __name__ == '__main__':
    sio.start_background_task(update_connection_status)
    eventlet.wsgi.server(eventlet.listen(('', int(CHAT_PORT))), app)