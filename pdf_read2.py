import pdfplumber
import pdfplumber.page
import pandas as pd
import pickle
import numpy as np
def save_obj(obj, name):
    with open(name + '.pkl', 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)


def load_obj(name):
    with open(name + '.pkl', 'rb') as f:
        return pickle.load(f)


zz=load_obj('综合问答题库（多旋翼）')
a=range(1,50)
zzz=str()
for i in zz.values():
    zzz=zzz+'\n'+i
res={}
part=[]
n=1
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
for i,j in res.items():
    if j!=None:
        for ii in j[::-1]:
            if ii[0]=='第' and ii[-1]=='页':
                continue
            part2.append(ii)
            try:
                float(ii[0])
                # part2.append(ii)
                res2[i]=part2
                n=n+1
                part2=[]
                break
            except:
                pass

ec=pd.DataFrame()
fau=[]
res3={}
res5={}
res6={}
for i,j in res2.items():
    # ec.loc[i,'题目']=j[-1]

    for da in j[0]:
        if da in ['A','B','C','D']:
            ec.loc[i,'答案']=da
            break

res3[i] = j

for i,j in res2.items():
    timu = str()
    for iii in j[::-1]:
        if iii[0]=='A' :
            break
        timu = timu + iii
    xuanxiang = str()
    for jjj in j[::-1]:

        if jjj[0]=='A':
            xuanxiang=xuanxiang+jjj
        if jjj[0] == 'B':
            xuanxiang = xuanxiang + jjj
        if jjj[0] == 'C':
            xuanxiang = xuanxiang + jjj


    if 'A．' in xuanxiang and 'B．' in xuanxiang and 'C．' in xuanxiang:

        a=xuanxiang.split('A．')[1].split('B．')[0]
        if a[0]=='．' or a[0]=='.':
            a=a[1:]
        b=xuanxiang.split('B．')[1].split('C．')[0]
        if b[0]=='．' or b[0]=='.':
            b=b[1:]
        c=xuanxiang.split('B．')[1].split('C．')[1]
        if c[0]=='．' or c[0]=='.':
            c=c[1:]
        ec.loc[i, '题目'] = timu
        ec.loc[i, '选项1'] = a
        ec.loc[i, '选项2'] = b
        ec.loc[i, '选项3'] = c
    elif 'A.' in xuanxiang and 'B.' in xuanxiang and 'C.' in xuanxiang:
        try:
            a=xuanxiang.split('A.')[1].split('B.')[0]
            if a[0]=='．' or a[0]=='.':
                a=a[1:]
            b=xuanxiang.split('B.')[1].split('C.')[0]
            if b[0]=='．' or b[0]=='.':
                b=b[1:]
            c=xuanxiang.split('B.')[1].split('C.')[1]
            if c[0]=='．' or c[0]=='.':
                c=c[1:]
            ec.loc[i, '题目'] = timu
            ec.loc[i, '选项1'] = a
            ec.loc[i, '选项2'] = b
            ec.loc[i, '选项3'] = c
        except:
            res5[i] = j

    elif 'A ' in xuanxiang and 'B ' in xuanxiang and 'C ' in xuanxiang:
        try:
            a = xuanxiang.split('A ')[1].split('B ')[0]
            if a[0] == '．' or a[0] == '.':
                a = a[1:]
            b = xuanxiang.split('B ')[1].split('C ')[0]
            if b[0] == '．' or b[0] == '.':
                b = b[1:]
            c = xuanxiang.split('B ')[1].split('C ')[1]
            if c[0] == '．' or c[0] == '.':
                c = c[1:]
            ec.loc[i, '题目'] = timu
            ec.loc[i, '选项1'] = a
            ec.loc[i, '选项2'] = b
            ec.loc[i, '选项3'] = c
        except:
            res5[i] = j

    elif 'A．' in xuanxiang and 'B.' in xuanxiang and 'C.' in xuanxiang:
        try:
            a=xuanxiang.split('A．')[1].split('B.')[0]
            if a[0]=='．' or a[0]=='.':
                a=a[1:]
            b=xuanxiang.split('B.')[1].split('C.')[0]
            if b[0]=='．' or b[0]=='.':
                b=b[1:]
            c=xuanxiang.split('B.')[1].split('C.')[1]
            if c[0]=='．' or c[0]=='.':
                c=c[1:]
            ec.loc[i, '题目'] = timu
            ec.loc[i, '选项1'] = a
            ec.loc[i, '选项2'] = b
            ec.loc[i, '选项3'] = c
        except:
            res5[i] = j

    elif 'A、' in xuanxiang and 'B、' in xuanxiang and 'C、' in xuanxiang:
        try:
            a=xuanxiang.split('A、')[1].split('B、')[0]
            if a[0]=='．' or a[0]=='.':
                a=a[1:]
            b=xuanxiang.split('B、')[1].split('C、')[0]
            if b[0]=='．' or b[0]=='.':
                b=b[1:]
            c=xuanxiang.split('B、')[1].split('C、')[1]
            if c[0]=='．' or c[0]=='.':
                c=c[1:]
            ec.loc[i, '题目'] = timu
            ec.loc[i, '选项1'] = a
            ec.loc[i, '选项2'] = b
            ec.loc[i, '选项3'] = c
        except:
            res5[i] = j

    elif 'B.' in xuanxiang and 'C.' in xuanxiang and 'A.' not in xuanxiang:
        try:
            a=xuanxiang.split('B.')[0]
            if a[0]=='．' or a[0]=='.':
                a=a[1:]
            b=xuanxiang.split('B.')[1].split('C.')[0]
            if b[0]=='．' or b[0]=='.':
                b=b[1:]
            c=xuanxiang.split('B.')[1].split('C.')[1]
            if c[0]=='．' or c[0]=='.':
                c=c[1:]
            ec.loc[i, '题目'] = timu
            ec.loc[i, '选项1'] = a
            ec.loc[i, '选项2'] = b
            ec.loc[i, '选项3'] = c
        except:
            res5[i] = j

    elif 'A' in xuanxiang and 'B' in xuanxiang and 'C' in xuanxiang:
        try:
            a = xuanxiang.split('A')[1].split('B')[0]
            if a[0] == '．' or a[0] == '.':
                a = a[1:]
            b = xuanxiang.split('B')[1].split('C')[0]
            if b[0] == '．' or b[0] == '.':
                b = b[1:]
            c = xuanxiang.split('B')[1].split('C')[1]
            if c[0] == '．' or c[0] == '.':
                c = c[1:]
            ec.loc[i, '题目'] = timu
            ec.loc[i, '选项1'] = a
            ec.loc[i, '选项2'] = b
            ec.loc[i, '选项3'] = c
        except:
            res5[i] = j

    elif len(xuanxiang)>0 and xuanxiang[0]!='A' and 'B' in xuanxiang and 'C' in xuanxiang:
        try:
            a = xuanxiang.split('B')[0]
            if a[0] == '．' or a[0] == '.':
                a = a[1:]
            b = xuanxiang.split('B')[1].split('C')[0]
            if b[0] == '．' or b[0] == '.':
                b = b[1:]
            c = xuanxiang.split('B')[1].split('C')[1]
            if c[0] == '．' or c[0] == '.':
                c = c[1:]
            ec.loc[i, '题目'] = timu
            ec.loc[i, '选项1'] = a
            ec.loc[i, '选项2'] = b
            ec.loc[i, '选项3'] = c
        except:
            res5[i] = j

    elif len(j)==3:


        if 'A' not in j[1] and 'B' in j[1] and 'C' in j[1]:
            a=j[1].split('B')[0]
            if a[0]=='．' or a[0]=='.':
                a=a[1:]
            b=j[1].split('B')[1].split('C')[0]
            if b[0]=='．' or b[0]=='.':
                b=b[1:]
            c=j[1].split('B')[1].split('C')[1]
            if c[0]=='．' or c[0]=='.':
                c=c[1:]
            ec.loc[i, '题目'] = timu
            ec.loc[i, '选项1'] =a
            ec.loc[i, '选项2'] =b
            ec.loc[i, '选项3'] =c
    elif len(j)==5:
        a=j[3]
        b=j[2]
        c=j[1]
        ec.loc[i, '题目'] = timu
        ec.loc[i, '选项1'] = a
        ec.loc[i, '选项2'] = b
        ec.loc[i, '选项3'] = c

    else:
        res5[i]=j

    ec.isna()
    ec[ec.isnull()]
    # zzzzzzz=np.where(ec.where==np.nan)
    zzzzzzz=np.where(ec.isna())
    A=len(set(zzzzzzz[0]))
    # ec.to_excel('无人机题库.xlsx')
    ec1=ec[1:]


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
res8={}
part=[]
for i,j in res.items():
    for n in range(0,len(j)):
        if len(j[n])>0 and j[n][0]=='注':
            part.append(n)
        try:
            if j[n] in ec.loc[i,'题目']:
                part.append(n)
        except:
            print('cuowu')
    if len(part)==2:
        res8[i]=j[part[0]:part[1]]
    else:
        print('youcuo')




# res9={}
# for i,j in res.items():
#     zhushi = []
#     flag=0
#     for jj in j:
#
#         if len(jj)>0 and jj[0]=='注':
#
#             flag=1
#
#         elif i!=1041 and jj in ec.loc[i,'题目']:
#             res9[i]=zhushi
#             flag=0
#             continue
#
#         if flag==1:
#             zhushi.append(jj)
