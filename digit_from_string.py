import re


def sum_from_string(texts: str) -> int:
    digits = find_digits_from_text(texts)
    return sum(digits)


def find_digits_from_text(texts: str) -> list[int]:
    temp = []
    for digit in re.findall(r'-?\d+', texts):
        try:
            temp.append(int(digit))
        except ValueError as e:
            print(e)
    return temp


if __name__ == "__main__":
    text = '-100#^sdfkj8902w3ir021@swf-20'
    print(sum_from_string(text))
