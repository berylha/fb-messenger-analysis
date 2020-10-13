import numpy as np
import pandas as pd
import os
import json
import matplotlib.pyplot as plt
from cycler import cycler


#### SPECIFY SETTINGS HERE: ####################################################

# If you would like plots made only for specific chats, specify them here:
# (Otherwise default will be all)
chatlist = []

# Setting style for plots; change fonts, colors if desired
plt.rcParams['font.family'] = 'serif'
plt.rcParams['axes.prop_cycle'] = cycler('color', ['#2364aa', '#3da5d6',
            '#73bfb8', '#fec601', '#ea7317', '#f0f465', '#fab3a9', '#ed6b86',
            '#a62639', '#db324d'])
################################################################################


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
    print('Extracting data from ' + chatname)
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

    # Now plot the pie chart
    print('Plotting' + chatname)
    tot = np.sum(df.N)
    # Participant name only listed if sent >1% of messages
    # (otherwise plot is too cluttered)
    labels = [mem if df.N[i]>tot/100 else '' for i, mem in enumerate(df.member)]
    # Generate pie chart of chat participants
    plt.pie(df.N, labels=labels, rotatelabels=True)
    plt.title(chatname, pad=70)
    fig_name = 'plots_group/' + chatname + '.png'
    plt.savefig(fig_name, bbox_inches='tight')
    plt.close()
