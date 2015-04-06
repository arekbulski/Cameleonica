
data = '0'*51200 #50K
for i in xrange(10000):
    with open('container/%d' % i, 'w') as f:
        f.write(data)
        
