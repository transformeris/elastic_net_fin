import tkinter
# 创建主窗口
win = tkinter.Tk()
# 设置标题
win.title("小王最帅")
#设置大写和位置
win.mainloop()
data = {
    '北京': {
        '昌平':
            {
                '沙河': ['沙河机场', '链家'],
                '天通苑': ['北方明珠', '天通尾货']
            },
        '朝阳':
            {
                '花家地': ['朝阳公园', '望京soho'],
                '北小河': ['北小河公园', '北京中学']
            }
    },
    '上海': {
        '虹桥':
            {
                '虹桥机场': ['超市', '特产店', '水吧'],
                '东方明珠': ['电影院', '游泳馆', '餐馆']
            },
        '浦东':
            {
                '景秀路': ['世纪公园', '立交桥'],
                '中环路': ['鲁迅公园', '同济大学']
            }
    },
    '河北': {
        '石家庄':
            {
                '行唐': ['东正', '阳关'],
                '赵县': ['赵州桥', '高村乡']
            },
        '唐山':
            {
                '滦南县': ['司各庄镇', '安各庄镇'],
                '玉田县': ['玉田镇', '亮甲店镇']
            }
    }
}
while True:
    for i in data:  # 打印第一级列表
        print(i)
    choice = input("请选择省或直辖市(退出请按q):")
    if choice in data:  # 如果在第一级列表里则进入下一级列表
        while True:
            for i2 in data[choice]:  # 打印第二级列表
                print(i2)
            choice2 = input("请选择(退出请按q返回省或直辖市列表请按b):")
            if choice2 in data[choice]:  # 如果在第二级列表里则进入下一级
                while True:
                    for i3 in data[choice][choice2]:  # 打印第三级列表
                        print(i3)
                    choice3 = input("请选择(退出请按q返回上一级列表请按b):")
                    if choice3 in data[choice][choice2]:
                        for i4 in data[choice][choice2][choice3]:
                            print(i4)
                        choice4 = input("已经到达最后一级(退出请按q返回上一级列表请按b):")
                        if choice4 == 'b':
                            continue
                        elif choice4 == 'q':
                            exit()
                    elif choice3 == 'b':  # 从第三级返回第二级
                        break
                    elif choice3 == 'q':
                        exit()
            elif choice2 == 'b':  # 从第二级返回第一级
                break
            elif choice2 == 'q':
                exit()
    elif choice == 'q':
        exit()
