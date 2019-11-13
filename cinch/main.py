import nltk
#nltk.download('punkt')
from nltk.stem.lancaster import LancasterStemmer
stemmer = LancasterStemmer()
import numpy
import tflearn
import tensorflow
import random
import json
import pickle
import os
import ctypes,webbrowser, wikipedia, wolframalpha

client = wolframalpha.Client('J823UE-2GUVV5EYRG')

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
json_data = os.path.join(BASE_DIR, "cinch","intents.json")
pickle_data = os.path.join(BASE_DIR, "cinch","data.pickle")
with open(json_data) as file:
    data = json.load(file)

try:
    with open("./data.pickle","rb") as f:
        words, labels, training, output = pickle.load(f)
except:
    words = []
    labels = []
    docs_x = []
    docs_y =[]
    for intent in data["intents"]:
        for pattern in intent["patterns"]:
            wrds = nltk.word_tokenize(pattern)
            words.extend(wrds)
            docs_x.append(wrds)
            docs_y.append(intent["tag"])
            if intent["tag"] not in labels:
                labels.append(intent["tag"])
    words =[stemmer.stem(w.lower()) for w in words if w !=  "?"]
    words = sorted(list(set(words)))

    labels = sorted(labels)

    training = []
    output = []
    out_empty = [0 for _ in range(len(labels))]

    for x, doc  in enumerate(docs_x):
        bag = []
        wrds = [stemmer.stem(w) for w in doc]
        for w in words:
            if w in wrds:
                bag.append(1)
            else:
                bag.append(0)
        output_row = out_empty[:]
        output_row[labels.index(docs_y[x])] = 1

        training.append(bag)
        output.append(output_row)

    training = numpy.array(training)
    output = numpy.array(output)
    #print(words, labels, training, output)
    with open("data.pickle","wb") as f:
        pickle.dump((words, labels, training, output),f)
#tensorflow.reset_default_graph()
tensorflow.reset_default_graph()

net = tflearn.input_data(shape=[None, len(training[0])])
net = tflearn.fully_connected(net,8)
net = tflearn.fully_connected(net,8)
net = tflearn.fully_connected(net,len(output[0]), activation="softmax")
net = tflearn.regression(net)

model = tflearn.DNN(net)

try:
    model.load("cinch\\model.tflearn")
except:
    model.fit(training, output, n_epoch=1000,batch_size=8,show_metric=True)
    model.save("model.tflearn")

def bag_of_words(s,words):
    bag = [0 for _ in range(len(words))]
    s_words = nltk.word_tokenize(s)
    s_words = [stemmer.stem(word.lower()) for word in s_words]
    for se in s_words:
        for i, w in enumerate(words):
            if w == se:
                bag[i]= 1
    return numpy.array(bag)

def chat(dat):
    #print('start talking to bot:')
    dat = dat.lower()
    if 'lock my' in dat:
        ctypes.windll.user32.LockWorkStation()
        return "ok sir!"
    result = model.predict([bag_of_words(dat,words)])[0]
    result_index = numpy.argmax(result)
    tag = labels[result_index]
    print(result[result_index])
    if result[result_index] > 0.9489824:
        for taginjson in data["intents"]:
            if taginjson["tag"] == tag:
                responses = taginjson['responses']
                responses = random.choice(responses)
        return responses
    else:
        if 'open youtube' in dat:
            webbrowser.open('www.youtube.com')
            return "yo! enjoy opened youtube for u"
        elif 'open gmail' in dat:
            webbrowser.open('www.gmail.com')
            return "yo! enjoy opened gmail for u"
        elif 'stop music' in dat:
            os.system('TASKkILL /F /IM wmplayer.exe')
            os.system('TASKkILL /F /IM Music.UI.exe')
            return "umm k stoped music for you"
        elif 'play music' in dat:
            music= []
            webbrowser.open(random.choice(music))
            return 'Okay, here is your music! Enjoy!'
        elif 'change music' in dat:
            music= []
            webbrowser.open(random.choice(music))
            return 'Okay, changed music! Enjoy!'
        elif 'search' in dat:
            webbrowser.open(query[8:])
        elif 'shutdown' in dat:
            os.system('shutdown -s')
        else:
            query = dat
            try:
                try:
                    res = client.query(query)
                    results = next(res.results).text
                    return results

                except:
                    results = wikipedia.summary(query, sentences=2)
                    return results

            except:
                failtoserach = ["opps! sorry i missed it","umm! i haven't came accross such query","sorry i didn't get it"]
                return random.choice(failtoserach)
