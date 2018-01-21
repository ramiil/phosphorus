import hsm, json

class Blockchain():
  chain = []
  complexity = 6

  def __init__(self, block):
    self.updateChain([block])

  def updateChain(self, subchain):
    for item in subchain:
      self.chain.append(item)

  def toBin(self, x):
    return "{0:0{1}b}".format(x,8)

  def validateBlock(self, newBlock, prevBlock=False):
    alpha, beta = '', ''
    if not(prevBlock):
      prevBlock = self.getLastBlock()
    byteNum=(self.complexity//8)+1
    
    alpha = self.getHash(newBlock)[len(alpha)-byteNum:]
    beta = self.getHash(prevBlock)[:byteNum]

    alphaStr=''
    betaStr=''

    for i in alpha:
      alphaStr+=self.toBin(i)
    for i in beta:
      betaStr+=self.toBin(i)

    print(alphaStr[(byteNum*8)-self.complexity:], betaStr[(byteNum*8)-self.complexity:])
    return alphaStr[(byteNum*8)-self.complexity:] == betaStr[(byteNum*8)-self.complexity:]

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
    return {'data': data, 'prevBlockHash': prevBlockHash , 'time': int(timestamp), 'nonce': nonce}

  def applyBlock(self, block):
    if self.validateBlock(block):
      self.chain.append(block)
      return True
    else:
      return False