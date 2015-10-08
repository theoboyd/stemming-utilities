#!/usr/bin/env python
# vim: set fileencoding=utf8 :
from os import walk

def load_directory(path):
    file_names = []
    file_lines = []
    
    for (_, _, file_name) in walk(path):
        file_names.extend(file_name)

    for file_name in file_names:
        file = open(stm.esp_path + stm.original_dir +
                             file_name)
        file_line = file.readline()  # Python doesn't have do-whiles
        while(file_line != ''):
            file_lines.append(file_line)
            file_line = file.readline()
        file.close()
        
    return file_lines