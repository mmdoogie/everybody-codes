ALPHABET = 'abcdefghijklmnopqrstuvwxyz'
DIGITS = '0123456789'
HEXCHARS = '0123456789abcdef'

def let2num(letter):
    return ord(letter.lower()) - ord('a')

def num2let(num):
    return chr(num + ord('a'))
