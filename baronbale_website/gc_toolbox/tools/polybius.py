import re

from django.utils.translation import ugettext as _

DECRYPTION_KEY = {
    '11': 'a',
    '12': 'b',
    '13': 'c',
    '14': 'd',
    '15': 'e',
   
    '21': 'f',
    '22': 'g',
    '23': 'h',
    '24': 'i',
    '25': 'k',
    
    '31': 'l',
    '32': 'm',
    '33': 'n',
    '34': 'o',
    '35': 'p',
    
    '41': 'q',
    '42': 'r',
    '43': 's',
    '44': 't',
    '45': 'u',
    
    '51': 'v',
    '52': 'w',
    '53': 'x',
    '54': 'y',
    '55': 'z',
}

ENCRYPTION_KEY = {
    'a': '11',
    'b': '12',
    'c': '13',
    'd': '14',
    'e': '15',
    
    'f': '21',
    'g': '22',
    'h': '23',
    'i': '24',
    'j': '24',
    'k': '25',
    
    'l': '31',
    'm': '32',
    'n': '33',
    'o': '34',
    'p': '35',
    
    'q': '41',
    'r': '42',
    's': '43',
    't': '44',
    'u': '45',
   
    'v': '51',
    'w': '52',
    'x': '53',
    'y': '54',
    'z': '55',
}

def decrypt(text):
    nums = _split_text(text)
    decrypted_text = ""
    for num in nums:
        try:
            decrypted_text += DECRYPTION_KEY[num]
        except KeyError:
            pass
    return decrypted_text
    
def _split_text(text):
    splitted = re.split('[^0-9]+', text)
    final = []
    for spl in splitted:
        if len(spl) > 2:
            final += _split_length(spl)
        else:
            final += [spl]
    return final
            
def _split_length(text):
    if len(text) % 2 != 0:
        raise ValueError(_("Error while splitting the input in pairs of two."))
    index = 0
    items = []
    while index <= len(text) - 2:
        items += [text[index: index + 2]]
        index += 2
    return items
    
def encrypt(text):
    text = text.lower()
    encrypted_chars = []
    for ch in text:
        try:
            encrypted_chars += [ENCRYPTION_KEY[ch]]
        except KeyError:
            pass
    return "".join(encrypted_chars)

