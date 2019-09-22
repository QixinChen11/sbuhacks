import json
import numpy as np
import tensorflow as tf
from tensorflow import keras

def training_data():
    f = input('Training data file? ')

    with open(f, 'r') as dataset:
        loaded = json.load(dataset)

        return loaded

    return None

songs = training_data()['songs']

half = len(songs) / 2

first = songs[1]['lyrics']

def encode():
    encoded = {}
    genres = {}
    r_encoded = {}
    r_genres = {}
    encode_lyrics = []
    genre_labels = []
    popular = []

    c = 0
    g = 0

    for song in songs:
        d = []
        lyrics = song['lyrics']

        if 'primary' not in song:
            continue

        genre = song['primary']
        genre_encoded = None

        if len(lyrics) == 0:
            continue

        if genre not in genres:
            genres[genre] = g
            r_genres[g] = genre
            g += 1

        genre_encoded = genres[genre]

        for lyric in lyrics:
            if lyric not in encoded:
                encoded[lyric] = c
                r_encoded[c] = lyric
                c += 1

            encoded_int = encoded[lyric]

            d.append(encoded_int)

        encode_lyrics.append(d)
        genre_labels.append(genre_encoded)
        popular.append(1 if int(song['p']) < 50 else 0)

    return {
        'r_encoded': r_encoded,
        'lyric_encoded': encoded,
        'r_genre': r_genres,
        'genre_encoded': genres,
        'lyrics': encode_lyrics,
        'genres': genre_labels,
        'hits': popular
    }

e = encode()

half = int(len(e['hits']) / 2)

training_lyrics = e['lyrics'][:half - 1]
testing_lyrics = e['lyrics'][half:]

train_data = keras.preprocessing.sequence.pad_sequences(training_lyrics, padding = 'post', maxlen = 30)
test_data = keras.preprocessing.sequence.pad_sequences(testing_lyrics, padding = 'post', maxlen = 30)

print(train_data)

train_labels = e['hits'][:half - 1]
test_labels = e['hits'][half:]

model = keras.Sequential()
model.add(keras.layers.Embedding(20000, 16))
model.add(keras.layers.GlobalAveragePooling1D())
model.add(keras.layers.Dense(16, activation = tf.nn.relu))
model.add(keras.layers.Dense(1, activation = tf.nn.sigmoid))

model.summary()

model.compile(optimizer = 'adam', loss = 'binary_crossentropy', metrics = ['acc'])

history = model.fit(train_data, train_labels, epochs = 100, batch_size = 512, validation_data = (test_data, test_labels), verbose = 1)

results = model.evaluate(test_data, test_labels)

with open('model.json', 'w') as model_json:
    model_json.write(model.to_json())

with open('model_encoded.json', 'w') as encoded_model:
    json.dump(e, encoded_model)

model.save_weights('model.h5')

print(results)
print('Done.')

