import matplotlib.pyplot as plt
import numpy as np
import json
import csv


def plot_table():
    with open("../result/tfidf_topic_filtered.json") as f:
        res = json.load(f)

    with open('../result/tfidf_topic.csv', 'w', encoding='UTF8') as f:
        w = csv.writer(f)
        w.writerow(list(res.keys()))
        w.writerows(list(zip(*res.values())))


def plot_topic_dist():
    with open("../result/topic_count.json") as f:
        data = json.load(f)
    topics = list(data.keys())
    d = list(data.values())
    cmap = plt.get_cmap("tab20c")
    colors = cmap(np.arange(6))

    def func(pct, allvalues):
        absolute = int(pct / 100. * np.sum(allvalues))
        return "{:.1f}%\n({:d})".format(pct, absolute)

    # Creating plot
    fig, ax = plt.subplots(figsize=(10, 7))
    ax.pie(d, colors=colors, autopct=lambda pct: func(pct, d), labels=topics, startangle=90, textprops={'fontsize': 15})
    plt.title('Tweet count by topic', fontsize=35)
    plt.savefig('../result/figures/topic_pie_chart.png')


def plot_sentiment_dist():
    with open("../result/sentiment_count.json") as f:
        data = json.load(f)
    topics = list(data.keys())
    d = list(data.values())
    cmap = plt.get_cmap("tab20c")
    colors = cmap(np.arange(3))

    def func(pct, allvalues):
        absolute = int(pct / 100. * np.sum(allvalues))
        return "{:.1f}%\n({:d})".format(pct, absolute)

    # Creating plot
    fig, ax = plt.subplots(figsize=(10, 7))
    ax.pie(d, colors=colors, autopct=lambda pct: func(pct, d), labels=topics, startangle=90, textprops={'fontsize': 15})
    plt.title('Tweet count by sentiment', fontsize=35)
    plt.savefig('../result/figures/sentiment_pie_chart.png')


def plot_topic_and_sentiment():
    with open("../result/topic_and_sentiment.json") as f:
        res = json.load(f)
    # set width of bar
    barWidth = 0.25
    fig = plt.subplots(figsize=(20, 15))

    # set height of bar
    positive = [res[k]['positive'] for k in res.keys()]
    neutral = [res[k]['neutral'] for k in res.keys()]
    negative = [res[k]['negative'] for k in res.keys()]

    cmap = plt.get_cmap("tab20c")
    colors = cmap(np.arange(3))

    # Set position of bar on X axis
    br1 = np.arange(len(positive))
    br2 = [x + barWidth for x in br1]
    br3 = [x + barWidth for x in br2]

    # Make the plot
    plt.bar(br1, positive, color=colors[0], width=barWidth,
            edgecolor='grey', label='positive')
    plt.bar(br2, neutral, color=colors[1], width=barWidth,
            edgecolor='grey', label='neutral')
    plt.bar(br3, negative, color=colors[2], width=barWidth, label='negative')

    # Adding Xticks
    plt.xlabel('Topic', fontsize=25)
    plt.ylabel('Number of tweets', fontsize=25)
    plt.xticks([r + barWidth for r in range(len(positive))], list(res.keys()), fontsize=20, rotation=15, ha='right')
    plt.yticks(fontsize=20)

    plt.title('Tweet count by sentiment for each topic', fontsize=30)
    plt.legend(prop={"size":20})
    plt.savefig('../result/figures/topic_and_sentiment_bar_chart.png')


if __name__ == '__main__':
    plot_table()
    plot_topic_dist()
    plot_sentiment_dist()
    plot_topic_and_sentiment()
