#!/usr/bin/env python
# vim: set fileencoding=utf8 :

"""Produce plottable data to determine whether stemming is useful."""

from __future__ import division
from collections import Counter
import sys
import stemmer as stm  # My stemmer functions
import bnc_calculator


def create_frequency_plots():
    #bnc_words = stm.load_bnc()
    original_kaggle_words = stm.load_kaggle(False)
    print('Loaded ' + str(len(original_kaggle_words)) + ' original words')
    stemmed_kaggle_words = stm.load_kaggle(True)
    print('Loaded ' + str(len(stemmed_kaggle_words)) + ' stemmed words')

    # Plot two lines of points
    original_points = []
    stemmed_points = []

    original_kaggle_size = len(original_kaggle_words)

    # Tally up words in the Kaggle corpus and sort by frequency decreasing
    original_kaggle_tally = Counter(original_kaggle_words).most_common()
    stemmed_kaggle_tally = Counter(stemmed_kaggle_words).most_common()

    accumulator = 0
    freq_accumulator = 0
    for _, word_freq in original_kaggle_tally:
        # Percentage of Kaggle corpus covered by this word
        freq_accumulator += word_freq
        percentage = freq_accumulator / original_kaggle_size

        # Number of tokens so far
        accumulator += 1
        #number_of_tokens = math.pow(accumulator, 2)

        # Plottable (x,y) point
        original_points.append((accumulator, percentage))

    accumulator = 0
    freq_accumulator = 0
    for _, word_freq in stemmed_kaggle_tally:
        # Percentage of Kaggle corpus covered by this word
        freq_accumulator += word_freq
        percentage = freq_accumulator / original_kaggle_size

        # Number of tokens so far
        accumulator += 1
        #number_of_tokens = math.pow(accumulator, 2)

        # Plottable (x,y) point
        stemmed_points.append((accumulator, percentage))

    return (original_points, stemmed_points)


def points_to_mathematica(xy_tuple_list, prefix=''):
    # Produces output in the form of two lists, xx and yy such that we can plot
    # and further manipulate them in Mathematica using:
    # ListPlot[{{x, y}, {x, y}, ...}]

    coords_string = prefix + 'xy = {'
    limit = len(xy_tuple_list)
    count = 0

    for (x, y) in xy_tuple_list:
        count += 1
        coords_string += '{Internal`StringToDouble["' + str(x) + \
                         '"], Internal`StringToDouble["' + str(y) + '"]}'
        if count < limit:
            coords_string += ', '

    coords_string += '};'

    return coords_string


def main():
    (original_points, stemmed_points) = create_frequency_plots()

    bnc_calculator.save_temp('stemming_benefit_lines',
                             [points_to_mathematica(original_points),
                              points_to_mathematica(stemmed_points, 's')])
    print('Saved')

if __name__ == '__main__':
    args = sys.argv

    main()
