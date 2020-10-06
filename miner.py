import os, time, math, blockchain, sys, json, random
import urllib3, certifi

q = urllib3.PoolManager(cert_reqs='CERT_REQUIRED', ca_certs=certifi.where())

POOL = "http://192.168.1.100:1993"
WORKER = random.randint(10000, 99999)
USERNAME = 'Ramiil'

def cls():
    os.system('cls' if os.name=='nt' else 'clear')

class Miner():
  active = True
  totalBlocksFound = 0
  rejectedBlocks = 0
  totalHashed = 0
  startTime = 0
  localTimestamp = 0
  remoteData = None
  localChain = None

  def hashRate(self, hashNum, deltaTime):
    return round(hashNum/(1+deltaTime), 1)

  def statistics(self):
    cls()
    print("Statistics {0}@{1}".format(WORKER, USERNAME))
    print(" Total hashes:     ", self.totalHashed)
    print(" Applied/rejected: ", self.totalBlocksFound, self.rejectedBlocks)
    print(" Time passed:      ", round(time.time()-self.startTime), "sec.")
    print(" Hashrate:         ", str(self.hashRate(self.totalHashed, time.time()-self.startTime))+" H/s")
    print(" Complexity:       ", self.localChain.complexity)

  def getBlocksNumber(self):
    try:
      resp = q.request('GET', POOL+"/blockstat").data.decode("utf-8")
      return int(json.loads(resp)['count'])
    except urllib3.exceptions.MaxRetryError:
      print("Cannot communicate with server.")
      sys.exit()

  def setup(self):
    self.totalBlocksFound = 0
    self.totalHashed = 0
    self.startTime = time.time()
    self.localTimestamp = time.time()

  def register(self):
    try:
      resp = q.request('GET', POOL+"/join?username="+USERNAME+"&worker="+str(WORKER)).data.decode("utf-8")
    except urllib3.exceptions.MaxRetryError:
      print("Cannot communicate with server.")
      sys.exit()

  def unregister(self):
    try:
      resp = q.request('GET', POOL+"/leave?username="+USERNAME+"&worker="+str(WORKER)).data.decode("utf-8")
    except urllib3.exceptions.MaxRetryError:
      print("Cannot communicate with server.")
      sys.exit()

  def send_hashrate(self, hashrate):
    try:
      resp = q.request('GET', POOL+"/report_hashrate?username="+USERNAME+"&worker="+str(WORKER)+"&hashrate="+str(hashrate)).data.decode("utf-8")
    except urllib3.exceptions.MaxRetryError:
      print("Cannot communicate with server.")
      sys.exit()

  def load(self):
    self.localChain = blockchain.Blockchain()

    remoteBlocksCount = self.getBlocksNumber()

    try:
      print("Total blocks: {0}".format(remoteBlocksCount))
      for i in range(0, remoteBlocksCount, 10):
        resp = q.request('GET', POOL+"/blocks?start="+str(i)+"&count="+str(10)).data.decode("utf-8")
        for j in json.loads(resp):
          self.localChain.add(j['data'], j['prevBlockHash'], j['time'], j['nonce'])
    except urllib3.exceptions.MaxRetryError:
      print("Connection error")
      sys.exit()

    try:
      self.localChain.complexity = int(q.request('GET', POOL+"/complexity").data.decode("utf-8"))
      self.remoteData = q.request('GET', POOL+"/data").data.decode("utf-8")
    except urllib3.exceptions.MaxRetryError:
      print("Connection error")
      sys.exit()

  def run(self):
    self.load()
    print('Mining at {0} started'.format(POOL))
    while(True):
      avg_hashrate = (self.totalHashed // (time.time()-self.startTime))+1
      if (self.totalHashed%avg_hashrate==0):
        self.statistics()
        self.send_hashrate(avg_hashrate)
        if self.getBlocksNumber()>len(self.localChain.chain):
          self.load()
        self.localChain.complexity = int(q.request('GET', POOL+"/complexity").data.decode("utf-8"))

      nonce = random.randint(0, 65536)
      localBlock = self.localChain.makeBlock(self.remoteData, self.localTimestamp, nonce)
      self.totalHashed += 1
      if(self.localChain.validateBlock(localBlock)):

        try:
          validated = q.request('POST', POOL+"/validate?worker="+str(WORKER)+"&nonce="+str(nonce)+"&timestamp="+str(self.localTimestamp), encode_multipart=False, multipart_boundary=None, fields = {"data": self.remoteData}).data.decode("utf-8")
        except urllib3.exceptions.MaxRetryError:
          print("Connection error")
          sys.exit()

        if(validated=="{'applied': 'True'}"):
          self.localChain.applyBlock(localBlock)
          self.localTimestamp = int(time.time())
          self.remoteData=q.request('GET', POOL+"/data").data.decode("utf-8")
          self.localChain.complexity = int(q.request('GET', POOL+"/complexity").data.decode("utf-8"))
          self.totalBlocksFound += 1
        else:
          self.rejectedBlocks += 1
          self.load()


if __name__ == "__main__":
  miner = Miner()
  miner.setup()
  miner.register()
  try:
    miner.run()
  except KeyboardInterrupt:
    miner.unregister()
