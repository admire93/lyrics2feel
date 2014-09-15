# -*- coding: utf-8 -*-
from math import ceil

from flask import (Flask, render_template, request, json, redirect, url_for,
                   abort)
from sqlalchemy.exc import IntegrityError

from ..crawl import NmusicCrawler
from ..word import Lyrics, Word
from ..db import session


app =  Flask(__name__)


def pager(current, len_, lim):
    page_len = int(ceil(len_ / float(lim)))
    for i in range(1, page_len + 1):
        if i == current:
            r = (i, 'c')
        elif i == 1:
            r = (i, 'f')
        elif page_len == i:
            r = (i, 'e')
        elif (current - 4) < i < (current + 4):
            r = (i, 'n')
        else:
            continue
        yield r


def bind_page(post_per_page=15):
    page = request.args.get('page', 1, type=int)
    o = (page - 1) * post_per_page
    return page, o, post_per_page


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


@app.route('/word_counts/', methods=['GET'])
def word_count():
    page, offset, limit = bind_page()
    q = session.query(Word)\
        .order_by(Word.word)
    wc = q\
         .offset(offset)\
         .limit(limit)\
         .all()
    return render_template('word_count.html',
                           wc=wc,
                           pages=pager(page, q.count(), limit))
