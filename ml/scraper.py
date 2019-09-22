import string
import csv
import re
import os
import ast
import ssl
import json
import requests
from bs4 import BeautifulSoup as BS
import urllib.request
import urllib.parse
import urllib.error
from datetime import date, timedelta
from urllib.request import Request, urlopen

from tools import split_lyrics

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

song_info = {
    'songs': []
}

def scrape_song(bsoup):
    song = {
        'lyrics': [],
        'genres': []
    }

    for metadata in bsoup.findAll('meta', attrs = { 'itemprop': 'page_data' }):
        data = metadata['content']
        data = re.sub(r'&quot;', '"', data)

        regex = re.search(r'("genres":\[(?:"[\w\s-]+",?)*\])', data)

        if regex:
            genres = regex.groups()[0]

            genres_str = f'{{ {genres} }}'
            genres_eval = ast.literal_eval(genres_str)['genres']

            song['genres'] = genres_eval

        primary_regex = re.search(r'\{"key":"Primary Tag","value":"([\w\s-]+)"\}', data)

        if primary_regex:
            primary = primary_regex.groups()[0]

            song['primary'] = primary

    for artist in bsoup.findAll('a', attrs = { 'class': 'header_with_cover_art-primary_info-primary_artist' }):
        song['artist'] = artist.text.strip()

    for genre in bsoup.findAll('a', attrs = { 'class': 'metadata_with_icon-link' }):
        print(f'Genre: {genre}')
        song['genres'].append(genre.text.strip())

    for div in bsoup.findAll('div', attrs = { 'class': 'lyrics' }):
        words_in_line = split_lyrics(div.text)

        for word in words_in_line:
            song['lyrics'].append(word.lower().strip(string.punctuation))

    return song

def scrape_start(url, title, peak):
    print(f'Scraping {url}')

    req = Request(url, headers = { 'User-Agent': 'Mozilla/5.0'  })
    page = requests.get(url)

    soup = BS(page.content, 'html5lib')
    html = soup.prettify('utf-8')

    scraped = scrape_song(soup)
    scraped['t'] = title
    scraped['p'] = peak

    song_info['songs'].append(scraped)

def create_genius_url(title, artist):
    artist = artist.lower()
    artist = re.sub(r'\'', '', artist)
    artist = re.sub(r'\s+', '-', artist)
    artist = artist.capitalize()
    artist = artist.strip(string.punctuation)

    title = title.lower()
    title = re.sub(r'\'', '', title)
    title = re.sub(r'\s+', '-', title)
    title = title.strip(string.punctuation)

    return f'http://genius.com/{artist}-{title}-lyrics'

def billboard_scraper(week = ''):
    print('Scraping billboard')

    url = 'http://billboard.com/charts/hot-100/' + week

    req = Request(url, headers = { 'User-Agent': 'Mozilla/5.0' })
    page = requests.get(url)

    soup = BS(page.content, 'html5lib')

    top_songs = soup.select('div.chart-list-item')

    songs = []

    for song in top_songs:
        song_name = song.find('span', { 'class': 'chart-list-item__title-text' }).text.strip()
        song_artist = song.find('div', { 'class': 'chart-list-item__artist' }).text.strip()
        song_peak = song.find('div', { 'class': 'chart-list-item__weeks-at-one' }).text.strip()

        print(f'Scraping {song_name}...')

        songs.append({
            'n': song_name,
            'a': song_artist,
            'p': song_peak,
            'g': create_genius_url(song_name, song_artist)
        })

    return songs

def billboard_weeks():
    start = date(2014, 5, 1)
    end = date.today()

    inc = timedelta(days = 30)

    songs = []

    while start < end:
        songs_of_week = billboard_scraper(str(start))

        songs.extend(songs_of_week)

        start += inc

    return songs

def start():
    billboard_file = input('File? ')

    with open(billboard_file, 'r') as billboard:
        songs = json.load(billboard)

        for song in songs:
            url = song['g']
            scrape_start(url, song['n'], song['p'])

    '''
    with open('targets', 'r') as csvs:
        csv_read = csv.reader(csvs, quotechar = '"', delimiter = ',')

        for row in csv_read:
            url = row[0]
            scrape_start(url)
    '''

    with open('data3.json', 'w') as out:
        json.dump(song_info, out)

    print('Scrape done')

if __name__ == '__main__':
    start()

