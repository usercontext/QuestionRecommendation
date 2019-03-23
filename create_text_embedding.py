import json
import numpy as np
# import allennlp
# from allennlp.modules.elmo import Elmo, batch_to_ids
# import nltk
# from nltk.tokenize import word_tokenize
import sklearn
from sklearn.feature_extraction.text import TfidfVectorizer
import spacy
nlp = spacy.load('en_core_web_lg')

# options_file = "~/elmo_2x4096_512_2048cnn_2xhighway_options.json"
# weight_file = "~/elmo_2x4096_512_2048cnn_2xhighway_weights.hdf5"

# elmo = Elmo(options_file, weight_file, 1, dropout=0)


with open("/Users/sharadchitlangia/Desktop/Projects/UserContext/TaskHierarchy138K/scraped_data.json") as f:
    data = json.load(f)
    

def get_desc(content, to_return="string"):
    """
    Takes value from content key in each node

    Input: list of json articles

    Returns: A Corpus of articles in the format of a list. A single
    article is one concatenated sentence consisting of all the sentences
    """
    if to_return == "string":
        articles = ""
    elif to_return == "list":
        articles = []
    for i, i_element in enumerate(content):
        article = ""
        for n, section_values in (i_element['meta']['sections'].items()):
            for m, step_values in (section_values['steps']).items():
                article += step_values['title']
                article += " "
                article += step_values['desc']
                article += " "

        if to_return == "string":
            articles += article
        elif to_return == "list":
            articles.append(article)
    return articles


def get_top_n_words(articles, n):
    vectorizer = TfidfVectorizer(stop_words='english')
    X = vectorizer.fit_transform(articles)
    vocab = dict((v, k) for k, v in vectorizer.vocabulary_.items())
    top_5 = [X.toarray()[i].argsort()[-1*n:][::-1] for i in range(X.shape[0])]
    words = [[vocab[idx] for idx in top_5_article] for top_5_article in top_5]
    return words


def get_same_level_articles(data):
    articles = []
    for i in data:
        article = get_desc(i["content"], to_return="string")
        articles.append(article)
    return articles


def set_top_n_words(X, data, n, vocab):
    for i, element in enumerate(data):
        top_n_idx = X.toarray()[i].argsort()[-1*n:][::-1]
        top_n_words = [vocab[idx] for idx in top_n_idx]
        data[i]["key_words"] = top_n_words


def rec_embedding(data):
    embedding = np.zeros(300)
    print(data["name"])
    if data["name"] == "Hobbies and Crafts":
        n = 10
        articles = get_desc(data["content"], to_return="list")
        vectorizer = TfidfVectorizer(stop_words='english')
        X = vectorizer.fit_transform(articles)
        vocab = dict((v, k) for k, v in vectorizer.vocabulary_.items())
        top_n_idx = [X.toarray()[i].argsort()[-1*n:][::-1] for i in range(X.shape[0])]
        top_n_words = [[vocab[idx] for idx in top_idx] for top_idx in top_n_idx]
        embedding += sum([sum([nlp(i).vector for i in top_n]) for top_n in top_n_words])
    if 'key_words' in data.keys():
        for i in data['key_words']:
            embedding += nlp(i).vector
    data["personal_embed"] = embedding.tolist()

    if data['children']:
        articles = get_same_level_articles(data["children"])
        if data['name'] == "Drawing Patterns and Prints":
            print(articles)
        vectorizer = TfidfVectorizer(stop_words='english')
        X = vectorizer.fit_transform(articles)
        vocab = dict((v, k) for k, v in vectorizer.vocabulary_.items())
        set_top_n_words(X, data["children"], 10, vocab)
    for i in data["children"]:
        rec_embedding(i)


rec_embedding(data['children'][0])
# tls = get_top_n_words(articles_hbc, 10)
# print(tls)
# articles_hbc = get_desc(hbc_content)
# vectorizer = TfidfVectorizer(stop_words='english')
# X = vectorizer.fit_transform(articles_hbc)
# vocab = dict((v,k) for k, v in vectorizer.vocabulary_.items())
# stop = vectorizer.stop_words_
# top_5 = X.toarray()[1].argsort()[-10:][::-1]
# for i, element in enumerate(top_5):
#     print(vocab[element])
# rec_embedding(data)

with open('personal_embed_text.json', 'w') as f:
    import re
    output = json.dumps(data, indent=4)
    f.write(re.sub(r'(?<=\d),\s+', ', ', output))
# data['children'][0]['children'][1]['key_words']
