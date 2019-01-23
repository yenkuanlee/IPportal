import iservstor
a = iservstor.iServStor()
print(a.GetSwarmPeers())
b = a.FileUpload('r.txt')
print(b)
c = a.CheckFileLocation(b)
print(c)
