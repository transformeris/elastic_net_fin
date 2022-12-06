import tkinter as tk
import tkinter.messagebox as msg

top = tk.Tk()
top.title("计算器")
nScreenWid, nScreenHei = top.maxsize()
top.geometry("210x180+{}+{}".format(int(nScreenWid / 2 - 155), int(nScreenHei / 2 - 90)))
bo = 0
v = tk.StringVar()


def num(i):
    global bo
    if bo == 1:
        v.set('')
        bo = 0
    v.set(v.get() + i)


def calc(x=0):
    global bo
    try:
        v.set(eval(v.get()))
        bo = 1
    except:
        msg.showinfo("错误", "请检查输入的内容")


# 以下是按钮的布局,同时绑定了相应事件,对输入输入框绑定了回车事件
tke = tk.Entry(top, textvariable=v)
tke.grid(row=0, column=0, columnspan=3, sticky='NEW')
tke.bind("<Return>", calc)
tk.Button(top, text='   C   ', command=lambda: v.set('')).grid(row=0, column=3, sticky='NEW')
st = ["7", "8", "9", "/", "4", "5", "6", "*", "1", "2", "3", "-", "0", ".", "+", "="]
for i in range(15):
    tk.Button(top, text=st[i], command=lambda x=st[i]: num(x)).grid(row=3 + int(i / 4), column=i % 4, sticky='NEW')
tk.Button(top, text='=', command=calc).grid(row=6, column=3, sticky='NEW')

top.mainloop()
