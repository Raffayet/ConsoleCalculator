from tokenizer import tokenize
from stack_start import Stack

"""
Naziv ovog modula treba da ostane nepromenjen.

Neophodno je implementirati metode calculate_from_infix(expression), to_postfix(expression),
 calculate_from_postfix(tokens). Izmena broja i tipa parametara nije dozvoljena ka ni izmena tipa povratne vrednosti.
 Obratite posebno pažnju na izuzetke koji se bacaju iz funkcije calculate_from_infix. Način na koji se ti izuzeci
 propagiraju (od mesta nastanka) nije određen, tako da mogu da poteknu ili iz funkcija to_postfix i
 calculate_from_postfix ili iz neke treće funkcije koja se interno poziva.

Zakomentarisan deo koda bi trebalo da se uključi u konačno rešenje kada se implementiraju svi izuzeci.

Rešenje će se testirati pokretanjem funkcije test. U obzir dolaze i drugi (ispravni i neispravni) izrazi. Pošto će se
testiranje zadataka obavljati automatski.
Obratiti pažnju na imenovanje svih klasa, funkcija i modula.
"""


class UnknownCharacterError(Exception):
    pass


class MissingOperandError(Exception):
    pass


class MissingOperatorError(Exception):
    pass


class NonMatchingNumberOfParenthesisError(Exception):
    pass


class OtherExpressionError(Exception):
    pass


class MyDivisionByZeroError(OtherExpressionError):
    pass


class MyEnterInputError(OtherExpressionError):
    pass


class MyRootingANegativeNumberError(OtherExpressionError):
    pass


class MyMultipleDotsError(OtherExpressionError):
    pass


def calculate_from_infix(expression):
    """
    :param expression - input string representing expression in infix notation (see test_cases)
    :return: integer or float overall result.
    :raises:
        UnknownCharacterError:  if expression contains unsupported characters
        MissingOperandError: if any operator is missing an operand (example: "5-4+")
        MissingOperatorError: if two consecutive operands are found (example: "5 6")
        NonMatchingNumberOfParenthesisError: if not every open parenthesis have matching closed one (example: "((4+3)*4")
        OtherExpressionError: if other problem has occurred
    """

    if expression == "":
        raise MyEnterInputError("Niste uneli nista!")

    if expression == ".":
        raise UnknownCharacterError("Uneli ste nedozvoljen karakter za ovaj kalkulator!")

    index = 0

    stek = Stack()

    for index in range(0, len(expression)):

        if expression[index] not in "0123456789.+-/*^() ":
            raise UnknownCharacterError("Uneli ste nedozvoljen karakter za ovaj kalkulator!")

        if index == len(expression) - 1:
            if expression[index - 1] in "0123456789." and expression[index] == "":
                raise MissingOperatorError("Nedostaje operator!")
            if expression[index - 1] == "." and expression[index] not in "0123456789":
                raise UnknownCharacterError("Uneli ste nedozvoljen karakter za ovaj kalkulator!")

        else:
            if expression[index] in "0123456789." and expression[index + 1] in ("", "("):
                raise MissingOperatorError("Nedostaje operator!")
            if expression[index] == "." and expression[index + 1] not in "0123456789":
                raise UnknownCharacterError("Uneli ste nedozvoljen karakter za ovaj kalkulator!")

        if index == len(expression) - 1:
            if expression[index - 1] in "+-/*^" and expression[index] in "+-/*^":
                raise MissingOperandError("Nedostaje operand!")

            if expression[index - 1] in "+-/*^" and expression[index] == "":
                raise MissingOperandError("Nedostaje operand!")

            if expression[index] in "+-*/^":
                raise MissingOperandError("Nedostaje operand!")

        else:
            if expression[index] in "+-/*^" and expression[index + 1] in "+-*/^":
                raise MissingOperandError("Nedostaje operand!")

            if expression[index] in "+-/*^" and expression[index + 1] == "":
                raise MissingOperandError("Nedostaje operand!")

        if index == 0:

            if expression[index] in "+*/^":
                raise MissingOperandError("Nedostaje operand!")

        if expression[index] == "(":
            stek.push(expression[index])
        elif expression[index] == ")":
            if stek.is_empty():
                raise NonMatchingNumberOfParenthesisError("Zagrade nisu dobro uparene!")
            if stek.pop() != "(":
                raise NonMatchingNumberOfParenthesisError("Zagrade nisu dobro uparene!")

    if stek.is_empty() == False:
        raise NonMatchingNumberOfParenthesisError("Zagrade nisu dobro uparene!")

    tokens = to_postfix(expression)
    return calculate_from_postfix(tokens)


