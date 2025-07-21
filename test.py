with open("HapMap.ped")as file:
    lines=file.readlines()
    
    for line in lines:
        count=0
        var=line.split()
        for i in range(len(var)):
            if var[i]=="D"or var[i]=="I":
                print(i)
                count+=1
        print(count)
        
        break
def give(func):
    return func
print(give(lambda x: x+6)==None)
        