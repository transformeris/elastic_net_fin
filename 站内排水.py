
import numpy as np
from matplotlib import pyplot as plt
import pandas as pd
plt.rcParams['font.sans-serif']=['SimHei']
def rain_fall():
    '''

    :param P: 多少年一遇的多少，如50年一遇就是50
            t：分钟，降雨历时
            A：雨力
            b，n，：地方参数
    :return: q，数组，暴雨强度，单位：升/秒*公顷
    '''
    P=50
    if 1<=P<=10:
        n=0.827-0.18*np.log10(P-0.64)
        b=18.799-7.198*np.log10(P-0.247)
        A=29.9-10.903*np.log10(P-0.771)
    elif P>10:
        n=0.719-0.078*np.log10(P-4.527)
        b=13.953-4.138*np.log10(P-6.185)
        A=21.732-2.945*np.log10(P-6.737)
    elif P<1 or P>100:
        print('重现期大于100或小于1')
    t=np.arange(1,60)
    q=167*A/np.power((t+b),n)
    return q

def chaodi():
    ##地面入渗率
    t=np.arange(1,60)
    '''
    t:降雨时间，s
    fp:理论入渗率，mm/h
    f0：初始入渗率，mm/h
    fw：稳定入渗率，mm/h
    K：衰减系数，由土壤成分决定
    '''
    f0=76.2
    fw=3.81
    K=2.6
    fp=(f0-fw)*np.exp(-K*t)+fw  ##参数取文献基于swmm的滇池环湖截污。。。
    return fp

def rain_chicago(P,r):
    '''

    :param P: 多少年一遇
    :param r: 0到1，降雨的高峰时刻在整场雨的百分之几出现，如0.5就是在整场雨
    :return:
    '''
    if 1<=P<=10:
        n=0.827-0.18*np.log10(P-0.64)
        b=18.799-7.198*np.log10(P-0.247)
        A=29.9-10.903*np.log10(P-0.771)
    elif P>10:
        n=0.719-0.078*np.log10(P-4.527)
        b=13.953-4.138*np.log10(P-6.185)
        A=21.732-2.945*np.log10(P-6.737)
    t = np.arange(1, 60)
    before_peak=np.arange(1,np.ceil(r*len(t))+1)
    after_peak=np.arange(1,np.ceil(len(t))+1-np.ceil(r*len(t))+1)
    I1=A*((1-n)*before_peak/r+b)/(np.power((before_peak/r+b),n+1))
    I2 = A * ((1 - n) * after_peak / (1-r) + b) / (np.power((after_peak / (1-r) + b), n + 1))

    chicage_rain=np.concatenate((np.flipud(I1), I2), axis=0)

    q=167*A/np.power((t+b),n)
    rain=sum(q)/sum(chicage_rain)*chicage_rain/10000*60  ##/10000*60为单位换算，单位为降雨量，单位mm

    return rain

def water_sum(rain,S_grass,S_hard):
    z=np.cumsum(rain)

    zz=z*0.15*S_grass/1000+0.9*z*S_hard/1000
    return zz

def water_delta(rain,S_grass,S_hard):


    zz=rain*0.3*S_grass/1000+rain*S_hard/1000
    return zz

def water_change(Q,water,water_warn):
    n=1
    for i in water:
        if i<water_warn:
            n=n+1
        elif i>water_warn:
            break
    out_zero=np.zeros(n)
    water_up = np.arange(1, len(water)-n+1) * Q
    water_up2=np.concatenate((out_zero, water_up), axis=0)
    water_rest = water - water_up2
    t_water_out=water_rest[-1]/Q

    water_out=np.arange(1,np.ceil(t_water_out))*Q
    water_out=np.flipud(water_out)

    water_out_line=np.concatenate((water_rest,water_out), axis=0)
    return water_out_line


if __name__=='__main__':

    low=1
    H=5
    g=9.8
    power=3000
    Q=power*0.7/(low*H*g)/60

    q=rain_chicago(50,0.3)

    # w=water_sum(q, 3700,1900)

    Q=0.5
    water=water_sum(q, 892,472)
    water_warn=10
    n=1
    for i in water:
        if i<water_warn:
            n=n+1
        elif i>water_warn:
            break
    out_zero=np.zeros(n)
    water_up = np.arange(1, len(water)-n+1) * Q
    water_up2=np.concatenate((out_zero, water_up), axis=0)
    water_rest = water - water_up2
    t_water_out=water_rest[-1]/Q

    water_out=np.arange(1,np.ceil(t_water_out))*Q
    water_out=np.flipud(water_out)

    water_out_line=np.concatenate((water_rest,water_out), axis=0)

    for i in [0.5,1,1.5,2,2.5,3]:
        zz=water_change(i,water,10)
        print(i,max(zz))
        zz[zz<0]=0
        plt.plot(zz,label='Q=')

    # plt.plot(water)
    plt.xlabel('时间/分钟')
    plt.ylabel('累计雨水量/立方米')
    plt.show()

    # ##水泵
    #
    # t_start=20
    #
    #
    #
    # water_up=np.arange(1,61)*Q
    #
    # water_rest=w-water_up
    #
    # water_rest[water_rest<Q]=0
    # water_rest[-1]
    # t_water_out=water_rest[-1]/Q
    #
    # water_out=np.arange(1,np.ceil(t_water_out))*Q
    # water_out=np.flipud(water_out)
    #
    # water_out_line=np.concatenate((water_rest,water_out), axis=0)
    #
    # plt.plot(water_out_line)
    # plt.plot(w)
    # plt.show()





