import json

def top5():
    with open('model_encoded.json', 'r') as data_file:
        data = json.load(data_file)

        r_lyric = data['r_encoded']
        lyric_dict = data['lyric_encoded']
        r_genre = data['r_genre']
        genre_dict = data['genre_encoded']

        all_lyrics = data['lyrics']
        genres = data['genres']

        frequencies = {}

        for lyrics in all_lyrics:
            for lyric in lyrics:
                if lyric not in frequencies:
                    frequencies[lyric] = 1
                else:
                    frequencies[lyric] += 1

        ordered = []

        for key, value in sorted(frequencies.items(), key = lambda item: item[1]):
            ordered.append((r_lyric[f'{key}'], value))

        ordered.reverse()

        freqs = {}

        for genre in genres:
            if genre not in freqs:
                freqs[genre] = 1
            else:
                freqs[genre] += 1

        ordered_genre = []

        for key, value in sorted(freqs.items(), key = lambda item: item[1]):
            ordered_genre.append((r_genre[f'{key}'], value))

        ordered_genre.reverse()

        return {
            'lyrics': ordered[25:1000],
            'genres': ordered_genre
        }

print(top5())

