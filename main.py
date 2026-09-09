import ollama_client as ol
import database as db

# -----------------------
# Helper Functions
# -----------------------

# def content_switch(new_convo_id):



# -----------------------
# Main Function
# -----------------------


def main():

    #Initialize the db
    db.initialize_db()

    #Create a new conversation
    convo_id = db.create_conversation()

    while True:

        #Retrieving User Input
        user_msg = input("YOU: ")
        print()

        #Control If Statements
        if user_msg == "/exit":
            break

        #Checking if title needs to be made
        if db.check_title(convo_id):  
            new_title = ol.create_title(user_msg)
            db.set_title(convo_id, new_title)

        
        

        #Saving User Message
        db.save_message(convo_id, "user", user_msg)

        #Retrieving conversation History
        convo_history = db.get_messages(convo_id)

        #Formatting the convo history
        ol_convo_history = db.convert_to_ollama(convo_history)

        #Sending History to Roxanne
        response = ol.send_msg(ol_convo_history)

        #Displaying Roxanne's response
        print("ROXANNE: ", response, end="\n")

        #Saving Roxanne's response
        db.save_message(convo_id, "assistant", response)


if __name__ == "__main__":
    main()