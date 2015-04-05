
data = '0'*10
for i in range(200000):
    with open('container/%d' % i, 'w') as f:
        f.write(data)
        
