#!/usr/bin/env python
# vim: set fileencoding=utf8 :

"""Stems bag of word descriptor files and saves their stemmed versions."""

import re
import sys
from os import walk
from collections import defaultdict
#from stemming.porter import stem as porter_stem
#from stemming.porter2 import stem as porter2_stem
#from stemming.lovins import stem as lovins_stem
from stemming.paicehusk import stem as paicehusk_stem
from nltk.stem.wordnet import WordNetLemmatizer

#TODO: see http://www.nltk.org/howto/wordnet.html
#from nltk.corpus import wordnet


run_size = 100000
usage_string = 'Usage: stemmer.py [nosave] [size:<integer>]'

# Acceptable words that don't otherwise match our valid word regex
valid_exceptions = ['mp3', 'mp3 player', 'mp3 players', '911', '9/11']

conflations = {'desktop': 'desk',
               'wallpaper': 'wall',
               'mp3': 'CD player',
               'mp3 player': 'CD player',
               'mp3 players': 'CD player',
               '9/11': '911',
               'mom': 'mother'}
misspellings = {'tounge': 'tongue'}

stop_words = ['a', 'aboard', 'about', 'above', 'across', 'after', 'against',
              'ago', 'albeit', 'all', 'along', 'alongside', 'although',
              'always', 'am', 'amid', 'among', 'amongst', 'an', 'and', 'any',
              'anybody', 'anyhow', 'anyone', 'anything', 'anytime', 'anyway',
              'anywhere', 'are', 'around', 'as', 'astride', 'at', 'atop', 'be',
              'because', 'been', 'before', 'behind', 'being', 'below',
              'beneath', 'beside', 'besides', 'between', 'beyond', 'billion',
              'billionth', 'both', 'but', 'by', 'can', 'cannot', 'could', 'de',
              'despite', 'did', 'do', 'does', 'doing', 'done', 'down',
              'during', 'each', 'eight', 'eighteen', 'eighteenth', 'eighth',
              'eightieth', 'eighty', 'either', 'eleven', 'eleventh', 'en',
              'enough', 'et', 'every', 'everybody', 'everyone', 'everything',
              'everywhere', 'except', 'few', 'fewer', 'fifteen', 'fifteenth',
              'fifth', 'fiftieth', 'fifty', 'first', 'five', 'for', 'fortieth',
              'forty', 'four', 'fourteen', 'fourteenth', 'fourth', 'from',
              'had', 'has', 'have', 'he', 'her', 'here', 'hers', 'herself',
              'him', 'himself', 'his', 'how', 'hundred', 'hundredth', 'i',
              'if', 'in', 'inside', 'into', 'is', 'it', 'its', 'itself',
              'least', 'less', 'lest', 'like', 'little', 'many', 'may', 'me',
              'might', 'million', 'millionth', 'mine', 'minus', 'more', 'most',
              'much', 'must', 'my', 'myself', 'near', 'neither', 'never',
              'next', 'nine', 'nineteen', 'nineteenth', 'ninetieth', 'ninety',
              'ninth', 'no', 'nobody', 'none', 'nor', 'not', 'nothing',
              'notwithstanding', 'now', 'nowhere', 'of', 'off', 'on', 'one',
              'oneself', 'onto', 'opposite', 'or', 'our', 'ours', 'ourselves',
              'out', 'outside', 'over', 'par', 'past', 'per', 'plus', 'post',
              'second', 'seven', 'seventeen', 'seventeenth', 'seventh',
              'seventieth', 'seventy', 'shall', 'she', 'should', 'since',
              'six', 'sixteen', 'sixteenth', 'sixth', 'sixtieth', 'sixty',
              'so', 'some', 'somebody', 'somehow', 'someone', 'something',
              'sometime', 'somewhere', 'ten', 'tenth', 'than', 'that', 'the',
              'their', 'theirs', 'them', 'themselves', 'then', 'there',
              'these', 'they', 'third', 'thirteen', 'thirteenth', 'thirtieth',
              'thirty', 'this', 'those', 'though', 'thousand', 'thousandth',
              'three', 'through', 'throughout', 'til', 'till', 'times', 'to',
              'too', 'toward', 'towards', 'twelfth', 'twelve', 'twentieth',
              'twenty', 'two', 'under', 'underneath', 'unless', 'unlike',
              'until', 'unto', 'up', 'upon', 'us', 'versus', 'via', 'vs',
              'was', 'we', 'were', 'what', 'when', 'where', 'whereas',
              'whether', 'which', 'while', 'who', 'whom', 'whose', 'why',
              'will', 'willing', 'with', 'within', 'without', 'worth', 'would',
              'yes', 'yet', 'you', 'your', 'yours', 'yourself', 'yourselves',
              'zero']

delta_statistics = defaultdict(int)
bow_statistics = defaultdict(int)
pre_stemmed_words = set()
post_stemmed_words = set()
wordnet_lemmatiser = WordNetLemmatizer()
save_results = True


def stem_files(bow_file_directory, pre_stemmed_folder, post_stemmed_folder):
    all_bow_file_paths = []
    for (_, _, filenames) in walk(bow_file_directory + pre_stemmed_folder):
        all_bow_file_paths.extend(filenames)
        break

    print('Found ' + str(len(all_bow_file_paths)) + ' files to stem at ' +
          bow_file_directory + pre_stemmed_folder + '.')
    print('Stemming ' + str(run_size) + ' of them.')
    if save_results:
        print('Stemmed files will be saved to ' + bow_file_directory +
              post_stemmed_folder + '.')
    else:
        print('Debug run, not saving.')

    for bow_file_path in all_bow_file_paths[:run_size]:
        stem_file(bow_file_directory + pre_stemmed_folder + bow_file_path,
                  bow_file_directory + post_stemmed_folder + bow_file_path)


