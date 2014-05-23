#!/usr/bin/env python
# vim: set fileencoding=utf8 :

"""Produce plottable data to determine whether stemming is useful."""

from __future__ import division
from collections import Counter
import math
import stemmer as stm  # My stemmer functions
import bnc_calculator


def create_frequency_plots():
    bnc_words = stm.load_bnc()
    original_kaggle_words = ['hello']  # stm.load_kaggle()
    stemmed_kaggle_words = stm.stem_list(original_kaggle_words, bnc_words)

    # Plot two lines of points
    original_points = []
    stemmed_points = []

    original_kaggle_size = len(stemmed_kaggle_words)
    stemmed_kaggle_size = len(stemmed_kaggle_words)
    accumulator = 0

    # Tally up words in the Kaggle corpus and sort by frequency decreasing
    original_kaggle_tally = Counter(original_kaggle_words)
    stemmed_kaggle_tally = Counter(stemmed_kaggle_words)

    for _, word_freq in original_kaggle_tally.iteritems():
        # Percentage of Kaggle corpus covered by this word
        percentage = word_freq / original_kaggle_size

        # Number of tokens so far, squared
        accumulator += 1
        number_of_tokens = math.pow(accumulator, 2)

        # Plottable (x,y) point
        original_points.append((number_of_tokens, percentage))

    for _, word_freq in stemmed_kaggle_tally.iteritems():
        # Percentage of Kaggle corpus covered by this word
        percentage = word_freq / stemmed_kaggle_size

        # Number of tokens so far, squared
        accumulator += 1
        number_of_tokens = math.pow(accumulator, 2)

        # Plottable (x,y) point
        stemmed_points.append((number_of_tokens, percentage))

    return (original_points, stemmed_points)


def points_to_mathematica(xy_tuple_list):
    # Produces output in the form of two lists, xx and yy such that we can plot
    # and further manipulate them in Mathematica using:
    # data = Transpose@{xx, yy};
    # ListPlot[data]

    x_coords_string = 'xx = {'
    y_coords_string = 'yy = {'
    limit = len(xy_tuple_list)
    count = 0

    for (x, y) in xy_tuple_list:
        count += 1

        x_coords_string += str(x)
        y_coords_string += str(y)

        if count < limit:
            x_coords_string += ', '
            y_coords_string += ', '

    x_coords_string += '}'
    y_coords_string += '}'

    return x_coords_string + '\n' + y_coords_string


def main():
    (original_points, stemmed_points) = create_frequency_plots()

    bnc_calculator.save_temp('stemming_benefit_lines',
                             [points_to_mathematica(original_points),
                              points_to_mathematica(stemmed_points)])

if __name__ == '__main__':
    main()
