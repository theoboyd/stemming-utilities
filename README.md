Code to assist with BNC (British National Corpus) and Kaggle (and ESPGame100k)
word research project.

Requires a number of (large, independent) directories of data files as
specified.


Stemmer
-------

Perform cleanup and stemming operations. Both standalone (run stemmer.py) or as
a stemming module (import stemmer).


BNC Calculator
--------------

Calculates statistics for the BNC words along with stemmed and unstemmed Kaggle
words and tokens.


File To Data
------------

Aims to convert files output by BNC Calculator into easily plottable data.


Stemming Benefit
----------------

Tries to determine the utility of stemming by producing metrics for percentage
of words covered versus number of tokens.


Create Word File
----------------

Generates a list of the most common words, ordered by frequency, for use in COALS calculations.


Static Statistics
-----------------
Calculates word statistics from previously generated static sources.
