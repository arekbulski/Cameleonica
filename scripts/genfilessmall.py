data = '0' * 51200 #50KB
for i in xrange(10000): #10K
    with open('files/%d' % i, 'w') as f:
        f.write(data)
