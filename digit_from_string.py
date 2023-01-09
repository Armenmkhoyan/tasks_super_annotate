import re


def find_digit_from_string(text: str) -> list[int]:
    temp = []
    for digit in re.findall(r'-?\d+', text):
        try:
            temp.append(int(digit))
        except:
            pass
    return temp


if __name__ == "__main__":
    text = '-100#^sdfkj8902w3ir021@swf-20'
    print(sum(find_digit_from_string(text)))
