
data = '0'*50100
for i in range(10000):
    with open('container/%d' % i, 'w') as f:
        f.write(data)
        
