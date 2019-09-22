import json
from scraper import billboard_weeks

name = input('file name? ')

with open(name, 'w') as billboard:
    json.dump(billboard_weeks(), billboard, indent = 4)

