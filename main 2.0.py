import copy
import os
from tkinter import *
from tkinter import filedialog
from tkinter.messagebox import *
from PIL import ImageGrab


PATH = os.path.dirname(os.path.realpath(__file__))          #编写端
#PATH = os.getcwd()                                         #应用端

root = Tk()
root.title('选座位 by 丁誉轩')
root.geometry('1600x1000+0+0')
root.resizable(False, False)
root.config(bg = '#1e1e1e')
root.iconbitmap(PATH + '\\Threat.contrast-black.ico')

Seatlist = ['list of Seat']
BUJU_MODE = 2

def NOTHING(*arge):
    pass

file_path = PATH + '\\table.dyxseat'

def open_file():
    global file_path

    file_path = filedialog.askopenfilename(title = '打开座位表', filetypes = [('座位表文件', '.dyxseat')], initialdir = PATH)
    file_path = file_path.strip()
    if file_path == '':
        return
    seat_file = open(file_path, 'r', encoding = 'UTF-8')
    formal_data = seat_file.readlines()
    seat_file.close()

    for i in range(len(formal_data)):
        if formal_data[i] == '#--------#\n':
            nnn = formal_data[:i]
            ccc = formal_data[i+1:]
            break

    for i in range(len(nnn)):
        nnn[i] = nnn[i].strip()

    for i in range(len(ccc)):
        ccc[i] = ccc[i].strip()

    core._replace()

    undo_button['state'] = 'normal'
    jump_button['state'] = 'normal'
    new_seat_button['state'] = 'normal'
    restart_button['state'] = 'normal'
    save_picture_button['state'] = 'normal'


    core.names = copy.deepcopy(nnn)
    core.waiting = copy.deepcopy(nnn)
    for i in range(len(ccc)):
        core.excute(ccc[i])
    core.flash()

def new_file():
    global BUJU_MODE


    new_guide = Frame(root, bg = '#3C3C3C')
    new_guide.place(x = 0, y = 0, width = 1600, height = 1000)

    Label(new_guide, text = ' →  选择一个预设布局：', bg = '#3c3c3c', fg = '#519ABA', font = ('微软雅黑', 30)).place(x = 0, y = 100, width = 600, height = 100)
    buju_details = Label(new_guide, text = '√ 预设模式2：双人同桌，共 4 大组、八行八列， 外加窗边特色座位 5 个，共 69 个座位。', bg = '#3c3c3c', fg = '#3fffff', font = ('微软雅黑', 18), anchor = 'w', justify = 'left', wraplength = 550)
    buju_details.place(x = 100, y = 800, height = 80, width = 550)

    def mode1():
        "空"
        global BUJU_MODE
        BUJU_MODE = 1
        buju_details.config(text = '√ 预设模式1：没有预设座位。')

    def mode2():
        "8x8+4"
        global BUJU_MODE
        BUJU_MODE = 2
        buju_details.config(text = '√ 预设模式2：双人同桌，共 4 大组、八行八列， 外加窗边特色座位 5 个，共 69 个座位。')

    mode1_but = Button(new_guide, text = '预设模式1', font = ('微软雅黑', 13), borderwidth = 0, fg = 'lime', bg = '#49494B', activebackground = '#252526', activeforeground = 'white', command = mode1)
    mode2_but = Button(new_guide, text = '预设模式2', font = ('微软雅黑', 13), borderwidth = 0, fg = 'lime', bg = '#49494B', activebackground = '#252526', activeforeground = 'white', command = mode2)

    mode1_but.place(x = 120, y = 250, height = 80, width = 200)
    mode2_but.place(x = 120, y = 370, height = 80, width = 200)


    Label(new_guide, text = ' →  输入名单：', bg = '#3c3c3c', fg = '#519ABA', font = ('微软雅黑', 30), anchor = 'w').place(x = 820, y = 100, width = 600, height = 100)
    Label(new_guide, text = '↑↑↑ 一行一个姓名，其中每个名字里不可含有空格 ↑↑↑', bg = '#3c3c3c', fg = 'grey', font = ('微软雅黑', 10), anchor = 'w', justify = 'left', wraplength = 550).place(x = 850, y = 610, height = 40, width = 550)

    name_getter = Text(new_guide, bg = '#4d4d4d', fg = 'white', font = ('微软雅黑', 16), borderwidth = 0)
    name_getter.place(x = 850, y = 210, height = 400, width = 500)

    def okok():
        namelist = name_getter.get(1.0, END).strip().split()
        if len(namelist) == 0:
            showerror('无效', '名单为空。请检查输入，好歹得有一个人吧大哥？')
            return

        core._replace()
        core.names = []
        core.waiting = []
        core.jumped = []
        for item in namelist:
            core.names.append(item)
            core.waiting.append(item)
        undo_button['state'] = 'normal'
        jump_button['state'] = 'normal'
        new_seat_button['state'] = 'normal'
        restart_button['state'] = 'normal'
        save_picture_button['state'] = 'normal'


        if BUJU_MODE == 2:
            core.excute('init_69')

        core.flash()
        offf()

    def offf():
        new_guide.destroy()

    ok_button = Button(new_guide, text = '确 定', font = ('微软雅黑', 15), borderwidth = 0, fg = 'lime', bg = '#49494B', activebackground = '#252526', activeforeground = 'white', command = okok)
    off_button = Button(new_guide, text = '取 消', font = ('微软雅黑', 15), borderwidth = 0, fg = 'red', bg = '#49494B', activebackground = '#252526', activeforeground = 'white', command = offf)

    ok_button.place(x = 850, y = 700, height = 60, width = 200)
    off_button.place(x = 1070, y = 700, height = 60, width = 200)


