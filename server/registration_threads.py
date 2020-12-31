from threading import Thread
from queue import Queue
from database import UsersDb
from constants import ACTIVE, INACTIVE


# get table objects
db = UsersDb() # database object
db_conn = db.db_conn # database connection object
users_table = db.table('users') # users table object


class ActivationThread(Thread):
    """
    Activates account
    """

    def __init__(self):
        super().__init__(daemon=True)
        self.activation_queue = Queue()
        self.stop = False

    def add_to_queue(self, sid, data):
        """
        Adds data to the activation queue
        """
        self.activation_queue.put((sid, data))

    def activate(self):
        """
        Activates the account
        """
        sid, data = self.activation_queue.get()
        update_activation_status_query = users_table.update().where(users_table.c.sid==sid).values(activation_status=ACTIVE)
        db_conn.execute(update_activation_status_query)

    def run(self):
        """
        Effects the activation
        """
        while not self.stop:
            if not self.activation_queue.empty():
                self.activate()


class RegistrationThread(Thread):
    """
    Activates account
    """

    def __init__(self):
        super().__init__(daemon=True)
        self.registration_queue = Queue()
        self.stop = False

    def add_to_queue(self, data):
        """
        Adds data to the activation queue
        """
        self.registration_queue.put(data)

    def register(self):
        """
        Activates the account
        """
        operation, sid, email_address, username, password_hash, activation_code = self.registration_queue.get()
        if operation == 'update':
            update_user_query = users_table.update().where(users_table.c.email==email_address).values(email=email_address, username=username, password_hash=password_hash, sid=sid, activation_code=activation_code)
            db_conn.execute(update_user_query)
        else:
            insert_user_query = users_table.insert().values(email=email_address, username=username, password_hash=password_hash, sid=sid, activation_code=activation_code)
            db_conn.execute(insert_user_query)

    def run(self):
        """
        Effects the activation
        """
        while not self.stop:
            if not self.registration_queue.empty():
                self.register()