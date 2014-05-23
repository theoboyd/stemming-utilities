#!/usr/bin/env python
# vim: set fileencoding=utf8 :

"""Produce plottable data to determine whether stemming is useful."""

from __future__ import division
from collections import Counter
import math
import sys
import stemmer as stm  # My stemmer functions
import bnc_calculator

usage_string = 'Usage: stemming_benefit.py [size:<integer>]'
stemming_jump = 0


def create_frequency_plots():
    # For speed when debugging, we may skip every j words and only keep some
    # for stemming
    j = 1
    if stemming_jump > 1:
        j = stemming_jump

    bnc_words = stm.load_bnc()
    original_kaggle_words = stm.load_kaggle()
    stemmed_kaggle_words = stm.stem_list(original_kaggle_words[::j], bnc_words)

    # Plot two lines of points
    original_points = []
    stemmed_points = []

    original_kaggle_size = len(stemmed_kaggle_words)
    stemmed_kaggle_size = len(stemmed_kaggle_words)
    accumulator = 0
    freq_accumulator = 0

    # Tally up words in the Kaggle corpus and sort by frequency decreasing
    original_kaggle_tally = Counter(original_kaggle_words)
    stemmed_kaggle_tally = Counter(stemmed_kaggle_words)

    for _, word_freq in original_kaggle_tally.iteritems():
        # Percentage of Kaggle corpus covered by this word
        percentage = (word_freq + freq_accumulator) / original_kaggle_size
        freq_accumulator += word_freq

        # Number of tokens so far, squared
        accumulator += 1
        number_of_tokens = math.pow(accumulator, 2)

        # Plottable (x,y) point
        original_points.append((percentage, number_of_tokens))

    for _, word_freq in stemmed_kaggle_tally.iteritems():
        # Percentage of Kaggle corpus covered by this word
        percentage = word_freq / stemmed_kaggle_size

        # Number of tokens so far, squared
        accumulator += 1
        number_of_tokens = math.pow(accumulator, 2)

        # Plottable (x,y) point
        stemmed_points.append((percentage, number_of_tokens))

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
        coords_string += '{' + str(x) + ', ' + str(y) + '}'
        if count < limit:
            coords_string += ', '

    coords_string += '};'

    return coords_string


def main():
    (original_points, stemmed_points) = create_frequency_plots()

    bnc_calculator.save_temp('stemming_benefit_lines',
                             [points_to_mathematica(original_points),
                              points_to_mathematica(stemmed_points, 's')])

if __name__ == '__main__':
    args = sys.argv

    for arg in args:
        if 'size:' in arg:
            try:
                stemming_jump = int(arg[5:])
            except ValueError:
                print(usage_string)
                sys.exit()

    main()