help_win_opened = 0

def helpo():

    help_text = '''选座位助手 2.0 使用帮助

    更新：2024.7.14

    选座位助手 2.0 相较于之前的 1.0 版本，新增了撤销、跳过、自定义座位、保存、导出为图片等实用且简洁易用的功能。每次操作后，程序都将自动保存当前座位表。详细信息敬请前往 B 站，观看代码编写全过程和视频使用教程！

    感谢大家的使用！如有问题欢迎反馈！

    QQ：431495254
    B 站：卢丁喆丰群
    https://space.bilibili.com/1004176582

    开发者：杭州第二中学钱江学校 丁誉轩'''

    global help_win_opened
    if help_win_opened:
        return
    help_win_opened = 1
    help_win = Tk()
    help_win.geometry('600x380')
    help_win.title('帮助')
    help_win.resizable(False, False)
    help_win.wm_attributes('-topmost', 1)

    TPT = Text(help_win, font = ('微软雅黑', 13))
    TPT.place(x = 0, y = 0, width = 600, height = 380)
    TPT.insert(1.0, help_text)
    TPT['state'] = 'disabled'

    def of(*args):
        global help_win_opened
        help_win_opened = 0

    help_win.bind('<Destroy>', of)
    help_win.mainloop



def restart():
    if askyesno('确认', '“重新开始”不是可撤销的操作。是否继续？'):
        core._replace()
        core.waiting = copy.deepcopy(core.names)
        if BUJU_MODE == 2:
            core._init_mode_69()
        core.flash()


# ----------下面是界面中的常驻控件----------

Label(root, text = '讲台', bg = '#1E1E1E', fg = 'white', font = ('仿宋', 38)).place(x = 600, y = 120, height = 120, width = 200, anchor = 'nw')
Label(root, text = '已选人员', bg = '#666666', fg = 'white', font = ('楷体', 18)).place(x = 0, y = 0, height = 40, width = 200, anchor = 'nw')
Label(root, text = '未选人员', bg = '#666666', fg = 'white', font = ('楷体', 18)).place(x = 0, y = 400, height = 40, width = 200, anchor = 'nw')
Label(root, text = '跳过人员', bg = '#666666', fg = 'white', font = ('楷体', 18)).place(x = 0, y = 800, height = 40, width = 200, anchor = 'nw')


done_list_T = Text(root, bg = '#333333', fg = 'lime', font = ('楷体', 18), borderwidth = 0)
done_list_T.place(x = 0, y = 40, height = 360, width = 200)
done_list_T['state'] = 'disabled'

waiting_list_T = Text(root, bg = '#333333', fg = '#F5E72D', font = ('楷体', 18), borderwidth = 0)
waiting_list_T.place(x = 0, y = 440, height = 360, width = 200)
waiting_list_T['state'] = 'disabled'

