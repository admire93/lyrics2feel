""":mod:`lyrics2feel.crawl` --- crawl song's lyrics from nmusic.
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

"""
import urllib.request
import urllib.parse

import html5lib

from html5lib import treewalkers, treebuilders


class NmusicCrawler(object):
    """Crawl nmusic's information.
    """

    walker = treewalkers.getTreeWalker("dom")

    #: search url
    url = 'http://music.naver.com/search/search.nhn?query={}'.format

    #: lyrics url
    lyrics_url = 'http://music.naver.com/lyric/index.nhn?trackId={}'.format

    parser = html5lib.HTMLParser(tree=treebuilders.getTreeBuilder("dom"))

    def read_doc(self, url):
        """Read html document from given :param url: .

        :param url: url want to be readed.
        :return: html document.
        """
        r = urllib.request.urlopen(url)
        return self.parser.parse(r.read())


    def lyrics(self, nmusic_id):
        """Get lyrics.

        :param int nmusic_id: naver music id.
        :return: lyrics of :param nmusic_id: .
        :rtype: str
        """
        doc = self.read_doc(self.lyrics_url(nmusic_id))
        l = [
            ('lyrics', self.find_by_class(doc, 'div', 'show_lyrics')),
            ('track', self.find_by_class(doc, 'span', 'ico_play')),
            ('artist', self.find_by_class(doc, 'span', 'artist')),
            ('album', self.find_by_class(doc, 'span', 'album'))
        ]
        for i, (k, v) in enumerate(l[:]):
            l[i] = k, self.text(v).strip()
        return dict(l)


    def search(self, word):
        """Search naver music track id.

        :param str word: song's name or artist name want to search.
        :return: list of result.
        :rtype: list
        """
        l = []
        doc = self.read_doc(self.url(urllib.parse.quote(word)))
        div = self.find_by_class(doc, 'div', 'tracklist_table')
        if div:
            div = div[0]
        else:
            return []
        tr = self.find_by_class(div, 'tr', '_tracklist_move')
        for t in tr:
            trackdata = t.getAttribute('trackdata')
            title = self.find_by_class(t, 'a', '_title')
            artist = self.find_by_class(t, 'a', '_artist')
            album = self.find_by_class(t, 'a', '_album')
            title_txt = None
            artist_txt = None
            album_txt = None
            track_id = trackdata.split('|')[0]
            try:
                track_id = int(track_id)
                if title:
                    title_txt = self.text(
                        self.find_by_class(title[0], 'span', 'ellipsis')
                    ).strip()
                if artist:
                    artist_txt = self.text(
                        self.find_by_class(artist[0], 'span', 'ellipsis')
                    ).strip()
                if album:
                    album_txt = self.text(
                        self.find_by_class(album[0], 'span', 'ellipsis')
                    ).strip()
            except ValueError as e:
                track_id = None
            if all([title_txt, artist_txt, album_txt, track_id]):
                l.append({
                    'title': title_txt,
                    'artist': artist_txt,
                    'album': album_txt,
                    'track_id': track_id})
        return l


    def find_by_class(self, doc, elem, class_):
        r = []
        for n in doc.getElementsByTagName(elem):
            class_names = n.getAttribute('class').split(' ')
            if class_ in class_names:
                r.append(n)
        return r


    def text(self, doc):
        t = ''
        for x in doc:
            if x.nodeName == '#text':
                t += ' ' + x.nodeValue
            else:
                t += self.text(x.childNodes)
        return t
