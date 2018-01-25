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

        # Temporarily stores the headers and body of the original file
        csv_headers = list()
        csv_body = list()

        """ Open the file as read-only, retrieve the current headers,
            translate and store them in a different dictionary """
        with open(self.orig_csv_file, 'r') as fr:
            reader = csv.reader(fr)
            del csv_headers[:]
            del csv_body[:]
            # Represents the first line of the file, in other words, the header
            header = 1
            try:
                for row in reader:
                    if reader.line_num == header:
                        for column in row:
                            if column.strip() in translations.keys():
                                csv_headers.append(translations.get(column.strip()))
                            else:
                                csv_headers.append(column.strip())
                    else:
                        csv_body.append(row)
            except csv.Error as e:
                sys.exit('Error while reading file: %s, line: %d: %s' % (filename, reader.line_num, e))
            finally:
                fr.close()

        """ Generate a new CSV file containing the translation of the matched words
        but not excluding the words that have not been found """
        with open(self.new_csv_file, 'w') as fw:
            delimiter = ", "
            counter = 1
            try:
                for header in csv_headers:
                    if counter < len(csv_headers):
                        fw.write(header + delimiter)
                    else:
                        fw.write(header)
                        fw.write('\n')
                    counter += 1

                """ Since csv_body is a list of text rows
                    we need to iterate through each row and retrieve each element of the current row
                    e.g: ['0', '2015-01-11', '3.0', '53.00587123', '0.0', '0.0'] """
                for body in csv_body:
                    counter = 1
                    for data in body:
                        if counter < len(body):
                            fw.write(data + delimiter)
                        else:
                            fw.write(data)
                        counter += 1
                    fw.write('\n')
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
