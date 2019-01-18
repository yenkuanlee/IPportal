import bchain
import sys
a = bchain.Bchain()
method = sys.argv[1]

if method=='register':
    print(a.register(sys.argv[2]))
