import sys

ALPHABET_CAPITAL = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
ALPHABET = "abcdefghijklmnopqrstuvwxyz"

def encrypt(rot, text):
    ciphertext = ''
    key = int(rot)
    for char in text:
        index = str.find(ALPHABET, char)
        if index >= 0:
            char_index = _get_encrypted_index(index, key)
            ciphertext += ALPHABET[char_index]
        else:
            index = str.find(ALPHABET_CAPITAL, char)
            if index >= 0:
                char_index = _get_encrypted_index(index, key)
                ciphertext += ALPHABET_CAPITAL[char_index]
            else:
                ciphertext += char
    return ciphertext

def _get_encrypted_index(index, key):
	index += key
	if index > 25:
		index -= 26
	return index
		
def try_all_keys(text):
    if isinstance(text, str):
        text_array = text.split('\n')
    else:
        text_array = text
    decrypted_text = ""
    
    for rot in range(1,26):
        decrypted_text += "rot-key: %s%s" % (rot, "\n")
        for line in text_array:
            decrypted_text += decrypt(rot, line) + "\n"
        decrypted_text += "\n"
    return decrypted_text
        
def decrypt(key, text):
    decrypted_text = ""
    for c in text:
        try:
            index = ALPHABET.find(c)
            if index >= 0:
                decrypted_text += ALPHABET[_get_decrypted_index(index, int(key))]
            else:
                index = ALPHABET_CAPITAL.find(c)
                if index >= 0:
                    decrypted_text += ALPHABET_CAPITAL[_get_decrypted_index(index, int(key))]
                else:
                    decrypted_text += c
            
        except:
            decrypted_text += c 
    return decrypted_text

def _get_decrypted_index(index, key):
    index -= int(key)
    
    if index < 0:
        index += 26
    
    return index
