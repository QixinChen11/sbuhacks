import re
import string

def split_lyrics(lyrics):
    text = lyrics.strip()
    text = re.sub(r'\[[\w\s]+\]', '', text)
    text = text.strip(string.punctuation)

    words = text.split()

    final_words = []

    for word in words:
        final_word = word.strip(string.punctuation).strip()

        final_words.append(final_word)

    return words

