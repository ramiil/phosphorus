BSIZE = 4
HSIZE = 32

def xor(xs, ys):
  if type(ys)==list:
    return [x^y for x, y in zip(xs, ys)]
  else:
    return [(x^ys)%256 for x in xs]

def hsm(data):
  data = '$@1t3dW^t3r' +data + chr(0) * (HSIZE-(len(data)%HSIZE))
  data = [ord(x) for x in data]
  hashsum = 170
  text = [hashsum] * HSIZE
  blocks = []

  # Mixing input data
  for i in range(1, len(data)):
    data[i] = (data[i-1] ^ (data[i]+1) ^ i-1)%256

  # Split data to 4-byte blocks and mix bits with each other
  for i in range(0, (len(data)//BSIZE)):
    block = []
    A, B, C, D = data[i*BSIZE:(i+1)*BSIZE]
    block += [abs((A&B)|(~A&C))]
    block += [abs((B&C)|(~C&D))]
    block += [abs(C^D^A)>>3]
    block += [abs(A^(~B|D))]
    blocks += block[::pow(-1, i)]

  # Create raw text collapsing blocks using xor
  for i in range(0, (len(blocks)//HSIZE)):
    text = xor(text, blocks[i*HSIZE:(i+1)*HSIZE])
  
  # Generating unique value to xoring. Part of FAQ6
  for i in range(0, len(text)): 
    hashsum += text[i]
    hashsum += (hashsum << 16)
    hashsum ^= (hashsum >> 7)
  hashsum += (hashsum << 3)
  hashsum ^= (hashsum >> 11)
  hashsum += (hashsum << 15)

  # Mixing one more time
  for i in range(1, len(text)):
    text[i] = (text[i-1] ^ (text[i]+1) ^ i)%256

  # Finally xor each byte of text to integer
  result = xor(text, hashsum)[0:HSIZE]
  
  # And return it's as hex string
  return "".join(map(lambda x: "{0:0{1}x}".format(x,2), result))