def to_postfix(expression):
    """
    :param expression - input string representing expression in infix notation (see test_cases)
    :return: list of tokens in postfix notation
    """
    tokens = tokenize(expression)

    stek2 = Stack()

    izlazna_lista = []

    for index in range(0, len(tokens)):
        if index == len(tokens) - 1:
            if tokens[index - 1].isdigit() and tokens[index].isdigit():
                raise MissingOperatorError("Nedostaje operator!")
            elif "." in tokens[index - 1] and "." in tokens[index]:
                raise MissingOperandError("Nedostaje operator!")
        else:
            if tokens[index].isdigit() and tokens[index + 1].isdigit():
                raise MissingOperatorError("Nedostaje operator!")
            elif "." in tokens[index] and "." in tokens[index + 1]:
                raise MissingOperandError("Nedostaje operator!")

    for token in tokens:

        if token.startswith("-") and len(token) > 1:
            izlazna_lista.append(token)

        if token.isdigit() or "." in token:
            izlazna_lista.append(token)

        elif token == "(":
            stek2.push(token)

        elif token == ")":
            while stek2._data[-1] != "(":
                izlazna_lista.append(stek2.pop())
            stek2.pop()

        elif token in "+-*/^":
            if token == "+":
                if stek2.is_empty():
                    stek2.push(token)
                else:
                    if stek2._data[-1] in "*/^+-":
                        izlazna_lista.append(stek2.pop())
                        stek2.push(token)
                    else:
                        stek2.push(token)

            elif token == "-":
                if stek2.is_empty():
                    stek2.push(token)
                else:
                    if stek2._data[-1] in "*/^+-":
                        izlazna_lista.append(stek2.pop())
                        stek2.push(token)
                    else:
                        stek2.push(token)

            elif token == "*":
                if stek2.is_empty():
                    stek2.push(token)
                else:
                    if stek2._data[-1] in "*/^":
                        izlazna_lista.append(stek2.pop())
                        stek2.push(token)
                    else:
                        stek2.push(token)

            elif token == "/":
                if stek2.is_empty():
                    stek2.push(token)
                else:
                    if stek2._data[-1] in "*/^":
                        izlazna_lista.append(stek2.pop())
                        stek2.push(token)
                    else:
                        stek2.push(token)

            elif token == "^":
                if stek2.is_empty():
                    stek2.push(token)
                else:
                    if stek2._data[-1] == "^":
                        izlazna_lista.append(stek2.pop())
                        stek2.push(token)
                    else:
                        stek2.push(token)

    izlazna_lista.append(stek2.pop())
    # transform tokens to postfix notation
    return izlazna_lista


def calculate_from_postfix(tokens):
    """

    :param tokens: list of tokens in postfix notation
    :return: integer or float result.

    """

    stek3 = Stack()

    for token in tokens:
        if token.isdigit():
            stek3.push(int(token))
        elif "." in token:
            stek3.push(float(token))

        elif token.startswith("-") and "." not in token and len(token) > 1:
            stek3.push(int(token))

        elif token.startswith("-") and "." in token and len(token) > 1:
            stek3.push(float(token))

        elif token in "+-*/^":

            if stek3.__len__() >= 2:
                drugi_operand = (stek3.pop())
                prvi_operand = (stek3.pop())

                if token == "+":
                    stek3.push(prvi_operand + drugi_operand)
                elif token == "-":
                    stek3.push(prvi_operand - drugi_operand)
                elif token == "*":
                    stek3.push(prvi_operand * drugi_operand)
                elif token == "/":
                    if drugi_operand == 0:
                        raise MyDivisionByZeroError("Nije dozvoljeno deljenje sa nulom!")
                    stek3.push(prvi_operand / drugi_operand)
                elif token == "^":
                    if prvi_operand < 0 and drugi_operand < 1:
                        raise MyRootingANegativeNumberError("Nije dozvoljeno korenovanje negativnog broja!")
                    stek3.push(prvi_operand ** drugi_operand)

            elif stek3.__len__() == 1:
                prvi_operand = stek3.pop()
                stek3.push(-prvi_operand)

    rezultat = stek3.pop()
    return rezultat

def test():
    test_cases_valid = {
        # test floats
        "3.14   ^2": 9.8596,
        "(2.08-.03) ^  2": 4.2025000000000015,

        # test integers
        "2+(3*4)": 14,
        "22*56/11": 112.0,

        # test negative
        "-(2+1)+1": -2,
        "(-4-2)+1": -5,
        "-(-5)": 5,
    }

    test_cases_invalid = {
        "22     56": MissingOperatorError,
        "ab cd": UnknownCharacterError,
        "10,22": UnknownCharacterError,
        "1-1-": MissingOperandError,
        "(43-(1+3)+3": NonMatchingNumberOfParenthesisError

     }

    for expression, expected in test_cases_valid.items():
        result = calculate_from_infix(expression)
        assert expected == result

    for expression, expected in test_cases_invalid.items():
        try:
            result = calculate_from_infix(expression)
            assert False
        except Exception as e:
            #assert type(e) == expected
            assert isinstance(e, expected)

if __name__ == '__main__':
    test()
