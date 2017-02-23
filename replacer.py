"""Replacement script for extending contractions"""
import re
from nltk.corpus import wordnet
# from nltk.metrics import edit_distance
# import enchant

replacement_patterns = [
    (r'won\'t', 'will not'),
    (r'can\'t', 'cannot'),
    (r'i\'m', 'i am'),
    (r'ain\'t', 'is not'),
    (r'(\w+)\'ll', '\g<1> will'),
    (r'(\w+)n\'t', '\g<1> not'),
    (r'(\w+)\'ve', '\g<1> have'),
    (r'(\w+)\'s', '\g<1> is'),
    (r'(\w+)\'re', '\g<1> are'),
    (r'(\w+)\'d', '\g<1> would'),
    (r'&gt;', '>'),
    (r'&lt;', '<'),
    (r'&amp', 'and'),
    (u'(\u00b4|\u2018|\u2019)', "'")
]


class RegexpReplacer(object):
    """ Replaces regular expression in a text.
    >>> replacer = RegexpReplacer()
    >>> replacer.replace("can't is a contraction")
    'cannot is a contraction'
    >>> replacer.replace("I should've done that thing I didn't do")
    'I should have done that thing I did not do'
    """

    def __init__(self, patterns=replacement_patterns):
        self.patterns = [(re.compile(regex), repl)
                         for (regex, repl) in patterns]

    def replace(self, text):
        s = text

        for (pattern, repl) in self.patterns:
            s = re.sub(pattern, repl, s)

        return s


class RepeatReplacer(object):
    """ Removes repeating characters until a valid word is found.
    >>> replacer = RepeatReplacer()
    >>> replacer.replace('looooove')
    'love'
    >>> replacer.replace('oooooh')
    'ooh'
    >>> replacer.replace('goose')
    'goose'
    """

    def __init__(self):
        self.repeat_regexp = re.compile(r'(.)\1{2,}')
        self.repl = r'\1\1\1'

    def replace(self, word):
        if wordnet.synsets(word) is True:
            return word
        else:
            repl_word = self.repeat_regexp.sub(self.repl, word)
            if repl_word != word:
                return self.replace(repl_word)
            else:
                return repl_word


class ComboReplacer(object):
    """ Replacer with both RegexpReplacer and RepeatReplacer capabilities
    """

    def __init__(self):
        self.regexp = RegexpReplacer()
        self.repeat = RepeatReplacer()

    def replaceRepeat(self, word):
        return self.repeat.replace(word)

    def replaceRegex(self, word):
        return self.regexp.replace(word)

    def replaceAll(self, word):
        return self.replaceRegex(self.replaceRepeat(word))
