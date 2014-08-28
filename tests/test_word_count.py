from re import split

from lyrics2feel.word import word_count


def test_simple_word():
    a = '''
    foo     foo
    foo bar bar ha ha
    '''
    splited = [x for x in split('\s*', a) if x != '']
    assert ['foo', 'foo', 'foo', 'bar', 'bar', 'ha', 'ha'] == splited


def test_l_word_count():
    a = '''
    foo     foo
    foo bar bar ha ha
    '''
    count = word_count(a)
    expect = {'foo': 3, 'bar': 2, 'ha': 2}
    assert expect == dict(count)
