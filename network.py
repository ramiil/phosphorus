import urllib3, certifi, random

class Network:

  nodes = {}
  q = urllib3.PoolManager(cert_reqs='CERT_REQUIRED',ca_certs=certifi.where())
  
  def __init__():
    pass

  def addNode(self, key, address):
    self.nodes[key]=address
    
  def pickRandomNode(self):
    return random.choice(nodes)

  def getData(self, node):
    try:
      return q.request('GET', node+"/data").data.decode("utf-8")
    except urllib3.exceptions.MaxRetryError:
      return "{'error': 'NodeUnreachable'}"
      
  def getChainsize(self, node):
    try:
      return q.request('GET', node+"/blockstat").data.decode("utf-8")
    except urllib3.exceptions.MaxRetryError:
      return "{'error': 'NodeUnreachable'}"

  def validateBlock(self, node, block):
    nonce = block['nonce']
    timestamp = block['nonce']
    fields = {'data': myData}
    try:    
      return q.request('POST', NODE+"/validate?nonce="+str(i)+"&timestamp="+str(myTimestamp), encode_multipart=False, multipart_boundary=None, fields = {'data': myData}).data.decode("utf-8")

    except urllib3.exceptions.MaxRetryError:
      return "{'error': 'NodeUnreachable'}"