"""Replacement script for extending contractions"""
import re
from nltk.corpus import wordnet
from nltk.metrics import edit_distance
import enchant

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
    (r'(\w+)\'d', '\g<1> would')
]


def replaceApostrophe(text):
    """ Replaces language contractions by displaying their full form
        """
    patterns = [(re.compile(regex), repl)
                for (regex, repl) in replacement_patterns]
    for (pattern, repl) in patterns:
        replaced = re.sub(pattern, repl, text)
    return replaced


def replaceRepeat(word):
    """ Shorten words with repeating letters
    """
    repeat_regexp = re.compile(r'(\w*)(\w)\2(\w*)')
    repl = r'\1\2\3'
    if wordnet.synsets(word):
        return word
    repl_word = repeat_regexp.sub(repl, word)
    if repl_word != word:
        return replaceRepeat(repl_word)
    else:
        return repl_word


def replaceSpelling(word, dict_name='en', max_dist=2):
    """ Replaces misspelled words with a likely suggestion based on shortest
    edit distance.
    NOTE: pyenchant C library issue, not using
    """
    spell_dict = enchant.Dict(dict_name)
    if spell_dict.check(word):
        return word
    suggestions = spell_dict.suggest(word)
    if suggestions and edit_distance(word, suggestions[0]) <= max_dist:
        return suggestions[0]
    else:
        return word
