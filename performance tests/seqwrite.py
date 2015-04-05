
with open('big','w') as f:
    data = '0'*512
    for i in xrange(10**9/512):
        f.write(data)
        
