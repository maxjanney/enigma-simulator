from enum import Enum, auto
from string import ascii_lowercase


class Mode(Enum):
  ENCRYPTING = auto()
  DECRYPTING = auto()


def caesar(text, k, mode):
  alphabet = ascii_lowercase
  shifted = alphabet[k:] + alphabet[:k]
  if mode is Mode.ENCRYPTING:
    table = str.maketrans(alphabet, shifted)
  else:
    table = str.maketrans(shifted, alphabet)
  return text.translate(table)


text = 'super secret message'
cipher = caesar(text, 5, Mode.ENCRYPTING)
print(text, '->', cipher)