jumped_list_T = Text(root, bg = '#333333', fg = 'grey', font = ('楷体', 18), borderwidth = 0)
jumped_list_T.place(x = 0, y = 840, height = 360, width = 200)
jumped_list_T['state'] = 'disabled'

history_viewer = Text(root, bg = 'black', fg = 'white', font = ('consolas', 14), borderwidth = 0)
history_viewer.place(x = 1200, y = 0, width = 400, height = 600)
history_viewer['state'] = 'disabled'

operating_box = Frame(root, bg = '#252526', borderwidth = 0)
operating_box.place(x = 1200, y = 600, width = 400, height = 400)

undo_button = Button(operating_box, text = '撤 销', font = ('微软雅黑', 16), bg = '#007ACC', fg = 'white', activeforeground = '#bbbbbb', activebackground = '#04395E', borderwidth = 0, command = lambda: core.excute('undo'))
undo_button.place(x = 20, y = 20, width = 170, height = 60)
undo_button['state'] = 'disabled'

jump_button = Button(operating_box, text = '跳 过', font = ('微软雅黑', 16), bg = '#007ACC', fg = 'white', activeforeground = '#bbbbbb', activebackground = '#04395E', borderwidth = 0, command = lambda: core.jump())
jump_button.place(x = 210, y = 20, width = 170, height = 60)
jump_button['state'] = 'disabled'

insert_button = Button(jumped_list_T, text = '插队', bg = '#252526', fg = '#C19961', font = ('微软雅黑', 10), activebackground = '#252526', activeforeground = 'white', borderwidth = 0, command = lambda: core.insert())
insert_button.place(x = 200, y = 0, anchor = 'ne')

new_seat_button = Button(operating_box, text = '新建座位', font = ('微软雅黑', 16), bg = '#007ACC', fg = 'white', activeforeground = '#bbbbbb', activebackground = '#04395E', borderwidth = 0, command = lambda: core.excute('addseat_user'))
new_seat_button.place(x = 20, y = 100, width = 170, height = 60)
new_seat_button['state'] = 'disabled'

restart_button = Button(operating_box, text = '重新开始', font = ('微软雅黑', 16), bg = '#007ACC', fg = 'white', activeforeground = '#bbbbbb', activebackground = '#04395E', borderwidth = 0, command = restart)
restart_button.place(x = 210, y = 100, width = 170, height = 60)
restart_button['state'] = 'disabled'

new_file_button = Button(operating_box, text = '新建座位表', font = ('微软雅黑', 16), bg = '#007ACC', fg = 'white', activeforeground = '#bbbbbb', activebackground = '#04395E', borderwidth = 0, command = new_file)
new_file_button.place(x = 20, y = 180, width = 170, height = 60)

open_file_button = Button(operating_box, text = '打开座位表', font = ('微软雅黑', 16), bg = '#007ACC', fg = 'white', activeforeground = '#bbbbbb', activebackground = '#04395E', borderwidth = 0, command = open_file)
open_file_button.place(x = 210, y = 180, width = 170, height = 60)

save_picture_button = Button(operating_box, text = '导出座位表为图片', font = ('微软雅黑', 15), bg = '#007ACC', fg = 'white', activeforeground = '#bbbbbb', activebackground = '#04395E', borderwidth = 0, command = lambda: core._print_picture())
save_picture_button.place(x = 20, y = 260, width = 170, height = 60)
save_picture_button['state'] = 'disabled'

help_button = Button(operating_box, text = '帮 助', font = ('微软雅黑', 16), bg = '#007ACC', fg = 'white', activeforeground = '#bbbbbb', activebackground = '#04395E', borderwidth = 0, command = helpo)
help_button.place(x = 210, y = 260, width = 170, height = 60)

Label(operating_box, text = '杭州第二中学钱江学校 丁誉轩 版权所有', bg = '#252526', fg = 'white', font = ('楷体', 12)).place(x = 0, y = 340, height = 60, width = 400)


# ----------上面是界面中的常驻控件----------


tmp_history = []


