import collections
import datetime
import html
import json
import operator
import pandas as pd
import os

date = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")

if __name__ == "__main__":
    with open("chat_history.json") as json_file:

        full_chat_history = json.load(json_file)

        # Build up a dictionary, where the keys are usernames, and the values are a list of messages either sent or received from that user
        parsed_chat_history = collections.defaultdict(list)

        for chat_type in full_chat_history.keys():

            for chat in full_chat_history[chat_type]:

                # A chat object looks like:
                # {'From': '<user>', 'Media Type': 'TEXT', 'Created': '2022-07-22 19:28:21 UTC', 'Text': 'Hello World'}

                if chat_type.startswith("Received"):
                    username = chat['From']

                elif chat_type.startswith("Sent"):
                    username = chat['To']

                # To make sorting easier ...
                unix_timestamp_for_chat = int(datetime.datetime.strptime(
                    chat['Created'], "%Y-%m-%d %H:%M:%S %Z").timestamp())

                chat['Created-Timestamp'] = unix_timestamp_for_chat

                message_body = chat['Text']

                # Convert symbols like '&#39' into the actual character representation
                if (message_body is not None):
                    message_body = html.unescape(message_body)

                parsed_chat_history[username].append(chat)

        # Sort the messages for each user by timestamp,
        # and then dump them out to a JSON file
        for username in parsed_chat_history.keys():
            parsed_chat_history[username] = sorted(
                parsed_chat_history[username], key=operator.itemgetter('Created-Timestamp'))

            
            file_name_json = "snapchat-chat-history-{}.json".format(username)
            with open(file_name_json, 'w', encoding="utf-8") as output_json_file:
                # ensure_ascii=False to make emojis render correctly
                # https://stackoverflow.com/a/52206290/1576548
                json.dump(
                    parsed_chat_history[username], output_json_file, indent=4, ensure_ascii=False)
            
            with open(file_name_json, 'r', encoding="utf-8") as panda_reader_file:
           
                # asdfasdf = os.path.join(os.getcwd(), file_name_json)
                # print(f"filename: {asdfasdf}")
            
                frame = pd.read_json(panda_reader_file)
                frame.to_csv(file_name_json + '.csv', index=False)
            
            os.remove(file_name_json) 
                    
     

            
            
            
            
