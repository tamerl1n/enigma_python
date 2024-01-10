from typing import Dict, List
from utils import caesar_shift

class Rotor:
    def __init__(self, alphabet: str, notch: str ="A", ring_setting: str = 'A', position: str = 'A'):
        self.position = ord(position) - 65
        self.notch = ord(notch) - 65
        ring_setting = ord(ring_setting) - 65
        self.alphabet = caesar_shift(alphabet, ring_setting)
        if ring_setting > 0:
            self.alphabet = self.alphabet[26-ring_setting:] + self.alphabet[0:26-ring_setting]
        

    def rotate(self):
        self.position = (self.position + 1) % 26
    
    def forward_movement(self, char: str):
        char_index = (ord(char) - 65) % 26
        pos = ord(self.alphabet[(char_index + self.position) % 26]) - 65
        encrypted_char_index = (pos - self.position + 26) % 26 
        return chr(encrypted_char_index + 65)

    def backward_movement(self, char: str):
        char_index = self.alphabet.index(chr(65 + ((ord(char) + self.position - 65) % 26)))
        encrypted_char_index = (char_index - self.position + 26) % 26
        return chr(encrypted_char_index + 65)

    
    
class Reflector:
    def __init__(self, alphabet: str):
        self.alphabet = alphabet

    def reflect(self, char: str):
        return self.alphabet[ord(char) - 65]


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