class Core:

    def __init__(self):
        self.seatnum = 0
        self.names = []
        self.done = []
        self.waiting = []
        self.jumped = []
        self.history = []

        self.add_seat_info = Label(root, text = '在此区域中单击以添加一个新的座位。单击位置将成为新座位的左上角。', font = ('仿宋', 20), bg = '#1e1e1e', fg = 'white', justify = 'left')
        self.cancel_add_seat_label = Label(operating_box, text = '取 消', font = ('微软雅黑', 16), bg = '#B180B4', fg = 'white')


    def excute(self, order: str):
        order = order.strip().split()
        if order[0] == 'addseat_user':
            if len(order) == 1:
                self.addseat_by_user()
            elif len(order) == 4:
                self.addseat_by_sys(x = int(order[1]), y = int(order[2]), m = int(order[3]))

        elif order[0] == 'addseat_sys':
            self.addseat_by_sys(x = int(order[1]), y = int(order[2]), m = int(order[3]))

        elif order[0] == 'select':
            global Seatlist
            seat_id = int(order[1])

            if len(self.waiting) > 0:
                Seatlist[seat_id].chosen(name = self.waiting[0])
                self.done.append(self.waiting[0])
                self.waiting.pop(0)
                self.flash()

                self.add_history(text = f'select {seat_id}')

        elif order[0] == 'undo':
            if (BUJU_MODE == 1 and len(self.history) > 0) or (BUJU_MODE == 2 and len(self.history) > 1):
                self.undo()

        elif order[0] == 'init_69':
            self._init_mode_69()

        else:
            pass

    def addseat_by_user(self):

        def show_coords(event):
            x = root.winfo_pointerx() - root.winfo_rootx()
            y = root.winfo_pointery() - root.winfo_rooty()

            if 1220 <= x <= 1390 and 700 <= y <= 760:
                self.add_seat_info.place_forget()
                self.cancel_add_seat_label.place_forget()
                root.bind("<Button-1>", NOTHING)
                return

            elif x < 200 or x > 1200 or y > 840:
                showerror('错误', '无效位置。请重新选择！')
                return

            self.seatnum += 1
            Seatlist.append(Seat(x = x, y = y, id = self.seatnum))

            Seatlist[-1].config()

            self.add_seat_info.place_forget()
            self.cancel_add_seat_label.place_forget()

            root.bind("<Button-1>", NOTHING)
            self.add_history(text = f'addseat_user {x} {y} 1')


        self.add_seat_info.place(x = 200, y = 920, height = 80, width = 1000)
        self.cancel_add_seat_label.place(x = 20, y = 100, width = 170, height = 60)
        root.bind("<Button-1>", show_coords)

    def addseat_by_sys(self, x, y, m):
        self.seatnum += 1
        Seatlist.append(Seat(x = x, y = y, id = self.seatnum))
        Seatlist[-1].config()
        if m != 0:
            self.add_history(text = f'addseat_sys {x} {y} {m}')

    def undo(self):
        global tmp_history
        self._back()
        tmp_history.pop(-1)

        for i in range(len(tmp_history)):
            self.excute(tmp_history[i])
        self.flash()

    def jump(self):
        if len(self.waiting) > 0:
            self.jumped.append(self.waiting[0])
            self.waiting.pop(0)

            self.flash()


    def insert(self):
        if len(self.jumped) > 0:
            self.waiting = [self.jumped[0]] + self.waiting
            self.jumped.pop(0)
            self.flash()

    def _save(self):
        seat_file = open(file_path, 'w', encoding = 'UTF-8')
        seat_file.write('\n'.join(self.names))
        seat_file.write('\n#--------#\n')
        seat_file.write('\n'.join(self.history))
        seat_file.close()

    def _print_picture(self):
        img = ImageGrab.grab()
        img.save(PATH + '\\full_screen_img.jpg')

        showinfo('好了', '图片已保存在程序目录下！')

    def flash(self):
        done_list_T['state'] = 'normal'
        done_list_T.delete(1.0, END)
        done_list_T.insert(1.0, '\n'.join(core.done))
        done_list_T.see('end')
        done_list_T['state'] = 'disabled'

        waiting_list_T['state'] = 'normal'
        waiting_list_T.delete(1.0, END)
        waiting_list_T.insert(1.0, '\n'.join(core.waiting))
        waiting_list_T['state'] = 'disabled'

        jumped_list_T['state'] = 'normal'
        jumped_list_T.delete(1.0, END)
        jumped_list_T.insert(1.0, '\n'.join(core.jumped))
        jumped_list_T['state'] = 'disabled'

        self.seatnum = len(Seatlist) - 1

        self._save()

    def _back(self):
        global Seatlist, done_list_T, waiting_list_T, jumped_list_T, tmp_history

        self.seatnum = 0
        self.done.clear()
        self.waiting = copy.deepcopy(self.names)
        self.jumped.clear()

        done_list_T['state'] = 'normal'
        done_list_T.delete(1.0, END)
        done_list_T['state'] = 'disabled'

        waiting_list_T['state'] = 'normal'
        waiting_list_T.delete(1.0, END)
        waiting_list_T['state'] = 'disabled'

        jumped_list_T['state'] = 'normal'
        jumped_list_T.delete(1.0, END)
        jumped_list_T['state'] = 'disabled'

        history_viewer['state'] = 'normal'
        history_viewer.delete(1.0, END)
        history_viewer['state'] = 'disabled'
        history_viewer.see('end')

        tmp_history = self.history
        self.history = []

        while len(Seatlist) > 1:
            Seatlist[1].shut()
            del Seatlist[1]
        Seatlist = ['list of Seat']


    def _replace(self):
        global Seatlist, done_list_T, waiting_list_T, jumped_list_T

        self.seatnum = 0
        self.history.clear()
        self.done.clear()
        self.waiting = copy.deepcopy(self.names)
        self.jumped.clear()

        done_list_T['state'] = 'normal'
        done_list_T.delete(1.0, END)
        done_list_T['state'] = 'disabled'

        waiting_list_T['state'] = 'normal'
        waiting_list_T.delete(1.0, END)
        waiting_list_T['state'] = 'disabled'

        jumped_list_T['state'] = 'normal'
        jumped_list_T.delete(1.0, END)
        jumped_list_T['state'] = 'disabled'

        history_viewer['state'] = 'normal'
        history_viewer.delete(1.0, END)
        history_viewer.insert(1.0, '\n'.join(self.history))
        history_viewer['state'] = 'disabled'
        history_viewer.see('end')

        while len(Seatlist) > 1:
            Seatlist[1].shut()
            del Seatlist[1]
        Seatlist = ['list of Seat']

    def _init_mode_69(self):
        "init mode 1 : 8x8 + 5"
        for i in range(1, 9):
            for j in range(1, 9):
                X = 240 + (i - 1) * 80 + (i - 1) // 2 * 40
                Y = 280 + (j - 1) * 60
                self.excute(f'addseat_sys {X} {Y} 0')

        self.excute('addseat_sys 1040 340 0')
        self.excute('addseat_sys 1040 420 0')
        self.excute('addseat_sys 1040 500 0')
        self.excute('addseat_sys 1040 580 0')
        self.excute('addseat_sys 1040 660 0')

        self.add_history(text = 'init_69')
        '''
        for i in range(1, len(Seatlist)):
            print(Seatlist[i].id)
        '''




    def add_history(self, text):
        self.history.append(text)

        history_viewer['state'] = 'normal'
        history_viewer.delete(1.0, END)
        history_viewer.insert(1.0, '\n'.join(self.history))
        history_viewer['state'] = 'disabled'
        history_viewer.see('end')

class Seat:

    def __init__(self, x, y, id):
        self.x = x
        self.y = y
        self.id = id
        self.state = 1  # 1 means able to choose
        self.text = ''

    def config(self):
        self.wi = Button(root, text = self.text, font = ('微软雅黑', 13), bg = '#0C2C05', fg = '#00FF00', borderwidth = 1, relief = GROOVE, activebackground = '#009900', activeforeground = '#00BF00', command = self.__be_pointed)
        self.wi.place(x = self.x, y = self.y, width = 80, height = 60, anchor = 'nw')

    def __be_pointed(self):
        core.excute(f'select {self.id}')

    def chosen(self, name):
        self.wi.config(text = name)
        self.wi.config(bg = '#00006D', fg = '#8AD2F0', activebackground = '#00006D', activeforeground = '#8AD2F0', command = NOTHING)

    def shut(self):
        self.wi.place_forget()
        del self.wi


core = Core()




def tui_chu(*arge):
    root.destroy()
root.bind('<x>', tui_chu)



root.mainloop()
