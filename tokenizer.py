"""Modul omogućava parsiranje aritmetičkih izraza."""
import re

__author__ = 'mijicd'


REGEX = r'(?:[(][\-])|(?:\d*\.\d+)|(?:\d+)|(?:[()+\-\^/*])'


def tokenize(expression):
    """Funkcija kreira tokene na osnovu zadatog izraza.

    Postupak formiranja liste tokena koristi regularni izraz
    zadat putem REGEX varijable. Omogućeno je pronalaženje
    sledećih tipova tokena:
        - floating-point vrednosti
        - celobrojne vrednosti
        - operatori +, -, *, /, ^
        - zagrade

    Args:
        expression (string): Izraz koji se parsira.

    Returns:
        list: Lista pronađenih tokena.

    Raises:
        AssertionError: Ako izraz nije zadat kao string.
    """
    assert isinstance(expression, str), "Expression should be string!"
    tokens = re.findall(REGEX, expression)
    index = 0

    if len(tokens) >= 2 and tokens[0] == '-' and not tokens[1].startswith('('):
        tokens[1] = '-' + tokens[1]
        del tokens[0]

    while index < len(tokens)-1:
        if tokens[index] == '(-':
            tokens[index] = '('
            if tokens[index+1].startswith('('):
                tokens.insert(index+1, '-')
                index += 1
            else:
                tokens[index+1] = '-'+ tokens[index+1]
        index += 1

    return tokens


if __name__ == '__main__':
    #
    # key: izraz, value: očekivana lista tokena
    #
    test_cases = {
        # test simple
        "4": ['4'],
        "-14.2": ['-14.2'],
        "-4": ['-4'],
        "-4-4": ['-4', '-', '4'],

        # test floats
        "3.14   ^2": ['3.14', '^', '2'],
        "(2.08-.03) ^  2": ['(', '2.08', '-', '.03', ')', '^', '2'],

        # test integers
        "2+(3*4)": ['2', '+', '(', '3', '*', '4', ')'],
        "22     56": ['22', '56'],

        # test negative
        "-(2+1)+1" : ['-', '(', '2', '+', '1', ')', '+', '1'],
        "(-4-2)+1" : ['(', '-4', '-', '2', ')', '+', '1'],
        "-(-5)" : ['-', '(', '-5', ')'],
        "-(-(-5))": ['-', '(', '-', '(', '-5', ')', ')'],

        # test invalid
        "ab cd": [],
        "10,22": ['10', '22']
    }

    for expression, expected in test_cases.items():
        tokenized = tokenize(expression)
        assert expected == tokenized
