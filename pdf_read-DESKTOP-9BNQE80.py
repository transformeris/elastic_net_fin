import pdfplumber
import pdfplumber.page
import pandas as pd

import pickle
def save_obj(obj, name):
    with open(name + '.pkl', 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)


def load_obj(name):
    with open(name + '.pkl', 'rb') as f:
        return pickle.load(f)
res={}
n=1
with pdfplumber.open(r'D:\onedrive\文档\WXWork Files\File\2023-04\图纸\图纸\500 千伏鳌峰开关站扩建第一台主变工程电气二次图纸\D0202\446-B50081S-D0202-19 主变小室监控交换机屏一端子排图.pdf') as pdf:
    print(pdfplumber.page.Page)
    zz=pdfplumber.page.Page

    for page in pdf.pages:
        # 获取当前页面的全部文本信息，包括表格中的文字,没有内容则打印None
        res[n]=page.extract_text()
        n=n+1
        print(page.extract_text())
# save_obj(res,'综合问答题库（多旋翼）')
#
# zz=load_obj('综合问答题库（多旋翼）')
# text=str()
# res={}
# zzz=[]
# for i,j in zz.items():
#     text=text+j
# aa=range(0,236)
# aaa=[]
# for i in aa:
#     aaa.append(str(i))
#
# res={}
# text2=str()
# from collections import Counter
# for n in text.splitlines():
#     z=n.replace(' ','')
#     text2=text2+z
# for i in range(1,236):
#     t1=text2.split(str(i)+'.')[1].split(str(i+1)+'.')[0]
#     res[i]=t1
# res_timu={}
# res_A={}
# res_B={}
# res_gabage={}
# res_C={}


#
# for i,j in res.items():
#     if 'A、' in j and j.count('A、')==1:
#         res_timu[i]=j.split('A、')[0]
#         res_A[i]=j.split('A、')[1].split('B、')[0]
#         res_B[i]=j.split('A、')[1].split('B、')[1].split('C、')[0]
#         res_C[i]=j.split('A、')[1].split('B、')[1].split('C、')[1]
#     else:
#         res_gabage[i]=j
# res_gabage2={}
# for i,j in res_B.items():
#     if '参' in j or '考' in j or '答' in j or '案' in j:
#         res_gabage2[i]=j
#         res_B[i]=j.split('参')[0]
#
#
# res_gabage3={}
# res_gabage4={}
# res_gabage5={}
# for i, j in res_C.items():
#     if '参' in j or '考' in j or '答' in j or '案' in j:
#         res_gabage3[i] = j
#         # res_C[i] = j.split('参')[0]
#         if '参考' in j:
#             res_C[i] = j.split('参考')[0]
#             res_gabage4[i]=j
#
#         if '参考答案' in j:
#             res_C[i] = j.split('参考答案')[0]
#         elif '考答案' in j:
#             res_C[i] = j.split('考答案')[0]
#         elif '答案' in j:
#             res_C[i] = j.split('答案')[0]
#         elif '案' in j:
#             res_C[i] = j.split('案')[0]
#         else:
#             res_gabage5[i] = j
#
# res_daan={}
# gabage_daan={}
# for i,j in res.items():
#     if i in res_timu.keys():
#         jj=j.replace(res_timu[i],'')
#         jjj=jj.replace(res_A[i],'')
#         jjjj = jjj.replace(res_B[i], '')
#         jjjjj = jjjj.replace(res_C[i], '')
#         a=jjjjj.count('A')
#         b = jjjjj.count('B')
#         c = jjjjj.count('C')
#         if a==2 and b==1 and c==1:
#             res_daan[i]='A'
#         elif b==2 and a==1 and c==1:
#             res_daan[i]='B'
#         elif c==2 and a==1 and b==1:
#             res_daan[i]='C'
#         else:
#             gabage_daan[i]=j
# for i,j in gabage_daan.items():
#     res_daan[i]=j[-1]
#     res_C[i]=res_C[i][0:-1]
# gabage_daan2={}
# for i,j in res.items():
#     if '参考答案：' in j:
#         daan=j.split('参考答案：')[1]
#         if len(daan)==1:
#             res_daan[i]=daan
#         elif daan[0]=='A' or daan[0]=='B' or daan[0]=='C':
#             res_daan[i] = daan[0]
#         else:
#             gabage_daan[i]=j
#
#     elif '考答案：' in j:
#         daan = j.split('考答案：')[1]
#         if len(daan) == 1:
#             res_daan[i] = daan
#     elif '答案：' in j:
#         daan = j.split('答案：')[1]
#         if len(daan) == 1:
#             print(daan)
#             res_daan[i] = daan
#     elif '案：' in j:
#         daan = j.split('案：')[1]
#         if len(daan) == 1:
#             print(daan)
#             res_daan[i] = daan
#     else:
# #         gabage_daan2[i]=j
# ec=pd.DataFrame()
# for i in res_timu.keys():
#     ec.loc[i,'题干']=res_timu[i]
#     ec.loc[i, '选项1'] = res_A[i]
#     ec.loc[i, '选项2'] = res_B[i]
#     ec.loc[i, '选项3'] = res_C[i]
# for i in res_daan.keys():
#     ec.loc[i, '答案'] = res_daan[i]
# ec.sort_index()
# ec.to_excel('综合问答3.xlsx')
    # for i in aaa:
    #     if i in n:
    #         res[i]=n
    # a=n.split('.  ')[0]
    # zzz.append(n)
    # try:
    #     float(a)
    #     res[a]=zzz
    #     zzz = []
    # except:
    #     pass

