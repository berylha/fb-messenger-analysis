import numpy as np
import pandas as pd
import os
import json
import datetime
from datetime import datetime
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


if len(chatlist) == 0:
    chatlist = os.listdir('count_group/')

# Generate pie charts of messages sent by each chat member
for chatname in chatlist:
    df = pd.read_csv('count_group/'+chatname, delim_whitespace=True)
    tot = np.sum(df.N)
    # Participant name only listed if participant sent >1% of messages
    # (otherwise plot is too cluttered)
    labels = [mem if df.N[i]>tot/100 else '' for i, mem in enumerate(df.member)]
    # Generate pie chart of chat participants
    plt.pie(df.N, labels=labels, rotatelabels=True)
    plt.title(chatname.replace('.dat',''), pad=70)
    plt.savefig('plots_group/'+chatname.replace('.dat','')+'.png', bbox_inches='tight')
    plt.close()
