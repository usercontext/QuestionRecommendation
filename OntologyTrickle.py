
# coding: utf-8

# In[2]:


import json
import pandas as pd
import allennlp
from allennlp.modules.elmo import Elmo, batch_to_ids
import numpy as np
import nltk
import scipy.spatial
from nltk.tokenize import word_tokenize
with open('avg_embed_text.json') as f:
    data = json.load(f)

import spacy
nlp = spacy.load('en_core_web_lg')

quora_dataset = pd.read_csv('/Users/sharadchitlangia/Downloads/questions.csv')
quora_dataset.head()

options_file = "~/elmo_2x4096_512_2048cnn_2xhighway_options.json"
weight_file = "~/elmo_2x4096_512_2048cnn_2xhighway_weights.hdf5"

elmo = Elmo(options_file, weight_file, 1, dropout=0)


def elmo_embed(sentence):
    char_ids = batch_to_ids(word_tokenize(sentence))
    elmo_embedding = elmo(char_ids)
    embedding = elmo_embedding['elmo_representations'][0].detach().numpy().sum(axis = 1).sum(axis = 0).reshape(1024,1)
    return embedding


def embed(sentence):
    return nlp(sentence).vector


def cosine_similarity(embedding1, embedding2):
    return (1 - scipy.spatial.distance.cosine(embedding1, embedding2))


def ontology_trickle(hierarchy, query):
    if hierarchy['name'] == 'Hobbies and Crafts':
        query = embed(query)
    if hierarchy['children']:
        total, count = 0, 0
        cosines = []
        for child in hierarchy['children']:
            child_cosine = cosine_similarity(child['avg_embed'], query)
            print(child['name'], child_cosine)
            # print(child['name'], child_cosine)
            cosines.append(child_cosine)
            total += 1
            if cosine_similarity(query, hierarchy['personal_embed']) >= child_cosine:
                count += 1
        child_idx = cosines.index(max(cosines))
        print("Personal Embed Cosine : ", cosine_similarity(query, hierarchy['personal_embed']))
        print("Max Child Embed Cosine : ", cosines[child_idx], hierarchy["children"][child_idx]["name"])
        print(hierarchy['children'][child_idx]['name'], cosines[child_idx])
        if total == count:
            print(hierarchy['name'])
            # return hierarchy['name']
            exit
        elif total != count:
            ontology_trickle(hierarchy['children'][child_idx], query)
    else:
        return hierarchy['name']


for i in range(1, 2000, 10):
    print('\n')
    print(quora_dataset.iloc[i][3])
    ontology_trickle(data['children'][0], quora_dataset.iloc[i][3])
    print('\n')


def set_embed(data):
    for i in data['children']:
        if 'avg_embed' not in i.keys():
            i['avg_embed'] = i['personal_embed']
        if i['children']:
            set_embed(i)


data['children'][0]['children'][0]['key_words']
cosine_similarity(embed("Photography click instagram image flickr film tap camera"), embed("Photography"))

ontology_trickle(data['children'][0], "Design and build a laser cut computer case with")

data['children'][0]['children'][1]['key_words']
cosine_similarity(data['children'][0]['children'][3]['avg_embed'], embed('Artificial Intelligence'))
set_embed(data['children'][0])
with open("../category_article.json") as f:
    articles = json.load(f)
