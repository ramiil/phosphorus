import time, math, blockchain, sys
import urllib3, certifi

q = urllib3.PoolManager(cert_reqs='CERT_REQUIRED',ca_certs=certifi.where())

NODE = "http://127.0.0.1:1993"


def hashRate(hashNum, deltaTime):
  hRate = hashNum/(1+deltaTime)
  return str(round(hRate, 1))+" H/s"

i=0
totalBlocksFound = 0
totalHashed = 0
startTime = time.time()
myTimestamp = time.time()

myChain = blockchain.Blockchain({'data': '', 'prevBlockHash ': '', 'time': 946684800, 'nonce': 0})

try:
  myData=q.request('GET', NODE+"/data").data.decode("utf-8")
except urllib3.exceptions.MaxRetryError:
  print("Connection error")
  sys.exit()

try:
  while(True):
    myBlock = myChain.makeBlock(myData, myTimestamp, i)
    totalHashed += 1
    #print(myChain.getHash(myBlock))
    if(myChain.validateBlock(myBlock)):
      print('\nNew block found after', i,'attempts')
      isValidated = q.request('POST', NODE+"/validate?nonce="+str(i)+"&timestamp="+str(myTimestamp), encode_multipart=False, multipart_boundary=None, fields = {'data': myData}).data.decode("utf-8")
      if(isValidated=="{'applied': 'True'}"):
        myChain.applyBlock(myBlock)
        myTimestamp = time.time()
        myData=q.request('GET', NODE+"/data").data.decode("utf-8")
        totalBlocksFound += 1
      i = 0
      myABC = input("Enter new transaction data and press Enter\n")
    i+=1
except KeyboardInterrupt:
  print('\n')
  print("Statistics:")
  print("Total calculated:", totalHashed)
  print("Total blocks found:", totalBlocksFound)
  print("Tlme passed:", round(time.time()-startTime, 1), "sec.")
  print("Hashrate:", hashRate(totalHashed, time.time()-startTime))
  sys.exit()
#except:
#  print("Connection error")
#  sys.exit()