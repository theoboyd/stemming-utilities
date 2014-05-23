#!/usr/bin/env python
# vim: set fileencoding=utf8 :

"""Script to help with BNC-related tasks."""

from __future__ import division
from os import walk
import sys
#import profile
import stemmer  # My stemmer functions

# Printing labels with:
ts = u'{:35s}{:10,d}'   # Thousands separated numbers
fp = u'{:35s}{:10.3f}'  # Floating point numbers
ls = u'{:35s}{:s}'      # Lists

esp_path = '../KaggleData/ESPGame100k/'
wordlists_path = '../IntermediateWordLists/'


def load_files():
    original_file_names = []
    stemmed_file_names = []
    original_words = []
    stemmed_words = []
    bnc_words = []

    for (_, _, original_file_name) in walk(esp_path + 'labels/'):
        original_file_names.extend(original_file_name)

    for original_file_name in original_file_names:
        original_file = open(esp_path + 'labels/' + original_file_name)
        of_line = original_file.readline()  # Python doesn't have do-whiles
        while(of_line != ''):
            original_words.append(stemmer.clean_text(of_line))
            of_line = original_file.readline()
        original_file.close()

    for (_, _, stemmed_file_name) in walk(esp_path + 'labels-stemmed/'):
        stemmed_file_names.extend(stemmed_file_name)

    for stemmed_file_name in stemmed_file_names:
        stemmed_file = open(esp_path + 'labels-stemmed/' + stemmed_file_name)
        sf_line = stemmed_file.readline()
        while(sf_line != ''):
            stemmed_words.append(stemmer.clean_text(sf_line))
            sf_line = stemmed_file.readline()
        stemmed_file.close()

    # Only one file for all BNC words
    bnc_file = open(wordlists_path + 'wordsBNC.txt')
    bnc_line = bnc_file.readline()
    while(bnc_line != ''):
        bnc_words.append(stemmer.clean_text(bnc_line))
        bnc_line = bnc_file.readline()
    bnc_file.close()

    print('Traversed directories and loaded words.')
    return (original_words, stemmed_words, bnc_words)


def main():
    # Load in all Kaggle words, their stemmed versions and the BNC words
    (original_words, stemmed_words, bnc_words) = load_files()

    # Calculate unique sets of the above
    set_original_words = set(original_words)
    set_stemmed_words = set(stemmed_words)
    set_bnc_words = set(bnc_words)

    # Calculate and print statistics
    print(ts.format(u'All original Kaggle words: ', len(original_words)))
    print(ts.format(u'   unique: ', len(set_original_words)))
    print(ls.format(u'   unique examples: ', list(set_original_words)[1:8]))

    print(ts.format(u'All stemmed Kaggle words: ', len(stemmed_words)))
    print(ts.format(u'   unique: ', len(set_stemmed_words)))
    print(ls.format(u'   unique examples: ', list(set_stemmed_words)[1:8]))

    print(ts.format(u'All BNC words: ', len(bnc_words)))
    print(ts.format(u'   unique: ', len(set_bnc_words)))
    print(ls.format(u'   unique examples: ', list(set_bnc_words)[1:8]))

    original_intersection = set.intersection(set_original_words, set_bnc_words)
    print(ts.format(u'Unique original Kaggle \u2229 BNC: ',
                    len(original_intersection)))

    stemmed_intersection = set.intersection(set_stemmed_words, set_bnc_words)
    print(ts.format(u'Unique stemmed Kaggle \u2229 BNC: ',
                    len(stemmed_intersection)))

    diff = set_stemmed_words - stemmed_intersection
    print(ts.format(u'   not \u2229 BNC: ', len(diff)))
    print(ls.format(u'   examples: ', list(diff)[1:8]))

    # Percentage of all Kaggle words that do not stem down to BNC words
    original_not_in_intersection = [w for w in original_words
                                    if stem(w) not in stemmed_intersection]
    print(fp.format(u'% original Kaggle words not in \u2229: ', 100 *
                    len(original_not_in_intersection) / len(original_words)))
    set_original_not_in_intersection = set(original_not_in_intersection)
    print(ts.format(u'   unique: ', len(set_original_not_in_intersection)))
    save_temp('original_not_in_intersection', original_not_in_intersection)


def save_temp(file_name, string_list):
    temp_file = open(wordlists_path + file_name + '.txt', 'w+')
    temp_file.write('\n'.join(string_list))
    temp_file.close()


def stem(word):
    # Wrapper for the separate stemmer program
    stemmer_output = stemmer.stem_list([word])

    if len(stemmer_output) == 1:
        return stemmer_output[0]
    elif len(stemmer_output) == 0:
        # Word would be removed by stemmer; return null character which is not
        # in the test corpus
        return '\0'
    else:
        # Unexpected (serious) stemmer problem
        sys.stderr.write('Stemmer failure for input \'' + word + '\'.\n')
        sys.exit(-1)

if __name__ == '__main__':
    args = sys.argv
    main()
    #profile.run('main()')
