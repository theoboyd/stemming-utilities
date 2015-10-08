#!/usr/bin/env python
# vim: set fileencoding=utf8 :

"""Generate a list of most common words for use in COALS calculations."""

from __future__ import division
from collections import Counter
import sys
import stemmer as stm  # My stemmer functions
import bnc_calculator

usage_string = 'Usage: create_word_file.py size:<suffix>'
file_arg = "_"
count_arg = 0


def create_word_file(words_limit):
    kaggle_words = stm.load_kaggle(False)
    bnc_words = stm.load_bnc()

    print('Loaded Kaggle: ' + str(len(kaggle_words)))

    # Remove invalid/junk placeholder (used for statistics) and words not in
    # the BNC
    kaggle_words = [word for word in kaggle_words if (word in bnc_words) and
                    (word != stm.invalid_token)]

    # Tally up the whole list of words
    kaggle_tally = Counter(kaggle_words)

    # Get 'n' most common (n is words_limit)
    top_tallies = kaggle_tally.most_common(count_arg)
    top_words = [top_tally[0] for top_tally in top_tallies]

    return top_words


def main():
    word_list = create_word_file(count_arg)

    bnc_calculator.save_temp('words' + file_arg, word_list)
    print('Saved words' + file_arg)


def fail():
    print(usage_string)
    sys.exit()

if __name__ == '__main__':
    args = sys.argv

    for arg in args[1:]:
        if 'size:' in arg:
            try:
                file_arg = arg[5:].replace('000000', 'm').replace('000', 'k')
                count_arg = int(arg[5:])
            except ValueError:
                fail()
        else:
            print('Wrong argument: ' + arg)
            fail()

    main()
