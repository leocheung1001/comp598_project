import json
import re
import math
from collections import defaultdict


topics = {
    "p": "legal and policy",
    "v": "vaccination experience",
    "i": "infected experience",
    "o": "opinions to vaccine",
    "c": "opinions to covid",
    "t": "third party",
}

sentiments = {
    "p": "positive",
    "m": "neutral",
    "n": "negative",
}


def process_line(line, stopwords):
    line = line.lower()
    line = re.sub(r"[()\[\],-.?!:;#&\ ]+", " ", line)
    tokens = line.strip().split(' ')
    clean_tokens = [t for t in tokens if re.match(r'[^\W\d]*$', t)]
    clean_tokens = list(filter(lambda x: x not in stopwords, clean_tokens))
    return clean_tokens


def get_word_count(data, stopwords):
    res = {p: dict() for p in topics.keys()}
    total_wc = defaultdict(lambda: 0)
    sentiment_res = {p: 0 for p in sentiments.values()}
    combined_res = {p: {"positive": 0, "neutral": 0, "negative": 0} for p in topics.values()}
    topic_count = {p: 0 for p in topics.values()}

    for row in data:
        topic = row['topic']
        sentiment = row['sentiment']
        text = row['text'].lower()
        lst = process_line(text, stopwords)
        for l in lst:
            if l not in res[topic]:
                res[topic][l] = 0
            topic_count[topics[topic]] += 1
            res[topic][l] += 1
            sentiment_res[sentiments[sentiment]] += 1
            combined_res[topics[topic]][sentiments[sentiment]] += 1
            total_wc[l] += 1
    filtered_res = {p: dict() for p in topics.keys()}
    for p in topics.keys():
        for key, item in res[p].items():
            if total_wc[key] >= 5:
                filtered_res[p][key] = item
    return filtered_res, sentiment_res, combined_res, topic_count


def tf_idf(wc, length=15):
    num = len(topics)

    word_usage = defaultdict(lambda: 0)
    for p in topics.keys():
        for key in wc[p].keys():
            word_usage[key] += 1

    res = {p: [] for p in topics.keys()}
    for p in topics.keys():
        for key, tf in wc[p].items():
            idf = math.log(num / word_usage[key])
            tf_idf = tf * idf
            res[p].append([-tf_idf, key])

    for p in topics.keys():
        res[p].sort()
        res[p] = res[p][:min(length, len(res[p]))]
        res[p] = [x[1] for x in res[p]]

    return res


if __name__ == '__main__':
    with open('../data/stopwords.txt') as f:
        stopwords = [line.rstrip() for line in f]
        stopwords = list(filter(lambda x: x[0] != '#', stopwords))

    with open('../data/annotated.json') as f:
        data = json.load(f)

    data, sentiment_count, topic_and_sentiment, topic_count = get_word_count(data, stopwords)
    res = tf_idf(data)
    topic_top_10 = {p: dict() for p in topics.values()}
    for topic, words in res.items():
        topic_top_10[topics[topic]] = words
    # print(f"top 10 tfidf words by topic: {topic_top_10}")
    with open('../result/tfidf_topic.json', 'w') as f:
        json.dump(topic_top_10, f, indent=4)
    with open('../result/sentiment_count.json', 'w') as f:
        json.dump(sentiment_count, f, indent=4)
    with open('../result/topic_and_sentiment.json', 'w') as f:
        json.dump(topic_and_sentiment, f, indent=4)
    with open('../result/topic_count.json', 'w') as f:
        json.dump(topic_count, f, indent=4)
