'''
This script will parse standard kindle clippings file ('My Clippings.txt') and
will create '.../Output/book_title (author).txt file for each book.
The file will contain only highlights separated by an empty line.
'''

import argparse
import os

class Parser(object):

    def parse(self, file):
        dictionary = dict()
        content = [x.strip().decode("UTF-8") for x in file.read().split("\n==========")]
        for chunk in content:
            try:
                title, highlight = self.parse_chunk(chunk)
            except ValueError:
                continue

            if title in dictionary:
                dictionary[title].append(highlight)
            else:
                dictionary[title] = [highlight]

        self.save_highlights(dictionary)


    def parse_chunk(self, chunk):
        """Parse a chunk of text.

        Keyword arguments:
        chunk -- represents a chunk of text between two '==========' separators
        """
        lines = chunk.splitlines()

        if not lines:
            raise ValueError('The line is empty')

        if 'Highlight' not in lines[1]:
            raise ValueError('The line does not contain Highlight')

        title = lines[0].encode("UTF-8")
        highlight = lines[3].encode("UTF-8")

        return title, highlight


    def save_highlights(self, dictionary):
        """Save 'book_title (author).txt' file for each book in ''.../Output' directory.

        Keyword arguments:
        dictionary -- title : [highlight1, highlight2, ...] structure
        """
        path = os.path.dirname(os.path.realpath(__file__))
        directory = os.path.join(path, 'Output')

        try:
            os.makedirs(directory)
        except OSError:
            pass # Directory already exists

        for key, value in dictionary.iteritems():
            path = os.path.join(directory, key + '.' + 'txt')
            with open(path, 'w') as file:
                for item in value:
                    file.write("%s\n\n" % item)

if __name__ == '__main__':

    argumentParser = argparse.ArgumentParser()
    argumentParser.add_argument('file', type=argparse.FileType('r'), help="'My Clippings.txt' file path")
    args = argumentParser.parse_args()

    parser = Parser()
    parser.parse(args.file)
