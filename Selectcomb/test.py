file = open("Selectcomb/l_0/givengroup300_0//result300.txt")
lines=file.readlines()
for i in range(-4-int(lines[1]),-4):
    ele= lines[i].split(sep=',')
    ele[0], ele[-1]=ele[0][1:], ele[-1][:-2]
    print(ele)
    for e in range(len(ele)):
        
        print(ele[e], "why", )
file.close()

print(int(str(9.5)))