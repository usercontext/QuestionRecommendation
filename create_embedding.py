import json
import numpy as np
import allennlp
from allennlp.modules.elmo import Elmo, batch_to_ids
import numpy as np
import nltk
from nltk.tokenize import word_tokenize

options_file = "~/elmo_2x4096_512_2048cnn_2xhighway_options.json"
weight_file = "~/elmo_2x4096_512_2048cnn_2xhighway_weights.hdf5"

elmo = Elmo(options_file, weight_file, 1, dropout = 0)


with open("../category_article.json") as f:
    data = json.load(f)

def rec_embedding(data):
    embedding = np.zeros((1024,1))
    print(data["name"])
    for i in data["content"]:
        char_ids = batch_to_ids(word_tokenize(i["name"]))
        elmo_embedding = elmo(char_ids)
        embedding += elmo_embedding['elmo_representations'][0].detach().numpy().sum(axis = 1).sum(axis = 0).reshape(1024,1)
    embedding = np.divide(embedding, len(data["content"]))

    data["personal_embed"] = embedding.tolist()

    for i in data["children"]:
        rec_embedding(i)

rec_embedding(data)

with open('personal_embed_elmo.json', 'w') as f:
    import re
    output = json.dumps(data, indent=4)
    f.write(re.sub(r'(?<=\d),\s+', ', ', output))
