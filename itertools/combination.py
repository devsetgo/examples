import itertools
from tqdm import tqdm
import time
t0 = time.time()
it = ["a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z"]

count=1
combo=[]
for i in tqdm(it):
    x = list(itertools.combinations(it, count))
    # print(x)
    count+=1
    combo.append(x)

c2 = 0
for com in tqdm(combo):
    for c in com:
        c2 +=2

print(c2)
t1 = time.time()-t0
print(f"it took {t1:.2f} seconds")