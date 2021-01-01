from threading import Thread
from queue import Queue
from database import db_conn, users_table
from constants import OFFLINE, ONLINE


class StatusUpdateThread(Thread):
    """
    Updates the status to offline or online
    """

    def __init__(self):
        super().__init__(daemon=True)
        self.status_update_queue = Queue()
        self.stop = False

    def stop_thread(self):
        """
        Stops the status update thread
        """
        self.stop = True

    def add_to_queue(self, sid, email, new_status):
        """
        Add status data to the status queue
        """
        self.status_update_queue.put({'sid': sid, 'email': email, 'new_status': new_status})

    def set_status_offline(self, status_update_data):
        """
        Sets a user's status to offline
        """
        # make database changes
        update_status_query = users_table.update().where(users_table.c.sid==status_update_data['sid']).values(sid=None, connection_status=OFFLINE)
        db_conn.execute(update_status_query)

    def set_status_online(self, status_update_data):
        """
        Sets a user's status to online
        """
        # make database changes
        update_status_query = users_table.update().where(users_table.c.email==status_update_data['email']).values(sid=status_update_data['sid'], connection_status=ONLINE)
        db_conn.execute(update_status_query)

    def change_status(self):
        """
        Effects the appropriate changes to the status
        """
        status_update_data = self.status_update_queue.get()
        if status_update_data['new_status'] == OFFLINE:
            self.set_status_offline(status_update_data)
        else:
            self.set_status_online(status_update_data)

    def run(self):
        """
        Runs the thread
        """
        while not self.stop:
            if not self.status_update_queue.empty():
                self.change_status()