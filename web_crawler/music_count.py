from utils import read_json

def sentiment_count(filename):
    lyrics = read_json(filename)
    classifications = {'pos': 0, 'neutral': 0, 'neg': 0}

    for lyric in lyrics:
        classifications[lyric['sentiment']] += 1

    print classifications