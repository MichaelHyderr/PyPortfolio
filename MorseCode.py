# ---- DICTIONARY LATIN ALPHABET & NUMBERS : MORSE CODE-----

l_to_m_dict = {"A": "•—", "B": "—•••", "C": "—•—•", "D": "—••", "E": "•", "F": "••—•", "G": "——•", "H": "••••",
               "I": "••",
               "J": "•———", "K": "—•—", "L": "•—••", "M": "——", "N": "—•", "O": "———", "P": "•——•", "Q": "——•—",
               "R": "•—•", "S": "•••", "T": "—", "U": "••—", "V": "•••—", "W": "•——", "X": "—••—", "Y": "—•——",
               "Z": "——••",
               "0": "—————", "1": "•————", "2": "••———", "3": "•••——", "4": "••••—", "5": "•••••", "6": "—••••",
               "7": "——•••", "8": "———••", "9": "————•"}

# ---- DICTIONARY MORSE CODE : LATIN ALPHABET & NUMBERS ----

m_to_l_dict = {value: key for key, value in l_to_m_dict.items()}  # List comprehension


# ---- ENCODE FROM L TO M ----
def encode(string):
    encoded_string = ""
    for char in string:
        if char in l_to_m_dict:
            morse_code = l_to_m_dict[char]  # Cerco il value della dict corrispondente al char(key)
            encoded_string = encoded_string + morse_code + " "  # Lo aggiungo alla nuova string aggiungendo uno spazio alla fine per rendere ogni lettera leggibile
        elif char == " ":  # Se c'è uno spazio nel testo da tradurre
            encoded_string = encoded_string + "  "  # Aggiungo due spazi per separare le due parole
        else:
            encoded_string = encoded_string + char + " "  # Se nel testo da tradurre c'è un carattere non presente nella dict allora lo riscrivo tale e quale
    print(encoded_string)


# ---- DECODE FROM M TO L ----
def decode(string):
    decoder = string.split(" ")  # Creo una lista dove ogni elemento della stringa è separato dallo spazio
    decoded_string = ""
    for code in decoder:
        if code in m_to_l_dict:  # Come sopra
            char = m_to_l_dict[code]
            decoded_string = decoded_string + char
        elif code == "":
            decoded_string = decoded_string + " "
        else:
            decoded_string = decoded_string + code
    print(decoded_string)


text = input("Type your text here to translate from latin alphabet to morse code or viceversa: ").upper()

# ---- LATIN OR MORSE DETECTOR ----
for char in text:
    if char in l_to_m_dict:  # Se trovo un carattere nella dict allora L to M
        encode(text)
        break
    else:
        decode(text)
        break
