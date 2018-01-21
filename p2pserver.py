from http.server import BaseHTTPRequestHandler, HTTPServer
from multiprocessing import Process
from url_decode import urldecode
import sys, time, os, json, random, blockchain, base64

DBG_VAL = 'myDBGval'

nodes = {}
#nodes[DBG_VAL]='127.0.0.1'
nodes[0] = DBG_VAL

newData = {}
newData[DBG_VAL]={DBG_VAL : '1'}

myChain = blockchain.Blockchain({'data': '', 'prevBlockHash ': '', 'time': 946684800, 'nonce': 0})

class rqHandler(BaseHTTPRequestHandler):
  def do_HEAD(self):
    self.send_response(200)
    self.send_header('Content-type', 'text/json')
    self.send_header('Access-Control-Allow-Origin', '*')
    self.end_headers()

  def do_POST(self):
    self.do_HEAD()
    actions = {}
    try:
      page, acts = self.path.split("?")
      for item in acts.split('&'):
        actions[item.split('=')[0]] = item.split('=')[1]
    except ValueError:
      page=self.path

    if(page=='/validate'):
      pass
      data = urldecode(self.rfile.read(int(self.headers['content-length'])).decode('utf-8')).split('=')[1]
      block = myChain.makeBlock(data, float(actions['timestamp']), int(actions['nonce']))
      if myChain.validateBlock(block):
        myChain.applyBlock(block)
        self.wfile.write("{'applied': 'True'}".encode("utf-8"))
        print("BLOCK APPLIED")
      else:
        self.wfile.write("{'applied': 'False'}".encode("utf-8"))
        print("BLOCK NOT APPLIED")

  def do_GET(self):
    self.do_HEAD()
    actions = {}
    try:
      page, acts = self.path.split("?")
      for item in acts.split('&'):
        actions[item.split('=')[0]] = item.split('=')[1]
    except ValueError:
      page=self.path

    if(page=='/time'):
      self.wfile.write(str(time.time()).encode("utf-8"))
    if(page=='/nodes'):
      self.wfile.write(str(nodes).encode("utf-8"))
    if(page=='/node'):
      try:
        self.wfile.write(str(nodes[actions['key']]).encode("utf-8"))
      except KeyError:
        self.wfile.write('{}'.encode("utf-8"))
    if(page=='/blocks'):
      myOutput =[myChain.getJsonBlock(i) for i in range(int(actions['start']), int(actions['start'])+int(actions['count'])) ] 
      self.wfile.write(('{'+','.join(myOutput)+'}').encode("utf-8"))
    if(page=='/blockstat'):
       self.wfile.write(("{ 'count':'"+str(len(myChain.chain))+"'}").encode("utf-8"))
    if(page=='/join'):
      nodes.update(actions)
      self.wfile.write("{'OK': True}".encode("utf-8"))
    if(page=='/data'):
      self.wfile.write(str(newData).encode("utf-8"))


HTTPServer(('127.0.0.1', int(1993)), rqHandler).serve_forever()