from string import ascii_uppercase


# Rotor numbers for the Wehrmacht
ROTOR_NUMS = {'I', 'II', 'III', 'IV', 'V'}


# Reflectors used by the Wehrmacht
REFLECTORS = {
  'B': 'YRUHQSLDPXNGOKMIEBFZCWVJAT',
  'C': 'FVPJIAOYEDRZXWGCTKUQSBNMHL',
}


# Internal wirings for each rotor, going forward and backwards
ROTOR_WIRINGS = {
  'I': {
    'forward': 'EKMFLGDQVZNTOWYHXUSPAIBRCJ',
    'backward': 'UWYGADFPVZBECKMTHXSLRINQOJ',
  },
  'II': {
    'forward': 'AJDKSIRUXBLHWTMCQGZNPYFVOE',
    'backward': 'AJPCZWRLFBDKOTYUQGENHXMIVS',
  },
  'III': {
    'forward': 'BDFHJLCPRTXVZNYEIWGAKMUSQO',
    'backward': 'TAGBPCSDQEUFVNZHYIXJWLRKOM',
  },
  'IV': {
    'forward': 'ESOVPZJAYQUIRHXLNFTGKDCMWB',
    'backward': 'HZWVARTNLGUPXQCEJMBSKDYOIF',
  },
  'V': {
    'forward': 'VZBRGITYUPSDNHLXAWMJQOFECK',
    'backward': 'QCYLXWENFTZOSMVJUDKGIARPHB',
  },
}


# Rotor notches for each rotor
ROTOR_NOTCHES = {
  'I': 'Q',   # If rotor steps from Q -> R, the next rotor is advanced
  'II': 'E',  # If rotor steps from E -> F, the next rotor is advanced
  'III': 'V', # If rotor steps from V -> W, the next rotor is advanced
  'IV': 'J',  # If rotor steps from J -> K, the next rotor is advanced
  'V': 'Z',   # If rotor steps from Z -> A, the next rotor is advanced
}


ALPHABET = ascii_uppercase


class Rotor:
  def __init__(self, rotor_num, window, prev_rotor=None):
    if rotor_num not in ROTOR_NUMS:
      raise Exception('Rotor number must be I, II, III, IV, or V')
    self.wiring = ROTOR_WIRINGS[rotor_num]
    self.notch = ROTOR_NOTCHES[rotor_num]
    self.window = window.upper()
    self.offset = ALPHABET.index(self.window)
    self.next_rotor = None
    self.prev_rotor = prev_rotor

  def step(self):
    if self.next_rotor and self.window == self.notch:
      self.next_rotor.step()
    self.offset = (self.offset + 1) % 26
    self.window = ALPHABET[self.offset]
  
  def encipher_letter(self, letter, forward):
    key = 'forward' if forward else 'backward'
    index = ALPHABET.index(letter.upper())
    encoded_letter = self.wiring[key][(index + self.offset) % 26]
    encoded_index = (ALPHABET.index(encoded_letter) - self.offset) % 26
    # going forward
    if self.next_rotor and forward:
      return self.next_rotor.encipher_letter(ALPHABET[encoded_index], forward)
    # going backwards
    elif self.prev_rotor and not forward:
      return self.prev_rotor.encipher_letter(ALPHABET[encoded_index], forward)
    # all done going forward or backwards
    else:
      return ALPHABET[encoded_index]
  

class Reflector:
  def __init__(self, reflector):
    if reflector in REFLECTORS.keys():
      self.wiring = str.maketrans(ALPHABET, REFLECTORS[reflector])
    else:
      raise Exception('Reflector type must be B or C')

  def __getitem__(self, letter):
    letter = letter.upper()
    return letter.translate(self.wiring)


class Plugboard:
  def __init__(self, swaps=None):
    self.swaps = {}
    if swaps is not None and len(swaps) <= 10:
      for swap in swaps:
        self.swaps[swap[0]] = swap[1]
        self.swaps[swap[1]] = swap[0]

  def __repr__(self):
    return self.swaps.__repr__()

  def __getitem__(self, letter):
    return self.swaps.get(letter, letter)
