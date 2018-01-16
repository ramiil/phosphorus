import hsm, json

class Blockchain():
  chain = []
  complexity = 3

  def __init__(self, block):
    self.updateChain([block])

  def updateChain(self, subchain):
    for item in subchain:
      self.chain.append(item)

  def toBin(self, x):
    return "{0:0{1}b}".format(x,8)

  def validateBlock(self, newBlock, prevBlock=False):
    if not(prevBlock):
      prevBlock = self.getLastBlock()
    byteNum=(complexity//8)+1
    alpha = self.getHash(newBlock)[len(alpha)-byteNum:]
    beta = self.getHash(prevBlock)[:byteNum]

    alphaStr=''
    betaStr=''

    for i in alpha:
      alphaStr+=toBin(i)
    for i in beta:
      betaStr+=toBin(i)

    return alphaStr[(byteNum*8)-complexity:] == betaStr[(byteNum*8)-complexity:]

  def getHash(self, block):
    return hsm.hsm(json.dumps(block))
    
  def getLastBlock(self):
    return self.chain[len(self.chain)-1]
    
  def getJsonBlock(self, id):
    if (id<=len(self.chain)):
      return json.dumps(self.chain[id])
    else:
      return "{'error': 'IndexTooBig'}"

  def makeBlock(self, data, timestamp, nonce):
    prevBlockHash = self.getHash(self.getLastBlock())
    return {'data': data, 'prevBlockHash': prevBlockHash , 'time': timestamp, 'nonce': nonce}

  def applyBlock(self, block):
    if self.validateBlock(block):
      self.chain.append(block)
      return True
    else:
      return False