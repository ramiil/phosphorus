import hsm, json, time

class Blockchain():

  MAX_COMPLEXITY = 24
  MIN_COMPLEXITY = 4
  MAX_TIME = 360

  chain = []
  complexity = 8

  def __init__(self, block=None):
    if block!=None:
    	self.update([block])

  def add(self, data, prevBlockHash, time, nonce):
    block = {"data":data, "prevBlockHash":prevBlockHash, "time":time, "nonce":nonce}
    self.chain.append(block)

  def update(self, subchain):
    for item in subchain:
      self.chain.append(item)

  def toBin(self, x):
    return "{0:0{1}b}".format(x,8)

  def getBlockTime(self):
    return self.chain[-1]['time'] - self.chain[-2]['time']

  def getLastBlockTime(self):
    return time.time() - self.chain[-1]['time']

  def setComplexity(self, complexity):
    if complexity>self.MAX_COMPLEXITY:
      self.complexity = self.MAX_COMPLEXITY
    elif complexity<self.MIN_COMPLEXITY:
      self.complexity = self.MIN_COMPLEXITY
    else:
      self.complexity = complexity

  def getComplexity(self):
    if len(self.chain)>2:
      last_block_time = self.getLastBlockTime()
      self.setComplexity(round(self.MAX_COMPLEXITY-((self.MAX_COMPLEXITY-self.MIN_COMPLEXITY)*(last_block_time/self.MAX_TIME))))
    else:
      self.setComplexity(8)

    return self.complexity


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

    return alphaStr[(byteNum*8)-self.complexity:] == betaStr[(byteNum*8)-self.complexity:]

  def getHash(self, block):
    return hsm.hsm(json.dumps(block))

  def getLastBlock(self):
    return self.chain[-1]

  def getJsonBlock(self, id):
    if (id<=len(self.chain)):
      return json.dumps(self.chain[id])
    else:
      return "{'error': 'IndexTooBig'}"

  def makeBlock(self, data, timestamp, nonce):
    prevBlockHash = self.getHash(self.getLastBlock())
    return {"data": data, "prevBlockHash": prevBlockHash , "time": int(timestamp), "nonce": nonce}

  def applyBlock(self, block):
    if self.validateBlock(block):
      self.chain.append(block)
      return True
    else:
      return False
