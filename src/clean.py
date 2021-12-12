import json
import re


key_word_list = ["covid", "vaccination", "pfizer", "astra", "zeneca", "moderna", "janssen"]


# load the word at first
with open("../data/total_words.txt") as text_file:
    words_set = set({line.strip() for line in text_file})


def parse_links_and_images(raw_text):
    return re.sub(r'http\S+', '', raw_text)


def is_english(content):
    words = content.lower().split()
    count = 0
    # check for only five words
    for word in words:
        if word.lower() in words_set:
            count = count + 1
            if count > 7:
                return True
    return False


def contain_target(content):
    for word in words_set:
        if word in content.lower():
            return True
    return False


def extract_text(tweets):
    new_tweets = []
    for tweet in tweets:
        content = tweet["full_text"]
        content = parse_links_and_images(content)

        # remove some unicode annotations like \u201c
        string_encode = content.encode("ascii", "ignore")
        content = string_encode.decode()

        if is_english(content) and contain_target(content):
            new_tweets.append(content)
    return new_tweets


def filter_duplicates(tweets):
    new_tweets = []
    for tweet in tweets:
        if tweet not in new_tweets:
            new_tweets.append(tweet)
    print(len(new_tweets))
    return new_tweets


def save_json(data, file_name):
    # transform the data into intended format
    result = []

    for text in data:
        new_json = {"text": text, "topic": "", "sentiment": "negative"}
        result.append(new_json)

    with open("../data/annotated_" + file_name, "w") as f:
        json.dump(result, f, indent=4)
    print(len(data))


def clean_file(file_name, limit, date):
    with open("../data/" + file_name, "r") as file:
        tweets = json.load(file)["data"]
    tweets = extract_text(tweets)
    tweets = filter_duplicates(tweets)
    save_json(tweets[0:limit], str(date) + ".json")


def main():
    clean_file("raw_12_1.json", 400, 1)
    clean_file("raw_12_2.json", 300, 2)
    clean_file("raw_12_3.json", 300, 3)


if __name__ == "__main__":
    main()