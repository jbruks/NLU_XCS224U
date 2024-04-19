# messaging.py
import psycopg2
from psycopg2.extras import RealDictCursor


class Messaging:
    def __init__(self, db_config):
        self.db_config = db_config
        self.conn = psycopg2.connect(**db_config)
        self.conn.autocommit = True
        
        # Create a cursor object
        cur = self.conn.cursor()
        # Set the search path to your schema
        schema_name = 'sch01'
        cur.execute(f'SET search_path TO {schema_name}')
    def send_message(self, sender, receiver, content):
        """Send a message from a sender to a receiver, storing it in the database."""
        query = "INSERT INTO messages (sender, receiver, content, read) VALUES (%s, %s, %s, FALSE);"
        with self.conn.cursor() as cur:
            cur.execute(query, (sender, receiver, content))

    def read_message(self, receiver):
        """Retrieve a single unread message for a specific receiver and mark it as read."""
        message = None
        with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
            # Select the first unread message for the receiver
            cur.execute("SELECT * FROM messages WHERE receiver = %s AND read = FALSE ORDER BY timestamp ASC LIMIT 1;", (receiver,))
            message = cur.fetchone()
            if message:
                # Mark the retrieved message as read using its ID
                cur.execute("UPDATE messages SET read = TRUE WHERE id = %s;", (message['id'],))
        return message
