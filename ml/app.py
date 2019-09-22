import json
from flask import Flask, jsonify, request
from flask_cors import CORS
import tensorflow as tf
from keras.models import model_from_json
import numpy as np

from tensorflow.python.keras.backend import set_session
from tools import split_lyrics
from data import top5

global sess
global graph
sess = tf.Session()
graph = tf.get_default_graph()

app = Flask(__name__)

CORS(app)

model_json_open = open('model.json', 'r')
model_json = model_json_open.read()
model_json_open.close()

set_session(sess)
loaded = tf.keras.models.model_from_json(model_json)
loaded.load_weights('model.h5')

@app.route('/predict', methods = ['GET', 'POST'])
def predict():
    with open('encoded.json') as encoded:
        lyrics = request.json['lyrics']

        en = json.load(encoded)

        le = en['lyric_encoded']
        ge = en['genre_encoded']
        hits = en['hits']

        split = split_lyrics(lyrics)
        encoded_lyrics = []
        nonencoded = []

        for lyric in split:
            if lyric in le:
                encoded_lyrics.append(le[lyric])
                nonencoded.append(lyric)

        print(encoded_lyrics)
        print(nonencoded)

        # padding = tf.keras.preprocessing.sequence.pad_sequences(encoded_lyrics, padding = 'post', maxlen = 30)

        with graph.as_default():
            set_session(sess)
            p = loaded.predict(np.array([encoded_lyrics]))
            number = float(p[0][0])

            return {
                'n': number
            }

    return None

@app.route('/top', methods = ['GET'])
def lyrics():
    return top5()

app.run()

