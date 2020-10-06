from http.server import BaseHTTPRequestHandler, HTTPServer
from multiprocessing import Process
from url_decode import urldecode
import sys, time, os, json, random, blockchain, base64

myChain = blockchain.Blockchain()
myChain.add("", "", time.time(), 0)

miners = {}

class rqHandler(BaseHTTPRequestHandler):
  global complexity_adjusted

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
      data = urldecode(self.rfile.read(int(self.headers['content-length'])).decode('utf-8')).split('=')[1]
      block = myChain.makeBlock(data, float(actions['timestamp']), int(actions['nonce']))
      if myChain.validateBlock(block):
        myChain.applyBlock(block)
        self.wfile.write("{'applied': 'True'}".encode("utf-8"))
        print(" BLOCK APPLIED")
      else:
        self.wfile.write("{'applied': 'False'}".encode("utf-8"))
        print(" BLOCK REJECTED")

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
    if(page=='/complexity'):
      self.wfile.write(str(myChain.getComplexity()).encode("utf-8"))

    if(page=='/totalhr'):
      totalhr = 0
      for miner in miners:
        for worker in miners[miner]:
          totalhr += float(miners[miner][worker]['hashrate'])
      self.wfile.write( json.dumps({"hashrate": totalhr}).encode("utf-8") )
    if(page=='/userhr'):
      userhr = 0
      for worker in miners[action['username']]:
        userhr += float(miners[action['username']][worker]['hashrate'])
      self.wfile.write( json.dumps({action['username']: totalhr}).encode("utf-8") )

    if(page=='/report_hashrate'):
      miners[actions['username']][actions['worker']]['hashrate'] = float(actions['hashrate'])

    if(page=='/blocks'):
      myOutput=json.dumps(myChain.chain[int(actions['start']):(int(actions['start'])+int(actions['count']))])
      self.wfile.write(myOutput.encode("utf-8"))
    if(page=='/blockstat'):
       blockstat = {"count": str(len(myChain.chain))}
       self.wfile.write(json.dumps(blockstat).encode("utf-8"))

    if(page=='/leave'):
      miners[actions['username']][actions['worker']] = None
    if(page=='/join'):
      if not actions['username'] in miners.keys():
        miners[actions['username']] = {}
      if not actions['worker'] in miners[actions['username']].keys():
        miners[actions['username']][actions['worker']] = {}
      else:
        miners[actions['username']][actions['worker']]['hashrate'] = 0.0
      self.wfile.write("{'OK': True}".encode("utf-8"))

    if(page=='/data'):
      data = {"user": random.randint(1, 1000)}
      self.wfile.write( json.dumps(data).encode("utf-8") )

HTTPServer(('0.0.0.0', int(1993)), rqHandler).serve_forever()
