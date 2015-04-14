
with open('big','w') as f:
    data = '0'*512
    for i in xrange(0,int(2e9),512):
        f.write(data)
    f.flush()
    