def file_to_bow(file_path):
    bow = []  # Bag of words

    bow_file = open(file_path)
    bow_line = clean_text(bow_file.readline())

    while(bow_line != ''):
        bow.append(bow_line)
        bow_line = clean_text(bow_file.readline())

    bow_file.close()

    return bow


def bow_to_file(file_path, bow):
    # Create handle to output file
    bow_file = open(file_path, 'w')

    for word in bow:
        bow_file.write('%s\n' % word)

    bow_file.close()


def remove_affix_punc_and_nums(word):
    # Remove prefix and postfix punctuation as it adds no meaning ('person.' is
    # equivalent to 'person' but 'google.com' has meaning in its own right)
    # Also remove prefix and postfix numbers to ease conflation for the stemmer
    word = re.sub(r'^[0-9 \-\.\'\?\!]*', '', word)
    word = re.sub(r'[0-9 \-\.\'\?\!]*$', '', word)
    return word


def is_valid(word, regex):
    if (word in valid_exceptions) or (len(regex.findall(word)) == 1):
        return True


def clean_urls_and_whitespace(word):
    # Clean url fragments, leaving only the meaningful domain
    word = re.sub(r'\.com', '', word)
    word = re.sub(r'\.', ' ', word)

    # Remove any whitespace that was reintroduced due to these or earlier
    # replacements
    word = word.strip()
    return word


def stem_file(input_file_path, output_file_path):
    # Read in the unstemmed bag of words from file
    bow = file_to_bow(input_file_path)

    stemmed_bow = stem_list(bow)

    # Save the stemmed bag of words file
    if save_results:
        bow_to_file(output_file_path, stemmed_bow)

    # Update statistics
    delta = len(stemmed_bow) - len(bow)
    delta_statistics[delta] += 1
    bow_statistics[len(bow)] += 1

    pre_stemmed_words.update(bow)
    post_stemmed_words.update(stemmed_bow)


def stem_list(input_list):
    stemmed_bow = input_list

    # Lowercase the words and remove trailing whitespace
    stemmed_bow = [word.lower().strip() for word in stemmed_bow]

    # Remove junk words such as numbers and symbols
    # The regex only allows lowercase alphabetic characters (since we've
    # ensured they are all lowercase already) and possibly spaces, hyphens and
    # apostrophes and dots if after the first character
    # Because the regex is so strict, first remove affixed dots and numbers
    valid_regex = re.compile(r'^[a-z][a-z \-\'\.]*$')
    stemmed_bow = [remove_affix_punc_and_nums(word) for word in stemmed_bow]
    stemmed_bow = [word for word in stemmed_bow if is_valid(word, valid_regex)]

    # Remove all dots and clean urls in words
    stemmed_bow = [clean_urls_and_whitespace(word) for word in stemmed_bow]

    # Replace a few words the stemmer doesn't handle and for better alignment
    # with the corpus
    stemmed_bow = [conflations[word] if word in conflations else word
                   for word in stemmed_bow]

    # Correct some obvious spelling errors -- manual list
    stemmed_bow = [misspellings[word] if word in misspellings else word
                   for word in stemmed_bow]

    # Remove stop words (such as 'the' and 'and')
    stemmed_bow = [word for word in stemmed_bow if word not in stop_words]

    # Lemmatise the words: this uses WordNet's corpus to clean the data
    #
    # For example, this will conflate word pairs such as leaf/leaves which
    # otherwise stem to leaf/leav with most standard stemmers
    stemmed_bow = [wordnet_lemmatiser.lemmatize(word) for word in stemmed_bow]
        #if (word[-1] == 'v') and ((word[:-1] + 'f') in raw_stemmed_bow):

    # Next, stem the words
    stemmed_bow = [stem_word(word) for word in stemmed_bow]

    stemmed_bow = sorted(list(set(stemmed_bow)))  # Merge stemming duplicates

    return stemmed_bow


def clean_text(source):
    return source.replace('\n', '').replace('\r', '').replace('\0', '')


def stem_word(word):
    # First run a (slightly modified) Paice-Husk stemmer

    #stem it
    #if in bnc then done
    #but if not in bnc then, is unstemmeed in bnc, good
    #   if unstemmed is also not in bnc, then it's a problem word

     #if it's a problem word that has quite a lot of it, fix maybe

    stemmed_word = paicehusk_stem(word)

    # If the stemmer failed to stem the word, return the original
    if len(stemmed_word) < 1:
        return word

    return stemmed_word

if __name__ == '__main__':
    args = sys.argv

    for arg in args:
        if arg == 'nosave':
            save_results = False
        elif 'size:' in arg:
            try:
                run_size = int(arg[5:])
            except ValueError:
                print(usage_string)
                sys.exit()

    stem_files('KaggleData/ESPGame100k/', 'labels/', 'labels-stemmed/')
    delta_stats = dict(delta_statistics).items()
    print(sorted(delta_stats))
    bow_stats = dict(bow_statistics).items()
    print(sorted(bow_stats))
    print('Pre-stemmed unique words: ' + str(len(pre_stemmed_words)))
    print('Post-stemmed unique words: ' + str(len(post_stemmed_words)))
