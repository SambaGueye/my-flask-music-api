from urllib.request import Request
from flask import Flask, render_template, send_file
import pandas as pd
import urllib
import matplotlib.pyplot as plt
import io
import seaborn as sns
# import 

app = Flask(__name__)


def get_genres(df):
    genres = df['genre'].unique()

    genres_music = []
    for genre in genres:
        val = genre.split(',')
        for i in val:
            if i not in genres_music:
                genres_music.append(i)
    return genres_music


df = pd.read_csv('dataset.csv')

@app.route('/')
def exercice2():
    genres_music = get_genres(df)
    # return render_template('test.html')
    return render_template('exercice2.html', genres=genres_music)

@app.route('/api/items/<genre>/<artiste>/<trier_par>', methods=['GET'])
def getInfos(genre, artiste, trier_par):
    df = pd.read_csv('dataset.csv')
    genre = df.genre == genre
    artist_name = df.artist_name==artiste
    sort_by = trier_par


    df = df.loc[genre & artist_name][:20].reset_index()
    df = df.sort_values(by=sort_by, ascending=False).to_dict('record')
    return df



@app.route('/plot/<score>/<artiste>')
def plot(score, artiste):
    df = pd.read_csv('dataset.csv')
    artist_name = df.artist_name==artiste
    df = df.loc[artist_name].reset_index()
    fig = plt.figure()
    sns.histplot(data=df, x=score, hue=df.genre, multiple="stack")
    img = io.BytesIO()
    fig.savefig(img, format='png')
    img.seek(0)

    return send_file(img, mimetype='image/png')



if __name__=='__main__':
    app.run(port=4001, debug=True)