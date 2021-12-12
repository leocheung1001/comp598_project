# this script is only for plotting data collection related figures
import json
import numpy as np
import matplotlib.pyplot as plt

# set width of bar
barWidth = 0.25
fig = plt.subplots(figsize=(12, 8))

# set height of bar
raw = [700, 700, 700]
processed = [578, 598, 577]
selected = [400, 300, 300]

# Set position of bar on X axis
br1 = np.arange(len(raw))
br2 = [x + barWidth for x in br1]
br3 = [x + barWidth for x in br2]

# Make the plot
plt.bar(br1, raw, width=barWidth,
        edgecolor='grey', label='Num of Raw Tweets')
plt.bar(br2, processed, width=barWidth,
        edgecolor='grey', label='Num of Available Tweets')
plt.bar(br3, selected, width=barWidth,
        edgecolor='grey', label='Num of Selected Tweets')

# Adding Xticks
plt.xlabel('Date', fontsize=15)
plt.ylabel('Number of tweets', fontsize=15)
plt.xticks([r + barWidth for r in range(len(raw))],
           ['December 1st', 'December 2nd', 'December 3rd'])
plt.title("Data cleaning in collection phase", fontsize=20)
plt.legend()
plt.show()
plt.savefig('../result/figures/data_collection.png')