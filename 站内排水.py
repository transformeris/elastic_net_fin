
import numpy as np
from matplotlib import pyplot as plt
import pandas as pd

def rain_fall(P):
    '''

    :param P: 多少年一遇的多少，如50年一遇就是50
            t：分钟，降雨历时
            A：雨力
            b，你，：地方参数
    :return: q，数组，暴雨强度，单位：升/秒*公顷
    '''
    P=3
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
    t=np.arange(1,24)
    q=167*A/np.power((t+b),n)
    return q

if __name__=='__main__':
