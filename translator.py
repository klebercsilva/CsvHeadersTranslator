# -*- coding: utf-8 -*-
#
# This script automatically translates headers from any CSV file.
#
# Author: Kleber Silva.

import csv, sys

class Translator:
    """ Translator class represents and translates the headers of a given .csv file
        Attributes:
            orig_csv_file: The original csv file which the headers will be translated from
            new_csv_file: The new csv file which the headers will be translated to
    """

    def __init__(self, orig_csv_file, new_csv_file):
        self.orig_csv_file = orig_csv_file
        self.new_csv_file = new_csv_file

        """ We are using a dictionary to store the original word as well as the translated word as a <key, value> pair
            TODO: Retrieve information from an external source e.g: database, webservice """
        translations = {'acct': 'id_conta',
                        'utc_date':'data_coleta_dados',
                        'num_courses_visited': 'num_cursos_visitados'}

        # List that will temporarily store the headers of the original file
        csv_data = list()

        """ Open the file as read-only, retrieve the current headers,
            translate and store them in a different dictionary """
        with open(self.orig_csv_file, 'r') as f:
            reader = csv.reader(f)
            del csv_data[:]
            # Represents the first line of the file, in other words, the header
            header = 1
            try:
                for row in reader:
                    if reader.line_num == header:
                        for column in row:
                            if column.strip() in translations.keys():
                                csv_data.append(translations.get(column.strip()))
                    else:
                        csv_data.append(column.strip())
            except csv.Error as e:
                sys.exit('Error while reading file: %s, line: %d: %s' % (filename, reader.line_num, e))
            finally:
                f.close()

        """ Generate a new CSV file containing the translation of the matched words
        but not excluding the words that have not been found """
        with open(self.new_csv_file, 'w') as fw:
            delimiter = ", "
            col_count = 1
            try:
                for data in csv_data:
                    if col_count < len(csv_data):
                        fw.write(data + delimiter)
                    else:
                        fw.write(data)
                    col_count += 1
            except IOError as ioe:
                sys.exit('Error while reading file: %s, %s' % (filename, ioe))
            finally:
                fw.close()

if __name__ == "__main__":
    if len(sys.argv) != 3:
        sys.exit('Invalid number of arguments. \n' +
                 'Please enter the full path of the original csv file as well as the new one. \n' +
                 'e.g: python translator.py ~/Documents/data.csv ~/Documents/new_data.csv')
    else:
        t = Translator(sys.argv[1], sys.argv[2])
