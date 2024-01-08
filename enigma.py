from typing import Dict, List

class Rotor:
    def __init__(self, alphabet: str, notch: str ="A", position: int = 0):
        self.alphabet = alphabet
        self.position = position
        self.notch = ord(notch) - 65

    def rotate(self):
        self.position = (self.position + 1) % 26
    
    def forward_movement(self, char: str):
        char_index = (ord(char) - 65 - self.position) % 26
        encrypted_char_index = (ord(self.alphabet[char_index]) - 65 + self.position) % 26
        return chr(encrypted_char_index + 65)

    def backward_movement(self, char: str):
        char_index = (ord(char) - 65 - self.position ) % 26
        encrypted_char_index = (self.alphabet.index(chr(char_index + 65)) + self.position) % 26
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
        for ind, rotor in enumerate(self.rotors):
            char = rotor.forward_movement(char)
        char = self.reflector.reflect(char)
        for rotor in reversed(self.rotors):
            char = rotor.backward_movement(char)
        char = self.plugboard.swap(char)
        self.rotors[0].rotate()
        for ind, rotor in enumerate(self.rotors[1:]):
            near_rotor = self.rotors[ind]                        
            if rotor.notch == near_rotor.position:
                rotor.rotate()
        return char

    def encrypt_message(self, message: str):
        encrypted_message = ""
        for char in message.upper():
            if char.isalpha():
                encrypted_message += self.encrypt_char(char)
            else:
                raise Exception("Only uppercase chars")
        return encrypted_message
