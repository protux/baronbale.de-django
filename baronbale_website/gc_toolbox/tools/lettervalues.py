import re

ALPHABET_VALUE_DICT = {
    'a': 1, 'A': 1,
    'b': 2, 'B': 2,
    'c': 3, 'C': 3,
    'd': 4, 'D': 4,
    'e': 5, 'E': 5,
    'f': 6, 'F': 6,
    'g': 7, 'G': 7,
    'h': 8, 'H': 8,
    'i': 9, 'I': 9,
    'j': 10, 'J': 10,
    'k': 11, 'K': 11,
    'l': 12, 'L': 12,
    'm': 13, 'M': 13,
    'n': 14, 'N': 14,
    'o': 15, 'O': 15,
    'p': 16, 'P': 16,
    'q': 17, 'Q': 17,
    'r': 18, 'R': 18,
    's': 19, 'S': 19,
    't': 20, 'T': 20,
    'u': 21, 'U': 21,
    'v': 22, 'V': 22,
    'w': 23, 'W': 23,
    'x': 24, 'X': 24,
    'y': 25, 'Y': 25,
    'z': 26, 'Z': 26,
}

NUMERIC_VALUE_DICT = {
    '0': 0,
    '1': 1,
    '2': 2,
    '3': 3,
    '4': 4,
    '5': 5,
    '6': 6,
    '7': 7,
    '8': 8,
    '9': 9,
}

def count(message, extras, offset, direction, include_numerics):
    extras = clean_extras(extract_extras_dict(extras))
    total_signs = len(message)
    relevant_signs = 0
    letters = 0
    numbers = 0
    special_characters = 0
    total_value = 0
    relevant_values = []
    
    for char in message:
        
        value = get_value(char, extras, offset, direction, include_numerics)
        
        if value > 0:
            relevant_values += [value]
            
        total_value += value
        
        if value != 0:
            relevant_signs += 1

        if char in ALPHABET_VALUE_DICT:
            letters += 1
        elif char in NUMERIC_VALUE_DICT:
            numbers += 1
        else:
            special_characters += 1
    
    return {
        'total_signs': total_signs, 
        'relevant_signs': relevant_signs, 
        'letters': letters,
        'numbers': numbers,
        'special_characters': special_characters,
        'total_value': total_value, 
        'relevant_values': relevant_values,
        'sum_of_digits': calculate_sum_of_digits(total_value),
        'iterated_sum_of_digits': calculate_iterated_sum_of_digits(total_value),
    }

def calculate_sum_of_digits(total_value):
    sum_of_digits = 0
    while total_value:
        sum_of_digits += total_value % 10
        total_value //= 10
    return sum_of_digits

def calculate_iterated_sum_of_digits(total_value):
    while (total_value > 9):
        total_value = calculate_sum_of_digits(total_value)
    return total_value
    
def extract_extras_dict(extras):
    result_dict = dict()
    if len(extras) == 0:
        return result_dict
    split = re.split('\r\n|\n', extras)
    for extra in split:
        splitted_extra = extra.split(':=')
        if len(splitted_extra) == 2 and len(splitted_extra[0]) == 1 and len(splitted_extra[1]) > 0:
            result = re.search('^[-]?[0-9]+$', splitted_extra[1])
            if result != None and len(result.group(0)) > 0:
                result_dict[splitted_extra[0]] = int(splitted_extra[1])
    return result_dict

def get_value(sign, extras, offset, direction, include_numeric):
    value = ALPHABET_VALUE_DICT.get(sign, 0)
    if value > 0:
        value += offset
        if direction == '2':
            return 27 - value
        return value
    elif sign in NUMERIC_VALUE_DICT and include_numeric:
        return NUMERIC_VALUE_DICT[sign]
    else:
        return extras.get(sign, 0)
    
def clean_extras(extras):
    cleaned_extras = dict()
    for extra in extras.items():
        if len(extra[0]) == 1 and type(extra[1]) == int:
            cleaned_extras[extra[0]] = extra[1]
    return cleaned_extras
