#! /usr/bin/env python

import os
import requests
import sys
from lxml import html

comment_char = {
    '.py': '# ',
    '.java': '// ',
    '.go': '// ',
    '.c': '// ',
    '.cpp': '// '
}


def download_problem(num, extension, interpreter=''):
    page = requests.get('https://projecteuler.net/problem=' + str(num))

    filename = str(num) + extension
    if page.status_code != 200 or os.path.exists(filename):
        print 'Did not download problem #{}'.format(num)

    tree = html.fromstring(page.content)
    problem = tree.xpath('//p')

    prob_statement = interpreter
    for p in problem:
        prob_statement += comment_char[extension] + print_text(p)

    with open(str(num) + extension, 'w') as f:
        f.write(prob_statement.encode('utf8'))


def print_text(element):
    result = element.text if element.text else ''

    for child in element.getchildren():
        result += print_text(child)

    result += element.tail if element.tail else ''

    return result


if __name__ == '__main__':

    if len(sys.argv) < 4:
        print 'Usage ./get_problems.py <file extension> <problem number (ex: 50) or range (ex: 1-10)> <optional: interpreter path>'
        sys.exit(0)

    extension = sys.argv[1]
    if '-' in sys.argv[2]:
        start, end = sys.argv[2].split('-')
        start, end = int(start), int(end)

    else:
        start, end = int(sys.argv[2]), int(sys.argv[2])

    interpreter = sys.argv[3] if len(sys.argv) > 3 else ''

    for problem in range(start, end + 1):
        download_problem(problem, extension, interpreter)
