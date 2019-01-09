import iota
from iota import TryteString
import json
import os
import requests
import signal
Cpath = os.path.dirname(os.path.realpath(__file__))
with open(Cpath+'/config.json') as f:
    Jconfig = json.load(f)
class IOTATransaction:
    def __init__(self, _MySeed):
        signal.signal(signal.SIGALRM, self.handler)
        self.MySeed = str.encode(_MySeed)
        self.FinalBundle = "INIT"
        self.TransactionHashList = list()
        self.Gateway = 'null'
        self.GetGateway()
        if self.Gateway == 'null':
            exit('No Good Gateway')
        self.api = iota.Iota(self.Gateway)
    def handler(self,signum, frame):
        raise Exception("end of time")
    def GetGateway(self):
        Glist = Jconfig['Gateway']
        for x in Glist:
            try:
                print(x)
                self.Gateway = x
                self.GetTransactionsFromTag('KEVIN999IS999HANDSOME')
                break
            except Exception as e:
                print(str(e))
                continue
    def MakePreparingTransaction(self, TargetAddress, StringMessage, tag='KEVIN999IS999HANDSOME'):
        TargetAddress = str.encode(TargetAddress)
        pt = iota.ProposedTransaction(address = iota.Address(TargetAddress),message = iota.TryteString.from_unicode(StringMessage),tag = iota.Tag(str.encode(tag)),value=0)
        return pt
    def SendTransaction(self, PTList, dep=Jconfig['dep'], mwm=Jconfig['mwm']):
        FinalBundle = self.api.send_transfer(depth=dep,transfers=PTList,min_weight_magnitude=mwm)['bundle']
        self.FinalBundle = FinalBundle
        for txn in FinalBundle:
            Vtxn = vars(txn)
            if Vtxn['hash'] not in self.TransactionHashList:
                self.TransactionHashList.append(Vtxn['hash'])
        
    def GetTransactionFinalBundleHash(self):
        return self.FinalBundle.hash
    def GetTransactionFinalBundle(self):
        return self.FinalBundle
    def GetTransactionHash(self):
        return self.TransactionHashList
    def GetTransactionMessage(self, TID):
        bundle = self.api.get_bundles(TID)
        Rdict = dict()
        for x in bundle['bundles']:
            for txn in x:
                Vtxn = vars(txn)
                if Vtxn['hash'] != TID:
                    continue
                address = str(Vtxn['address'])
                TryteStringMessage = str(Vtxn['signature_message_fragment'])
                message = TryteString(str.encode(TryteStringMessage)).decode()
                Rdict['address'] = address
                Rdict['message'] = message
                Rdict['timestamp'] = str(Vtxn['timestamp'])
                #return address,message
                return Rdict
    def GetTransactionsFromTag(self,tag):
        try:
            signal.alarm(Jconfig['GatewayTimeout'])
            headers = {'content-type': 'application/json','X-IOTA-API-Version': '1'}
            f = {"command": "findTransactions", "tags": [tag]}
            r = requests.post(self.Gateway, data=json.dumps(f), headers=headers)
            return json.loads(r.text)['hashes']
        except:
            return {"status": "Failed"}
