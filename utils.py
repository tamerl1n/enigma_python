A_ORD = 65
ALPHABET_LENGTH = 26

def caesar_shift(str, amount):
    output = ""

    for i in range(0,len(str)):
        c = str[i]
        code = ord(c)
        if ((code >= A_ORD) and (code <= A_ORD + ALPHABET_LENGTH - 1)):
            c = chr(((code - A_ORD + amount) % ALPHABET_LENGTH) + A_ORD)
        output = output + c
    return output    
