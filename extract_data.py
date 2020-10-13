import numpy as np
import pandas as pd
import os
import json

print('Counting number of messages from each person in each chat')

# Setting directory to find message data
# IMPORTANT: make sure you have extracted the folder into the same location as
# this file, or change the directory so it points to the correct location.
dir = 'messages/inbox/'

# Iterate through chats
for chatfolder in os.listdir(dir):
    chatname = chatfolder.split('_')[0]
    all_files = os.listdir(dir + chatfolder)

    # Ensure that this chat has text-based messages
    files = [f for f in all_files if f.startswith('message')]
    if len(files) == 0:
        continue
    print('    Extracting ' + chatname)

    # Define dictionary to store data
    data = {'participants': [], 'messages': []}

    # Iterate through JSON files; chats with >10000 messages have multiple
    for filename in files:
        data_new = json.load(open(dir + chatfolder + '/' + filename, 'r'))
        if len(data['participants']) == 0:
            data['participants'] = data['participants'] + data_new['participants']
        data['messages'] = data['messages'] + data_new['messages']
    senders = np.array([x['sender_name'] for x in data['messages']])

    # Move data to pandas dataframe
    df = pd.DataFrame(columns=['member','N'])
    # Count number of messages sent by each chat member
    for i, p in enumerate(data['participants']):
        df.loc[i] = [p['name'], np.sum(senders==p['name'])]
    # Sort by number of messages
    df = df.sort_values(by=['N'], ignore_index=True)

    # Determine which folder to save to depending on if 2-person or group chat
    if len(data['participants']) <= 2:
        to_save = 'count_single/' + chatname.replace('.json','') + '.dat'
    else:
        to_save = 'count_group/' + chatname.replace('.json','') + '.dat'
    # Save file as CSV
    df.to_csv(to_save, index=False, sep=' ')

print('Finished extracting data')
