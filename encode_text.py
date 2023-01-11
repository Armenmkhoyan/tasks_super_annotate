import string


def encode_text_by_letter_position(text: str, pos: int) -> str:
    temp = ""
    for letter in text:
        if is_letter(letter):
            temp += shift_letter_by_position(letter, pos)
        else:
            temp += letter
    return temp


def shift_letter_by_position(letter: str, pos: int) -> str:
    numbered_alphabet = {letter: index for index, letter in enumerate(string.ascii_lowercase)}

    letter_position = numbered_alphabet[letter.lower()]  # E.g.  a -> 0, b -> 1 ... z-> 25
    letter_shift_position = (letter_position + pos) % len(numbered_alphabet)

    return string.ascii_lowercase[letter_shift_position]


def is_letter(letter: str) -> bool:
    try:
        return letter.encode('ascii').isalpha()
    except:
        return False


def main():
    text_to_encode = 'the lazy dog jumped over the quick brown fox.'
    encoded_text = encode_text_by_letter_position(text_to_encode, 2)
    print(encoded_text)


if __name__ == '__main__':
    main()
