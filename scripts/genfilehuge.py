with open('file1','w') as f:
    data = '0' * 512
    for i in xrange(0, 2*1024**3, 512):
        f.write(data)
