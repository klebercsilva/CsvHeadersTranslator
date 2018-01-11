# -*- coding: utf-8 -*-
#
# Script to automatically translate headers from any CSV file.
#
# Author: Kleber Silva.

import csv, sys

def main(original_csv_file, new_csv_file):
    # We are using a dictionary to store the original word and the translated word as a <key, value> pair
    # TODO: Retrieve information from another source e.g: database, webservice
    translations = {'acct': 'id_conta',
                    'utc_date':'data_coleta_dados',
                    'num_courses_visited': 'num_cursos_visitados'}

    # Temporary list that will receive the original headers to be translated
    csv_data = list()

    # Open the file as read-only, retrieve the data and store in another dictionary
    # along with the corresponding translation
    with open(original_csv_file, 'r') as f:
        reader = csv.reader(f)
        del csv_data[:]
        # Just a cool way to represent the first line of the file
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

    # Write back in the original file the corresponding headers already translated
    with open(new_csv_file, 'w') as f:
        delimiter = ", "
        col_count = 1
        try:
            for data in csv_data:
                if col_count < len(csv_data):
                    f.write(data + delimiter)
                else:
                    f.write(data)
                col_count += 1
        except IOError as ioe:
            sys.exit('Error while reading file: %s, %s' % (filename, ioe))
        finally:
            f.close()

if __name__ == "__main__":
    if len(sys.argv) != 3:
        sys.exit('Invalid number of arguments. \nPlease enter the <original_csv_filepath.csv> and <new_csv_filepath.csv>.')
    else:
        original_csv_file = sys.argv[1]
        new_csv_file = sys.argv[2]
        main(original_csv_file, new_csv_file)
