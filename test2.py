# with open("HapMap.ped")as file:
#     lines=file.readlines()
#     last=0
#     count=0
#     for line in lines:
        
#         var=line.split()
#         print((var[1]))
#         if "5" in var[1] or "9" in var[1] :
#             count+=1
# print(count)



with open("HapMap.ped")as file:
    lines=file.readlines()
    last=0
    count=0
    for line in lines:
        
        var=line.split('\t')
        print((var[-10:]))
        
print(count)