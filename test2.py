with open("HapMap.map")as file:
    lines=file.readlines()
    last=0
    count=0
    for line in lines:
        
        var=line.split()
        if last!=int(var[0]):
            last=int(var[0])
            print(count+6, end=" ")
            # print(last)
        count+=1

print(count)
        