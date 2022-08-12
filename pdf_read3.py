import pandas as pd
import pickle
import numpy as np
def save_obj(obj, name):
    with open(name + '.pkl', 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)


def load_obj(name):
    with open(name + '.pkl', 'rb') as f:
        return pickle.load(f)


zz=load_obj('无人机题库')
a=range(1,50)
zzz=str()
for i in zz.values():
    zzz=zzz+'\n'+i
res={}
part=[]
n=1
zhushi=str()
for i in zzz.splitlines():
    if len(i) != 0 and i[0] == '注':
        zhushi=zhushi+i


for i in zzz.splitlines():
    try:
        float(i[0])
        part.append(i)
    except:
        part.append(i)

        if len(i)!=0 and i[0]=='答':

            res[n]=part
            n=n+1
            part=[]
res2={}
n=1
part2=[]
for j in res.values():
    if j!=None:
        for ii in j[::-1]:
            if ii[0]=='第' and ii[-1]=='页':
                continue
            part2.append(ii)
            try:
                float(ii[0])
                # part2.append(ii)
                res2[n]=part2
                n=n+1
                part2=[]
                break
            except:
                pass
res3={}
b=[]
for i in res2.keys():
    b = []
    a=res[i]
    for aa in a:
        if len(aa)>0:
            if aa in res[i] and aa not in res2[i] and aa[0]!='第' and aa[-1]!='页':
                b.append(aa)
                res3[i]=b
res4={}
for i,j in res3.items():
    if j[0][0]=='注':
        res4[i]=j