import os
import sys
from random import *
from tkinter import *
from tkinter.messagebox import *

root = Tk()
root.title('选座位 by 爽想文化')
root.geometry('1600x900')
root.resizable(False, False)
root.config(bg = '#1E1E1E')


STATE = 1


def refuse():
    pass

def lock(index):
    global f

    f[index].config(bg = '#00006D', fg = '#8AD2F0', activebackground = '#00006D', activeforeground = '#8AD2F0', command = refuse)

def flash():
    global Text_of_ready, Text_of_waited, Those_who_ready, These_who_didnt, Label_of_now, NOW, Zuo_wei_biao

    Text_of_ready['state'] = 'normal'
    Text_of_waited['state'] = 'normal'
    Text_of_ready.delete(1.0, END)
    Text_of_waited.delete(1.0, END)

    Text_of_ready.insert(1.0, '\n'.join(Those_who_ready))
    Text_of_waited.insert(1.0, '\n'.join(These_who_didnt))

    Text_of_ready.see('end')
    Text_of_ready['state'] = 'disabled'
    Text_of_waited['state'] = 'disabled'

    Label_of_now.config(text = NOW)

    if len(These_who_didnt) ==0 and NOW == None:
        Label_of_now.config(text = '已完成')


def STOP():
    global f, STATE

    if STATE == 1:
        for i in range(len(f)):
            f[i].config(bg = '#00006D', fg = '#8AD2F0', activebackground = '#00006D', activeforeground = '#8AD2F0', command = refuse)
        showinfo('已结束编辑', '若要继续编辑，请按开始按钮或重启程序。')

        Start_button.config(text = '开 始', command = BEGIN)

        STATE = 2

def RESTART():
    global NOW, Shun_xu_biao, These_who_didnt, Those_who_ready, Zuo_wei_biao

    Zuo_wei_biao = ['None' for i in range(58)]
    These_who_didnt = Shun_xu_biao[:]
    Those_who_ready = []
    NOW = These_who_didnt[0]
    del These_who_didnt[0]
    flash()

    for i in range(len(f)):
        f[i].config(text = '', bg = '#0C2C05', fg = '#00FF00', borderwidth = 1, relief = GROOVE, activebackground = '#009900', activeforeground = '#00BF00', font = ('微软雅黑', 17))
        for i in range(0, len(Zuo_wei_biao)):
            if Zuo_wei_biao[i] == 'None':
                f[i].config(command = chose_mother(i))
            else:
                f[i].config(bg = '#00006D', fg = '#8AD2F0', activebackground = '#00006D', activeforeground = '#8AD2F0', command = refuse)

def BEGIN():
    global f, STATE

    if STATE == 2:
        for i in range(0, len(Zuo_wei_biao)):
            if Zuo_wei_biao[i] == 'None':
                f[i].config(bg = '#0C2C05', fg = '#00FF00', borderwidth = 1, relief = GROOVE, activebackground = '#009900', activeforeground = '#00BF00')
                f[i].config(command = chose_mother(i))
        showinfo('已启用编辑', '可继续操作。')
        Start_button.config(text = '重新开始', command = RESTART)

        STATE = 1


def SAVE(*args):
    global These_who_didnt, Those_who_ready, Zuo_wei_biao

    Zuo_wei_biao_file = open(PATH + '\\table.txt', 'w', encoding = 'UTF-8')
    Those_who_ready_file = open(PATH + '\\ready.txt', 'w', encoding = 'UTF-8')
    These_who_didnt_file = open(PATH + '\\unready.txt', 'w', encoding = 'UTF-8')

    Zuo_wei_biao_file.write('\n'.join(Zuo_wei_biao))
    Those_who_ready_file.write('\n'.join(Those_who_ready))

    if NOW != None:
        These_who_didnt_file.write(NOW + '\n' + '\n'.join(These_who_didnt))

    Zuo_wei_biao_file.close()
    Those_who_ready_file.close()
    These_who_didnt_file.close()

    root.destroy()

