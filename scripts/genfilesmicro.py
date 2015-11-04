
data = '0' * 10  #just 10 bytes should fit within inode
for i in xrange(200000):  #200K
    with open('container/%d' % i, 'w') as f:
        f.write(data)
