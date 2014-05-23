#!/usr/bin/env python
# vim: set fileencoding=utf8 :

"""Quick script to convert a word file into useful data for plotting."""

from __future__ import division
from collections import defaultdict
import sys
import stemmer  # My stemmer functions
import bnc_calculator

wordlists_path = '../IntermediateWordLists/'


def main(file_name):
    data = load_data(file_name)

    histogram = defaultdict(int)
    for item in data:
        histogram[item] += 1

    #histogram = dict(zip(data, map(data.count, data)))

    # Format for plotting
    plot_output = '\n{'
    limit = len(histogram)
    count = 0
    accumulator = 0
    for w in sorted(histogram, key=histogram.get, reverse=True):
        count += 1
        accumulator += histogram[w]
        #plot_output += str(accumulator)
        plot_output += ('{' + str(w) + ', ' + str(accumulator) + '}')
        if count < limit:
            plot_output += ', '

    plot_output += '}\n'

    bnc_calculator.save_temp('plottable_' + file_name, [plot_output])


def load_data(file_name):
    # Given a file path, produce a list of useful plottable data
    # That eg: Mathematica could use
    data = []

    data_file = open(wordlists_path + file_name + '.txt')
    data_line = data_file.readline()
    while(data_line != ''):
        data.append(stemmer.clean_text(data_line))
        data_line = data_file.readline()
    data_file.close()

    return data


if __name__ == '__main__':
    args = sys.argv
    main(args[1])
