import math
try:
    print(math.log10(0.36))
except:
    print("fail")
txt="./k-fold/given50per_lbound_enf200_4/result7.txt"
print(txt.find("given"))
print(max((txt.find("bound_enf")),(txt.find("split")),(txt.find("shuffle"))))
print(txt[txt.find("given"):max((txt.find("bound_enf")),(txt.find("split")),(txt.find("shuffle")))])
