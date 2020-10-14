import numpy as np
import pandas as pd
import os
import csv
import json
import datetime
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

# CHOOSE PLOTS HERE #######################
line_plot_all_no_legend = True
line_plot_top_n = True
# if above is set to True, set n here:
n = 10
pie_chart = True
###########################################

################################################################################


# Setting directory to find message data
# IMPORTANT: make sure you have extracted the folder into the same location as
# this file, or change the directory so it points to the correct location.
dir = 'messages/inbox/'
if len(chatlist) == 0:
    chatlist = os.listdir(dir)

# Initialize pandas dataframe
df = pd.DataFrame(columns=['correspondent', 'timestamp', 'sender'])

# Iterate through chats
for chatfolder in chatlist:
    chatname = chatfolder.split('_')[0]
    all_files = os.listdir(dir + chatfolder)
    # Ensure that this chat has text-based messages
    files = [f for f in all_files if f.startswith('message')]
    if len(files) == 0:
        continue
    print('Extracting data from ' + chatname)
    # Iterate through JSON files
    for filename in files:
        i_init = len(df)
        data = json.load(open(dir + chatfolder + '/' + filename, 'r'))
        # Ensure that chat is direct message, not group chat
        if len(data['participants']) > 2:
            continue
        # Iterate through and count messages
        for i, message in enumerate(data['messages']):
            correspondent = data['participants'][0]['name']
            timestamp = datetime.datetime.fromtimestamp(message['timestamp_ms']/1000).strftime('%Y-%m-%d %H:%M:%S')
            sender = message['sender_name']
            df.loc[i_init + i] = [correspondent, timestamp, sender]

# Counts by correspondent and timeframe
alltime = np.array([datetime.datetime.strptime(t, '%Y-%m-%d %H:%M:%S').date() for t in df.timestamp])
tarr = pd.date_range(min(alltime), max(alltime)+datetime.timedelta(days=7), freq='1W')
counts = pd.DataFrame(columns=['correspondent', *tarr])
counts['correspondent'] = list(set(df.correspondent))
counts.set_index('correspondent', inplace=True)
counts.fillna(0, inplace=True)
for row in df.iloc:
    dt = datetime.datetime.strptime(row.timestamp, '%Y-%m-%d %H:%M:%S')
    i = 0
    while tarr[i] < dt:
        i += 1
    col = tarr[i-1]
    counts[col][row.correspondent] += 1

# Sort by total
sums = [np.sum(row) for row in counts.iloc]
counts['sum'] = sums
counts.sort_values(by=['sum'], ascending=False, inplace=True)
sorted_sums = list(counts['sum'])
tot = np.sum(sorted_sums)
counts.drop('sum', axis=1, inplace=True)



# Generating plots
print('GENERATING PLOTS')

tt = [datetime.datetime.strftime(t, '%Y-%m-%d') for t in counts.columns]
interval = int(len(tt)/12)

# LINE PLOT FOR ALL DATA WITH NO LEGEND
if line_plot_all_no_legend:
    print('Generating line plot for all data with no legend')
    fig, ax = plt.subplots(dpi=270)
    for row in counts.iloc:
        ax.plot(tt, list(row))
    ax.set_ylabel('Messages per week')
    ax.set_xticks(tt[::interval])
    ax.set_xticklabels([t.strip(':0') for t in tt[::interval]], rotation=60)
    fig.tight_layout()
    plt.savefig('lineplot_nolegend.png')
    plt.close()

# LINE PLOT FOR n MOST MESSAGED PEOPLE
if line_plot_top_n:
    print('Generating line plot for n most messaged individuals')
    fig, ax = plt.subplots(dpi=270)
    top_n = counts.head(n)
    for row in top_n.iloc:
        ax.plot(tt, list(row), label=row.name)
    ax.set_ylabel('Messages per week')
    ax.legend(loc='upper left')
    ax.set_xticks(tt[::interval])
    ax.set_xticklabels([t.strip(':0') for t in tt[::interval]], rotation=60)
    fig.tight_layout()
    plt.savefig('lineplot_top_n.png')
    plt.close()

# PIE CHART
if pie_chart:
    print('Generating pie chart')
    labels = [row.name if sorted_sums[i]>tot/100 else '' for i, row in enumerate(counts.iloc)]
    plt.pie(sorted_sums, labels=labels, rotatelabels=True)
    plt.savefig('pie_chart.png', bbox_inches='tight')
    plt.close()
