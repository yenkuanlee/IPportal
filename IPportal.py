import hashlib
import io
import iota
from iota import TryteString
import ipfsapi
import json
IPFS_IP = '127.0.0.1'
IPFS_PORT = '5001'
class IPportal:
    def __init__(self, _ip,_groupkey):
        self.ip = _ip
        self.api = ipfsapi.connect(IPFS_IP,IPFS_PORT)
        self.groupkey = _groupkey
        self.GroupHash = self.api.object_put(io.BytesIO(json.dumps({"Data":_groupkey}).encode()))['Hash']
    def IPENCODE(self):
        X = ""
        tmp = self.ip.split(".")
        for x in tmp:
            for i in range(3):
                try:
                    X += chr(int(x[i])+65)
                except:
                    X += 'X'
        return X
    def IPDECODE(self,eip):
        X = ""
        for i in range(12):
            if i%3==0:
                X += "."
            if eip[i]=="X":
                continue
            X += str(ord(eip[i])-65)
        return X[1:]
    def GetKey(self):
        m = hashlib.md5()
        m.update(self.IPENCODE().encode('utf-8')+self.groupkey.encode('utf-8'))
        md5key = m.hexdigest()
        return str(TryteString.from_unicode(md5key))
    def GetAddress(self):
        return self.IPENCODE()+self.GetKey()+"KEVIN"
    def GetMessageFromAddress(self,address):
        Rdict = dict()
        #ip = self.IPDECODE(address[0:12])
        key = address[12:76]
        #Rdict['ip'] = ip
        Rdict['grouphash'] = self.GroupHash
        Rdict['peerid'] = self.api.id()['ID']
        return json.dumps(Rdict)
    def CheckPeer(self,address,message):
        Jmessage = json.loads(message)
        gkey = self.api.object_get(Jmessage['grouphash'])['Data']
        m = hashlib.md5(address[0:12].encode('utf-8')+gkey.encode('utf-8'))
        md5key = m.hexdigest()
        if TryteString.from_unicode(md5key) == address[12:76]:
            return True
        return False
    def GetConnectionInfo(self,address,message):
        Jmessage = json.loads(message)
        ip = self.IPDECODE(address[0:12])
        peerid = Jmessage['peerid']
        return "/ip4/"+ip+"/tcp/4001/ipfs/"+peerid
