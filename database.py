import sqlite3

DATABASE = "roxanne.db"
TABLES = [
    """CREATE TABLE IF NOT EXISTS conversations (
        id INTEGER PRIMARY KEY, 
        title TEXT NOT NULL DEFAULT 'New Conversation',
        created_at TEXT DEFAULT CURRENT_TIMESTAMP

    );
    """,
    """CREATE TABLE IF NOT EXISTS messages (
        id INTEGER PRIMARY KEY,
        convo_id INTEGER NOT NULL,
        role TEXT NOT NULL,
        content TEXT NOT NULL,
        timestamp TEXT DEFAULT CURRENT_TIMESTAMP,

        FOREIGN KEY (convo_id)
            REFERENCES conversations (id)
            ON DELETE CASCADE
    );
    """

]

# -----------------------
# Database Initialization
# -----------------------

def initialize_db():
    """
    Creating Database/tables if they don't exist
    """
    try:
        with sqlite3.connect(DATABASE) as connect:
            #Creating Database 
            cursor = connect.cursor()

            for table in TABLES:
                cursor.execute(table)

    except sqlite3.OperationalError as e:
        print("Error creating Database:", e)



# -----------------------
# Conversation Functions
# -----------------------

def create_conversation():
    """
    Creating a new conversation row
    returns the conversation ID
    """
    try:
        with sqlite3.connect(DATABASE) as connect:
            #Creating a new row
            cursor = connect.cursor()
            cursor.execute("INSERT INTO conversations DEFAULT VALUES")

            convo_id = cursor.lastrowid
            return convo_id

    except sqlite3.OperationalError as e:
        print("Error when adding new row in Conversations:", e)

def get_conversations():
    """
    Return a list of existing conversation in tables
    """

    toReturn = []

    try:
        with sqlite3.connect(DATABASE) as connect:
            #Fetching all rows
            cursor = connect.cursor()
            cursor.execute("SELECT * FROM conversations")

            rows = cursor.fetchall()
            for row in rows:
                toReturn.append(row)

            return toReturn

    except sqlite3.OperationalError as e:
        print("Error retrieving all rows from Conversations:", e)



def delete_conversation(conversation_id):
    """
    Delete a conversation and its messages
    """

    try:
        with sqlite3.connect(DATABASE) as connect:
            cursor = connect.cursor()

            #Then Deleting the conversation
            convo_sql_delete = """DELETE FROM conversations WHERE id = ?"""
            cursor.execute(convo_sql_delete, (conversation_id,))

    except sqlite3.OperationalError as e:
        print("Error when deleting conversation:", e)

def set_title(conversation_id, new_title):
    """
    Setting a new title for the conversation
    """

    try:
        with sqlite3.connect(DATABASE) as connect:
            cursor = connect.cursor()

            sql_query = """UPDATE conversations SET title = ? WHERE id = ?"""

            cursor.execute(sql_query, (new_title, conversation_id))

    except sqlite3.OperationalError as e:
        print("Error creating a new title:", e)

def get_title(conversation_id):
    """
    Retrieving the conversation title
    """
    try:
        with sqlite3.connect(DATABASE) as connect:
            cursor = connect.cursor()

            sql_query = """SELECT title FROM conversations WHERE id = ?"""

            cursor.execute(sql_query, (conversation_id,))

            title = cursor.fetchone()
            return title[0]

    except sqlite3.OperationalError as e:
        print("Error retreiving the title:", e)


# -----------------------
# Message Functions
# -----------------------

def save_message(conversation_id, role, content):
    """
    Save one user/assistant message within a conversation
    """
    try:
        with sqlite3.connect(DATABASE) as connect:
            #Creating a new message
            cursor = connect.cursor()

            sql_query = """INSERT INTO messages (convo_id, role, content) VALUES (?,?,?)"""
            message_data = (conversation_id, role, content)

            cursor.execute(sql_query, message_data)

    except sqlite3.OperationalError as e:
        print("Error when saving message:", e)

def get_messages(conversation_id):
    """
    Retrieving all messages within a conversation
    """

    try:
        with sqlite3.connect(DATABASE) as connect:
            #Selecting specific set of messages with specific conversation
            cursor = connect.cursor()

            sql_query = """SELECT role, content FROM messages WHERE convo_id = ? ORDER BY id ASC"""

            cursor.execute(sql_query, (conversation_id,))
            messages = cursor.fetchall()
            return messages

    except sqlite3.OperationalError as e:
        print(f"Error when retrieving messages from convo_{conversation_id}:", e)


# -----------------------
# Helper Functions
# -----------------------

def convert_to_database(msg_response):
    """
    Converts the msg from Ollama format to sqlite3 format
    """

    role = msg_response.message.role
    content = msg_response.message.content

    return role, content


def convert_to_ollama(convo_history):
    """
    Converts the conversation history from 
    get_conversation() to a usable form for Ollama to use
    """
    ol_convo_history = []

    for convo in convo_history:
        role, content = convo

        ol_convo_history.append({
            'role': role,
            'content': content,
        })

    return ol_convo_history


def check_title(conversation_id):
    """
    Checks if current conversation has a title or not
    """
    try:
        with sqlite3.connect(DATABASE) as connect:
            cursor = connect.cursor()

            sql_query = """SELECT title FROM conversations WHERE id = ?"""
            cursor.execute(sql_query, (conversation_id,))

            cur_title = cursor.fetchone()

            return cur_title[0] == "New Conversation"

    except sqlite3.OperationalError as e:
        print("Error when checking title:", e)
