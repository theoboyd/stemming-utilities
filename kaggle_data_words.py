#!/usr/bin/env python
# vim: set fileencoding=utf8 :

"""Script to help with Kaggle (not ESP) word-related tasks."""

from os import listdir
from os.path import isfile, join

pubblinddirectory = "../KaggleData/public_test_options/"
privblinddirectory = "../KaggleData/private_test_options/"
pubdirectory = "../KaggleData/mlc2013/private_test_true_labels/"
privdirectory = "../KaggleData/mlc2013/private_test_true_labels/"

pubfiles = [f for f in listdir(pubdirectory) if isfile(join(pubdirectory, f))]
privfiles = [f for f in listdir(privdirectory) if isfile(join(privdirectory, f))]

allwordspub = []
for pubf in pubfiles:
    with open(join(pubdirectory, pubf)) as pubfo:
        allwordspub.append(pubfo.read().splitlines())

allwordspriv = []
for privf in privfiles:
    with open(join(privdirectory, privf)) as privfo:
        allwordspriv.append(privfo.read().splitlines())

# Flatten the lists
awpub = [item for sublist in allwordspub for item in sublist]
awpriv = [item for sublist in allwordspriv for item in sublist]

words1k = []
with open("../IntermediateWordLists/words1k.txt") as words1kfo:
    words1k = words1kfo.read().splitlines()

awpubin1k = [word for word in awpub if word in words1k]
awprivin1k = [word for word in awpriv if word in words1k]


print("                  | Public | Private | All")
print("File count        | " + str(len(allwordspub)) + " | " + str(len(allwordspriv)) + " | " + str(len(allwordspub) + len(allwordspriv)))
print("All               | " + str(len(awpub)) + " | " + str(len(awpriv)) + " | " + str(len(awpub)) + str(len(awpriv)))
print("Unique            | " + str(len(set(awpub))) + " | " + str(len(set(awpriv))) + " | " + str(len(set(awpub)) + len(set(awpriv))))
print("All in words1k    | " + str(len(awpubin1k)) + " | " + str(len(awprivin1k)) + " | " + str(len(awpubin1k) + len(awprivin1k)))
print("Unique in words1k | " + str(len(set(awpubin1k))) + " | " + str(len(set(awprivin1k))) + " | " + str(len(set(awpubin1k)) + len(set(awprivin1k))))