def GET_and_DO():
    cmd = Command_entry.get()
    if cmd == '/help':
        showinfo('说明', 'order.txt\nready.txt\nunready.txt\ntable.txt')



# Window init begin ------------------------------------------------------------------------------------------------------------------------------------------------------

line_label = [None for i in range(18)]

for i in range(0, 8):
    line_label[i] = Label(root, text = f'第{i+1}列', bg = '#1E1E1E', fg = 'white', font = ('仿宋', 16))
    line_label[i].place(x = 320 + (i//2) * 80 + i * 120, y = 120, width = 120, height = 80)

for i in range(8, 15):
    line_label[i] = Label(root, text = f'第{i-7}排', bg = '#1E1E1E', fg = 'white', font = ('仿宋', 16))
    line_label[i].place(x = 240, y = 200 + (i-8) * 80, width = 80, height = 80)

line_label[15] = Label(root, text = '讲台', bg = '#1E1E1E', fg = 'white', font = ('仿宋', 38))
line_label[15].place(x = 760, y = 20, width = 320, height = 100)

f = [Button() for i in range(80)]
for i in range(0, 8):
    for j in range(1, 8):
        X = 320 + (i//2) * 80 + i * 120
        Y = 200 + (j-1) * 80

        f[i*7+j] = Button(root, bg = '#0C2C05', fg = '#00FF00', borderwidth = 1, relief = GROOVE, activebackground = '#009900', activeforeground = '#00BF00', font = ('微软雅黑', 17))
        f[i*7+j].place(x = X, y = Y, width = 120, height = 80)


Text_of_ready = Text(root, borderwidth = 0, bg = 'black', fg = 'lime', font = ('楷体', 25), selectbackground = 'black')
Text_of_ready.place(x = 0, y = 0, width = 200, height = 420)

Label_of_now = Label(root, bg = 'grey', fg = 'yellow', font = ('楷体', 28), justify = 'center', text = '丁誉轩')
Label_of_now.place(x = 0, y = 420, width = 200, height = 60)

Text_of_waited = Text(root, borderwidth = 0, bg = 'black', fg = 'red', font = ('楷体', 25), selectbackground = 'black')
Text_of_waited.place(x = 0, y = 480, width = 200, height = 420)


Start_button = Button(root, text = '重新开始', fg = 'white', bg = '#252526', relief = FLAT, borderwidth = 0, font = ('微软雅黑', 16), activebackground = '#3C3C3C', activeforeground = 'white', command = RESTART)
Start_button.place(x = 940, y = 800, width = 180, height = 60)

Stop_button = Button(root, text = '结 束', fg = 'white', bg = '#252526', relief = FLAT, borderwidth = 0, font = ('微软雅黑', 16), activebackground = '#3C3C3C', activeforeground = 'white', command = STOP)
Stop_button.place(x = 1140, y = 800, width = 180, height = 60)

Cout_button = Button(root, text = '保存并退出', fg = 'white', bg = '#252526', relief = FLAT, borderwidth = 0, font = ('微软雅黑', 16), activebackground = '#3C3C3C', activeforeground = 'white', command = SAVE)
Cout_button.place(x = 1340, y = 800, width = 180, height = 60)

Command_entry = Entry(root, bg = 'black', fg = 'white', font = ('courier new', 14), borderwidth = 0)
Command_entry.place(x = 240, y = 800, width = 550, height = 40)

Command_button = Button(root, text = '执行', command = GET_and_DO, fg = 'white', bg = '#252526', relief = FLAT, borderwidth = 0, font = ('微软雅黑', 14), activebackground = '#3C3C3C', activeforeground = 'white')
Command_button.place(x = 790, y = 800, height = 40, width = 120)

Label_of_copyright = Label(root, text = 'Produced by Shuangxiang Culture Co., Ltd             爽想文化有限公司 出品', fg = 'white', bg = '#1E1E1E', relief = FLAT, borderwidth = 0, font = ('微软雅黑', 14))
Label_of_copyright.place(x = 240, y = 840, height = 40, width = 670)

# Window init end ------------------------------------------------------------------------------------------------------------------------------------------------------

# Data init begin ------------------------------------------------------------------------------------------------------------------------------------------------------

# Data input begin --------------------------------------------------

PATH = os.path.dirname(os.path.realpath(__file__))          #编写端
#PATH = os.getcwd()                                         #应用端

Zuo_wei_biao_file = open(PATH + '\\table.txt', 'r', encoding = 'UTF-8')
Shun_xu_biao_file = open(PATH + '\\order.txt', 'r', encoding = 'UTF-8')
Those_who_ready_file = open(PATH + '\\ready.txt', 'r', encoding = 'UTF-8')
These_who_didnt_file = open(PATH + '\\unready.txt', 'r', encoding = 'UTF-8')

# Main data is under ----------

Zuo_wei_biao = Zuo_wei_biao_file.readlines()
Shun_xu_biao = Shun_xu_biao_file.readlines()
Those_who_ready = Those_who_ready_file.readlines()
These_who_didnt = These_who_didnt_file.readlines()

if len(Zuo_wei_biao) != 0:
    for i in range(len(Zuo_wei_biao)):
        Zuo_wei_biao[i] = Zuo_wei_biao[i].split()[0]
while len(Zuo_wei_biao) <= 60:
    Zuo_wei_biao.append('None')

if len(Shun_xu_biao) != 0:
    for i in range(len(Shun_xu_biao)):
        Shun_xu_biao[i] = Shun_xu_biao[i].split()[0]

if len(Those_who_ready) != 0:
    for i in range(len(Those_who_ready)):
        Those_who_ready[i] = Those_who_ready[i].split()[0]

#print(These_who_didnt)
if len(These_who_didnt) != 0:
    for i in range(len(These_who_didnt)):
        These_who_didnt[i] = These_who_didnt[i].split()[0]

    NOW = These_who_didnt[0]
    del These_who_didnt[0]
#elif len(These_who_didnt) == 0 and len(Those_who_ready) == 0:
#    These_who_didnt = Shun_xu_biao
else:
    NOW = None
    Label_of_now.config(text = '已完成')

# Main data is above ----------

Zuo_wei_biao_file.close()
Shun_xu_biao_file.close()
Those_who_ready_file.close()
These_who_didnt_file.close()

# Data input end --------------------------------------------------

# Data config begin --------------------------------------------------

Text_of_ready.insert(1.0, '\n'.join(Those_who_ready)); Text_of_ready.see('end')
Label_of_now.config(text = NOW)
Text_of_waited.insert(1.0, '\n'.join(These_who_didnt))

for i in range(0, len(Zuo_wei_biao)):
    if Zuo_wei_biao[i] == 'None':
        continue
    else:
        f[i].config(text = Zuo_wei_biao[i])

Text_of_ready['state'] = 'disabled'
Text_of_waited['state'] = 'disabled'


# Data config end --------------------------------------------------

# Data init end ------------------------------------------------------------------------------------------------------------------------------------------------------

# Command init begin ------------------------------------------------------------------------------------------------------------------------------------------------------

def chose_mother(index):

    def chose_child():
        global f, NOW, Those_who_ready, These_who_didnt, Zuo_wei_biao

        if NOW != None:
            Those_who_ready.append(NOW)
            Zuo_wei_biao[index] = NOW
            f[index].config(text = NOW)

            #print(Zuo_wei_biao, '\n')

            if len(These_who_didnt) != 0:
                NOW = These_who_didnt[0]
                del These_who_didnt[0]
            else:
                NOW = None

            lock(index)
            flash()

        elif NOW == None:
            Label_of_now.config(text = '已完成')

    return chose_child

for i in range(0, len(Zuo_wei_biao)):
    if Zuo_wei_biao[i] == 'None':
        f[i].config(command = chose_mother(i))
    else:
        f[i].config(bg = '#00006D', fg = '#8AD2F0', activebackground = '#00006D', activeforeground = '#8AD2F0', command = refuse)


# Command init end ------------------------------------------------------------------------------------------------------------------------------------------------------

root.protocol('WM_DELETE_WINDOW', SAVE)
root.mainloop()
