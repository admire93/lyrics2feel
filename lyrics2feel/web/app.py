# -*- coding: utf-8 -*-
from flask import (Flask, render_template, request, json, redirect, url_for,
                   abort)
from sqlalchemy.exc import IntegrityError

from ..crawl import NmusicCrawler
from ..word import Lyrics
from ..db import session


app =  Flask(__name__)

@app.route('/', methods=['GET'])
def hi():
    return render_template('search.html')


@app.route('/search/', methods=['GET'])
def search():
    word = request.args.get('word', None)
    crawler = NmusicCrawler()
    search = []
    if word is not None:
        search = crawler.search(word)
    return render_template('search_result.html', search=search, dump=json.dumps)


@app.route('/song/<int:track_id>/', methods=['GET'])
def song(track_id):
    crawler = NmusicCrawler()
    lyrics = crawler.lyrics(track_id)
    return render_template('song.html', lyrics=lyrics)


@app.route('/song/', methods=['POST'])
def create_score():
    fields = set(['album', 'artist', 'track', 'lyrics', 'score'])
    diff = fields - set(request.form.keys())
    if diff:
        abort(400)
    l = Lyrics()
    for field in fields:
        setattr(l, field, request.form.get(field, None))
    session.add(l)
    try:
        session.commit()
    except IntegrityError as e:
        session.rollback()
        abort(500)
    return redirect(url_for('.hi'))
