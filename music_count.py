from utils import read_json

lyrics = read_json('database_min.json')
classifications = {'pos': 0, 'neutral': 0, 'neg': 0}

for lyric in lyrics:
    classifications[lyric['sentiment']] += 1

print classifications