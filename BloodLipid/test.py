b=open("BloodLipid/blood_lipid.ped")
lines=b.readlines()
b.close()
for j in range(100):
    found=lines[j].find("<")

    print(found)
    
    # var=lines[j].split("\t")
    
    # for i in range(230,250):
        # print(var[i])