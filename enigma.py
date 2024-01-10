from typing import Dict, List

class Rotor:
    def __init__(self, alphabet: str, notch: str ="A", ring_setting: str = 'A', position: str = 'A', a_ord: int = 65, alphabet_length: int = 26):
        self.position = ord(position) - a_ord
        self.notch = ord(notch) - a_ord
        ring_setting = ord(ring_setting) - a_ord
        self.a_ord = a_ord
        self.alphabet = caesar_shift(alphabet, ring_setting)
        self.alphabet_length = alphabet_length
        if ring_setting > 0:
            self.alphabet = self.alphabet[alphabet_length-ring_setting:] + self.alphabet[0:alphabet_length-ring_setting]
        

    def rotate(self):
        self.position = (self.position + 1) % self.alphabet_length
    
    def forward_movement(self, char: str):
        char_index = (ord(char) - self.a_ord) % self.alphabet_length
        pos = ord(self.alphabet[(char_index + self.position) % self.alphabet_length]) - self.a_ord
        encrypted_char_index = (pos - self.position + self.alphabet_length) % self.alphabet_length 
        return chr(encrypted_char_index + self.a_ord)

    def backward_movement(self, char: str):
        char_index = self.alphabet.index(chr(self.a_ord + ((ord(char) + self.position - self.a_ord) % self.alphabet_length)))
        encrypted_char_index = (char_index - self.position + self.alphabet_length) % self.alphabet_length
        return chr(encrypted_char_index + self.a_ord)

    
    
class Reflector:
    def __init__(self, alphabet: str, a_ord: int = 65):
        self.alphabet = alphabet
        self.a_ord = a_ord

    def reflect(self, char: str):
        return self.alphabet[ord(char) - self.a_ord]


class Plugboard:
    def __init__(self, settings: Dict):
        self.settings = settings

    def swap(self, char: str):
        return self.settings.get(char, char)


class Enigma:
    def __init__(self, reflector: Reflector, rotors: List[Rotor], plugboard: Plugboard):
        self.reflector = reflector
        self.rotors = rotors
        self.plugboard = plugboard

    def encrypt_char(self, char):
        char = self.plugboard.swap(char)
        for ind, rotor in enumerate(reversed(self.rotors[1:])):
            if rotor.notch == rotor.position:
                self.rotors[1 - ind].rotate()
        self.rotors[-1].rotate()
        for rotor in reversed(self.rotors):
            char = rotor.forward_movement(char)
        char = self.reflector.reflect(char)
        for rotor in self.rotors:
            char = rotor.backward_movement(char)
        char = self.plugboard.swap(char)
        return char

    def encrypt_message(self, message: str):
        encrypted_message = ""
        for char in message.upper():
            if char.isalpha():
                encrypted_message += self.encrypt_char(char)
            else:
                encrypted_message += char
        return encrypted_message
