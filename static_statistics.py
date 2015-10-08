#!/usr/bin/env python
# vim: set fileencoding=utf8 :

"""Calculate data statistics from static pre-generated files."""

from __future__ import division
from os import walk
import sys
import stemmer as stm  # My stemmer functions


def calculate():
    stem_to_BNC = 0
    unstemmed_only_in_BNC = 0
    problem_words = []

    bnc_words = stm.load_bnc()
    invalid_token = stm.invalid_token

    print('BNC: ' + str(len(bnc_words)))

    mappings = map_load_kaggle()
    print('Mapping: ' + str(len(mappings)))

    total = len(mappings)
    done = 0
    for _, mapping in mappings.iteritems():
        for (original_word, stemmed_word) in mapping:
            if stemmed_word in bnc_words:
                stem_to_BNC += 1
            elif original_word in bnc_words:
                unstemmed_only_in_BNC += 1
            else:
                problem_words.append(original_word + ' ==> ' + stemmed_word)

        done += 1
        if done % 10 == 0:
            sys.stdout.write('\r' + str(done) + ' of ' + str(total))
            sys.stdout.flush()

    print('\nStem to BNC: ' + str(stem_to_BNC))
    print('Do not stem to BNC but are in BNC unstemmed: ' +
          str(unstemmed_only_in_BNC))
    print('Problem words: ' + str(len(problem_words)))


def map_load_kaggle():
    kaggle_words = {}
    temp_file_paths = []

    for (_, _, filenames) in walk(stm.esp_path + stm.stemmed_dir):
        temp_file_paths.extend(filenames)
        break

    for temp_file_path in temp_file_paths:
        original_kaggle_words = stm.file_to_bow(stm.esp_path +
                                                stm.original_dir +
                                                temp_file_path)
        stemmed_kaggle_words = stm.file_to_bow(stm.esp_path +
                                               stm.stemmed_dir +
                                               temp_file_path)

        mapping = zip(original_kaggle_words, stemmed_kaggle_words)

        kaggle_words[temp_file_path] = mapping

    return kaggle_words


def main():
    calculate()

if __name__ == '__main__':
    args = sys.argv

    main()
