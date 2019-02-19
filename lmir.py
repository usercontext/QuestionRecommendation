queryq = "What is the step by step guide to invest in share market in india"

def lmir(w, Q):

    Qlist = Q.split()
    return Clist.count(w)/len(Clist)

def pml(w, C):
    Clist = C.split()
    return Clist.count(w)/len(Clist)

LAMBDA = 0.2

with open("tags.txt", "r") as f:
    data = [' '.join(i.split('\t')[0].split('-')).lower() for i in f.readlines()]

# print(data[10])
collection = ' '.join(data)
muls = []
Clist = collection.split()
lenClist = len(Clist)

for candidate in data:
    mul = 1.0
    # print("Hello")
    Qlist = candidate.split()
    lenQlist = len(Qlist)
    for w in queryq.lower().split(' '):
        try:
            mul *= (1-LAMBDA) * Qlist.count(w)/lenQlist + LAMBDA * Clist.count(w)/lenClist
        except:
            pass
        # print(candidate, pml(w, candidate), pml(w, collection))
        # if pml(w, collection) == 0:
        #     print(w)
    print(mul)
    muls.append((mul, candidate))

muls.sort(key=lambda tup: tup[0], reverse=True)
for i in muls[:10]:
    print(i[1])