# a=range(1,50)
# zzz=str()
# for i in zz.values():
#     zzz=zzz+'\n'+i
# res={}
# part=[]
# n=1
# for i in zzz.splitlines():
#     try:
#         float(i[0])
#         part.append(i)
#     except:
#         part.append(i)
#
#         if len(i)!=0 and i[0]=='答':
#
#             res[n]=part
#             n=n+1
#             part=[]
# res2={}
# n=1
# part2=[]
# for j in res.values():
#     if j!=None:
#         for ii in j[::-1]:
#             if ii[0]=='第' and ii[-1]=='页':
#                 continue
#             part2.append(ii)
#             try:
#                 float(ii[0])
#                 # part2.append(ii)
#                 res2[n]=part2
#                 n=n+1
#                 part2=[]
#                 break
#             except:
#                 pass
#
#
# for i,j in res2.items():
#     for jj in j[1:-1]:
#         if jj[0]!='A' and jj[0]!='B' and jj[0]!='C':
#             pass
#             # print(i)
#             # print(jj)
#
#
# ec=pd.DataFrame()
# fau=[]
# res3={}
# res5={}
# res6={}
# for i,j in res2.items():
#     # ec.loc[i,'题目']=j[-1]
#
#     for da in j[0]:
#         if da in ['A','B','C','D']:
#             ec.loc[i,'答案']=da
#             break
#     if len(j)==5:
#         ec.loc[i, '题目'] = j[-1]
#         zz=j
#         if len(j[3].split('A'))>1:
#             ec.loc[i, '选项1'] = j[3].split('A')[1][1:]
#         else:
#             ec.loc[i, '选项1'] = j[3].split('A')[0]
#
#         if len(j[2].split('B'))>1:
#             ec.loc[i, '选项2'] = j[2].split('B')[1][1:]
#         else:
#             ec.loc[i, '选项2'] = j[2].split('B')[0]
#
#         if len(j[1].split('C'))>1:
#             ec.loc[i, '选项3'] = j[1].split('C')[1][1:]
#         else:
#             ec.loc[i, '选项3'] = j[1].split('C')[0]
#
#
#     elif len(j)==3:
#         res6[i]=j
#         ec.loc[i, '题目'] = j[-1]
#         if 'A' in j[1] and 'B' in j[1] and 'C' in j[1]:
#             a=j[1].split('B')[0].split('A')[1]
#             if a[0]=='．' or a[0]=='.':
#                 a=a[1:]
#             b=j[1].split('B')[1].split('C')[0]
#             if b[0]=='．' or b[0]=='.':
#                 b=b[1:]
#             c=j[1].split('B')[1].split('C')[1]
#             if c[0]=='．' or c[0]=='.':
#                 c=c[1:]
#             ec.loc[i, '选项1'] =a
#             ec.loc[i, '选项2'] =b
#             ec.loc[i, '选项3'] =c
#             zz=j
#         else:
#             a = j[1].split('B')[0]
#             if a[0]=='．' or a[0]=='.':
#                 a=a[1:]
#             b = j[1].split('B')[1].split('C')[0]
#             if b[0]=='．' or b[0]=='.':
#                 b=b[1:]
#             c = j[1].split('B')[1].split('C')[1]
#             if c[0]=='．' or c[0]=='.':
#                 c=c[1:]
#             ec.loc[i, '选项1'] =a
#             ec.loc[i, '选项2'] =b
#             ec.loc[i, '选项3'] =c
#             fau.append([j,a,b,c])
#     else:
#         res3[i] = j
#         timu=str()
#         for iii in j[::-1]:
#             if iii[0]=='A' :
#                 break
#             timu = timu + iii
#         xuanxiang = str()
#         for jjj in j[::-1]:
#
#             if jjj[0]=='A':
#                 print('fuck')
#                 xuanxiang=xuanxiang+jjj
#             if jjj[0] == 'B':
#                 xuanxiang = xuanxiang + jjj
#             if jjj[0] == 'C':
#                 xuanxiang = xuanxiang + jjj
#
#
#         if 'A．' in xuanxiang and 'B．' in xuanxiang and 'C．' in xuanxiang:
#
#             a=xuanxiang.split('A．')[1]
#             if a[0]=='．' or a[0]=='.':
#                 a=a[1:]
#             b=xuanxiang.split('B．')[1].split('C．')[0]
#             if b[0]=='．' or b[0]=='.':
#                 b=b[1:]
#             c=xuanxiang.split('B．')[1].split('C．')[1]
#             if c[0]=='．' or c[0]=='.':
#                 c=c[1:]
#         elif 'A.' in xuanxiang and 'B.' in xuanxiang and 'C.' in xuanxiang:
#             try:
#                 a=xuanxiang.split('A.')[1]
#                 if a[0]=='．' or a[0]=='.':
#                     a=a[1:]
#                 b=xuanxiang.split('B.')[1].split('C.')[0]
#                 if b[0]=='．' or b[0]=='.':
#                     b=b[1:]
#                 c=xuanxiang.split('B.')[1].split('C.')[1]
#                 if c[0]=='．' or c[0]=='.':
#                     c=c[1:]
#             except:
#                 res5[i] = j
#
#         elif 'A ' in xuanxiang and 'B ' in xuanxiang and 'C ' in xuanxiang:
#             try:
#                 a = xuanxiang.split('A ')[1]
#                 if a[0] == '．' or a[0] == '.':
#                     a = a[1:]
#                 b = xuanxiang.split('B ')[1].split('C ')[0]
#                 if b[0] == '．' or b[0] == '.':
#                     b = b[1:]
#                 c = xuanxiang.split('B ')[1].split('C ')[1]
#                 if c[0] == '．' or c[0] == '.':
#                     c = c[1:]
#             except:
#                 res5[i] = j
#         else:
#             res5[i]=j
#         ec.loc[i, '题目'] = timu
#         ec.loc[i, '选项1'] =a
#         ec.loc[i, '选项2'] =b
#         ec.loc[i, '选项3'] =c
#         zz=j
#
#
#     # else:
#     #     res3[i]=j
#
#
# res4={}
# for i,j in res3.items():
#     for jj in j:
#         if jj[0]=='A':
#             res4[i]=j
#
#     # try:
#     #     timujiaxuanxiang = str()
#     #     for iii in j[::-1]:
#     #         timujiaxuanxiang = timujiaxuanxiang + iii
#     #         if iii[0]=='A' :
#     #             break
#     #         else:
#     #             print([i,j,'没有'])
#     # except:
#     #     pass
#
#     #     timu = timujiaxuanxiang.split('A')[0]
#     #     shengyu = timujiaxuanxiang.split('A')[1]
#     #     a = shengyu.split('B')[0]
#     #     if a[0] == '.':
#     #         a = a[1:-1]
#     #     ec.loc[i, 'A'] = a
#     #     shengyu = shengyu.split('B')[1]
#     #
#     #     b = shengyu.split('C')[0]
#     #     if b[0] == '.':
#     #         b = b[1:-1]
#     #     ec.loc[i, 'B'] = b
#     #     shengyu = shengyu.split('C')[1]
#     #
#     #     c = shengyu.split('答案')[0]
#     #     if c[0] == '.':
#     #         c = c[1:]
#     #     ec.loc[i, 'C'] = c
#     # except:
#     #     fau.append([i,j])
# # z=res2[363]
# # timujiaxuanxiang=str()
# # for i in z[::-1]:
# #     timujiaxuanxiang=timujiaxuanxiang+i
# # timu=timujiaxuanxiang.split('A')[0]
# # shengyu=timujiaxuanxiang.split('A')[1]
# # a=shengyu.split('B')[0]
# # if a[0]=='.':
# #     a=a[1:-1]
# # shengyu=shengyu.split('B')[1]
# #
# # b=shengyu.split('C')[0]
# # if b[0]=='.':
# #     b=b[1:-1]
# # shengyu=shengyu.split('C')[1]
# #
# # c=shengyu.split('答案')[0]
# # if c[0]=='.':
# #     c=c[1:]
#
# # timujiaxuanxiang=timujiaxuanxiang.split('C')
# # timujiaxuanxiang=timujiaxuanxiang.split('答案')
# # for i in zz.values():
# #     for ii in a:
# #         pass
#         # if str(ii) in i:
#         #     part=i[str(ii):str(ii+1)]
#         # except:
#         #     pass