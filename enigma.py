import re 
from parts import Rotor, Reflector, Plugboard


class Enigma:
  def __init__(self, rotor_nums=['I','II','III'], windows='AAA', reflector_type='B', swaps=None):
    if len(windows) != 3:
      raise Exception('Must provide 3 starting letters for the rotors')
    self.right_rotor = Rotor(rotor_nums[2], windows[2])
    self.mid_rotor = Rotor(rotor_nums[1], windows[1], self.right_rotor)
    self.left_rotor = Rotor(rotor_nums[0], windows[0], self.mid_rotor)
    self.reflector = Reflector(reflector_type)
    self.plugboard = Plugboard(swaps)

    self.mid_rotor.next_rotor = self.left_rotor
    self.right_rotor.next_rotor = self.mid_rotor

  def encipher(self, msg):
    msg = msg.replace(' ', '')
    valid = re.search(r'^[a-zA-Z]+$', msg)
    if not valid:
      raise Exception('Message can only contain a-z or A-Z')
    return ''.join([self.encipher_decipher_letter(c) for c in msg])

  def decipher(self, msg):
    return self.encipher(msg)

  def encipher_decipher_letter(self, letter):
    swapped = self.plugboard[letter]
    self.right_rotor.step()
    forward = self.right_rotor.encipher_letter(letter, forward=True)
    reflected = self.reflector[forward]
    final = self.left_rotor.encipher_letter(reflected, forward=False)
    return self.plugboard[final]
