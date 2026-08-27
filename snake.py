import threading
import time
import tkinter
import random
import tkinter.ttk
import tkinter.messagebox
import sys
import ctypes
import inspect
import math
import tkinter.colorchooser

size = (50,30) #长*宽
unit = 10 #单位边长
head = (0,0) #当前蛇头的位置
direction = 1
newdirection = 1
directions = [(0,-1),(0,1),(1,0),(-1,0)] #方向，分别为上、下、左、右
interval = 0.1 #蛇每移动一步等待时间
positions = [] #蛇身所在位置
pause = False #标记游戏是否暂停
score = 0 #分数
dead = False #游戏是否结束
food = (0,0) #食物所在位置
body = []
bodyobj = tkinter.Label
args = {"bg":"cyan","relief":"solid","borderwidth":1}


root = tkinter.Tk()
frame = tkinter.Canvas(root,relief="sunken",height=size[1] * unit,width=size[0] * unit)
frame.pack()
dot = tkinter.Label(frame,text="●",fg="red") #食物
showscore = tkinter.Label(root,text=0) #用于显示分数
showscore.pack()
focuspoint = tkinter.Frame(root,takefocus=True) #用于接收玩家的键盘输入
focuspoint.pack()
focuspoint.focus_set() #获取焦点


def settings():
    global pause
    pause = True
    top = tkinter.Toplevel()
    top.grab_set()
    def ok():
        global pause
        global size
        global unit
        global interval
        if unitinput.get().isdigit():
            if 5 <= int(unitinput.get()) <= 20:
                unit = int(unitinput.get())
        if widthinput.get().isdigit():
            if 10 <= int(widthinput.get()) <= 100:
                size = (int(widthinput.get()),size[1])
        if heightinput.get().isdigit():
            if 10 <= int(heightinput.get()) <= 100:
                size = (size[0],int(heightinput.get()))
                
        frame.delete(tkinter.ALL)
        drawnet()
        frame.configure(height=size[1] * unit,width=size[0] * unit)
        place(dot,food)
        for i in range(len(body)):
            place(body[i],positions[i])
        interval = 2 / speedvar.get()
        pause = False
        top.destroy()
    top.protocol("WM_DELETE_WINDOW",ok)
        

    speedvar = tkinter.IntVar()
    frame1 = tkinter.ttk.LabelFrame(top,text="速度")
    frame1.pack(expand=True,fill=tkinter.X)
    speed = tkinter.ttk.LabeledScale(frame1,variable=speedvar,from_=1,to=100)
    speedvar.set(2 / interval)
    speed.pack(expand=True,fill=tkinter.X)

    frame2 = tkinter.ttk.LabelFrame(top,text="界面大小")
    frame2.pack(expand=True,fill=tkinter.BOTH)
    setunit = tkinter.Frame(frame2)
    setunit.pack()
    askunit = tkinter.ttk.Label(setunit,text="单位大小：")
    askunit.grid(row=0,column=0)
    unitinput = tkinter.ttk.Spinbox(setunit,from_=5,to=20)
    unitinput.insert(0,unit)
    unitinput.grid(row=0,column=1)

    setwidth = tkinter.Frame(frame2)
    setwidth.pack()
    askwidth = tkinter.Label(setwidth,text="长：")
    askwidth.grid(row=0,column=0)
    widthinput = tkinter.ttk.Spinbox(setwidth,from_=10,to=100)
    widthinput.insert(0,size[0])
    widthinput.grid(row=0,column=1)
    
    setheight = tkinter.Frame(frame2)
    setheight.pack()
    askheight = tkinter.Label(setheight,text="宽：")
    askheight.grid(row=0,column=0)
    heightinput = tkinter.ttk.Spinbox(setheight,from_=10,to=100)
    heightinput.insert(0,size[1])
    heightinput.grid(row=0,column=1)

    def choose(sth):
        global args
        colordict = {"红色":"red","蓝色":"blue","绿色":"green","黄色":"yellow","紫色":"purple","靛蓝":"cyan","黑色":"black","白色":"white"}
        if sth == "更多":
            othercolor = tkinter.colorchooser.askcolor()
            colorvar.set(value=othercolor[1])
            if othercolor[1] == None:
                colorvar.set(value="不改变颜色")
            else:
                args["bg"] = othercolor[1]
        else:
            args["bg"] = colordict[sth]
        for i in body:
            i.configure(bg=args["bg"])
            
            
    frame3 = tkinter.ttk.LabelFrame(top,text="颜色")
    frame3.pack(expand=True,fill=tkinter.X)
    colors = ["红色","蓝色","绿色","黄色","紫色","靛蓝","黑色","白色","更多"]
    colorvar = tkinter.StringVar()
    colorvar.set(value="不改变颜色")
    color = tkinter.ttk.OptionMenu(frame3,colorvar,command=choose,*colors)
    color.pack(expand=True,fill=tkinter.X)
    
    ok = tkinter.ttk.Button(top,text="OK",command=ok)
    ok.pack(side=tkinter.RIGHT)


    
    root.wait_window()


def drawnet():
    for i in range(size[0]):
        frame.create_line(i * unit,0,i * unit,unit * size[1],fill="#CCCCCC")
    for i in range(size[1]):
        frame.create_line(0,i * unit,unit * size[0],i * unit,fill="#CCCCCC")
        


def newgame():
    global pause
    global positions
    global direction
    global score
    global body
    global newdirection
    global thread
    global dead

    if thread.is_alive():
        killthread(thread.ident,SystemExit)
    
    for i in body:
        i.destroy()
    body.clear()
    food = (0,0)
    positions.clear()
    direction = 1
    newdirection = 1
    score = 0
    pause = False
    dead = False
    showscore.configure(text="0")
    init() #初始化
    thread = threading.Thread(target=loop) #对于游戏主循环，则需另外开一个线程，否则会卡死主界面
    thread.start() #开始游戏！

def about():
    global pause
    top = tkinter.Toplevel()
    title = tkinter.Label(top,text="贪吃蛇",font=(None,20))
    title.pack()
    content = tkinter.Label(top,text="By Jzwalliser")
    content.pack()
    pause = True
    top.grab_set()
    def close():
        global pause
        pause = False
        top.destroy()
    top.protocol("WM_DELETE_WINDOW",close)
    root.wait_window()
    

def exitgame():
    if thread.is_alive():
        killthread(thread.ident,SystemExit)
    root.destroy()

def init():
    global head
    global body
    global positions
    
    head = (2,0) #蛇头初始位置在(2,0)
    
    for i in range(3): #刚开始蛇有3节身体
        node = bodyobj(frame,args)
        place(node,(i,0))
        positions.append((i,0)) #记录位置
        body.append(node) #将身体的每一节都放在一个列表中,备用
        mkfood()

def pausegame():
    global pause
    pause = not pause

def place(obj,pos): #方便绘制蛇
    obj.place(x=pos[0] * unit,y=pos[1] * unit,height=unit,width=unit)


def killthread(tid,exctype): #杀线程的代码来源于：https://tomerfiliba.com/recipes/Thread2
    try:
        tid = ctypes.c_long(tid)
        if not inspect.isclass(exctype):
            exctype = type(exctype)
        res = ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, ctypes.py_object(exctype))
        if res == 0:
            raise ValueError("Invalid Thread ID")
        elif res != 1:
            ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, None)
            raise SystemError("PyThreadState_SetAsyncExc failed")
    except Exception as err:
        print(err)

def loop():
    global head
    global body
    global dead
    global positions
    global score
    global direction
    while True:
        if not dead:
            positions.pop(0) #将蛇尾的坐标删除
            node = body[0] #将蛇尾的按钮出列
            body.pop(0)
            head = (head[0] + directions[direction][0],head[1] + directions[direction][1]) #计算当前蛇头的位置

            if head[0] < 0: #如果蛇左越界
                head = (head[0] + size[0],head[1]) #那么蛇从右边出来
            if head[1] < 0: #如果蛇上越界
                head = (head[0],head[1] + size[1]) #处理由越界和上越界
            head = (head[0] % size[0],head[1] % size[1])
            
            if head in positions: #如果蛇撞到了自己的身体
                dead = True #那么游戏结束
            positions.append(head) #将新的位置加入列表中
            place(node,head) #刚才的蛇尾放到蛇头
            body.append(node) #处理完蛇头那个按钮后，将其放到队尾

            if head == food: #如果吃到食物
                mkfood() #刷新食物位置
                score += math.ceil(0.1 / interval) ** 2 #加几分
                positions.insert(0,(0,0)) #当前蛇头的位置
                body.insert(0,bodyobj(frame,args)) #将坐标和一节身体都放在队头，这样在下一次循环中，就会被马上处理
                showscore.configure(text=score) #显示最新分数
            time.sleep(interval) #等待一会儿
            direction = newdirection
            while pause: #如果游戏被暂停,则阻塞线程
                time.sleep(0.2) #每隔2秒检查一次游戏状态
        else:
            death() #善后

def mkfood(): #用于确定食物的坐标
    global food
    while True: #不停地循环，直到找到可以放置食物的地方
        x = random.randint(0,size[0] - 1) #先随机食物的坐标
        y = random.randint(0,size[1] - 1)
        if (x,y) not in body: #方向，分别为上、下、左、右
            food = (x,y) #那这就是个合法的坐标
            dot.place(x=x * unit + 1,y=y * unit + 1,width = unit - 2,height = unit - 2) #可以把食物放在这个地方
            break #并结束循环

def death(): #游戏结束
    top = tkinter.Toplevel()
    def restart():
        newgame()
        top.destroy()
    label = tkinter.ttk.Label(top,text="游戏结束！\n得分：" + str(score) + "\n是否重新开始游戏？")
    label.pack()
    yesno = tkinter.ttk.Frame(top)
    yes = tkinter.ttk.Button(yesno,text="重新开始",command=restart)
    yes.grid(row=0,column=0)
    no = tkinter.ttk.Button(yesno,text="取消",command=exitgame)
    no.grid(row=0,column=1)
    yesno.pack()
    top.grab_set()
    root.wait_window()

def changedirection(event): #蛇每移动一步等待时间
    global newdirection
    disallow = [1,0,3,2] #只可以往当前方向的垂直方向走，如现在蛇向右走，那么改变方向时，蛇只能向上或向下而不能往回走
    dictionary = {"Up":0,"Down":1,"Left":3,"Right":2,"W":0,"A":3,"S":2,"D":1,"w":0,"a":3,"s":2,"d":1} #键盘映射方向
    print(event.keysym)
    if event.keysym in dictionary.keys():
        if disallow[dictionary[event.keysym]] != direction: #如果没有往回
            newdirection = dictionary[event.keysym] #那么就改变方向
            
focuspoint.bind("<Key>",changedirection) #绑定事件

root.protocol("WM_DELETE_WINDOW",exitgame)


drawnet()
init() #初始化
thread = threading.Thread(target=loop) #对于游戏主循环，则需另外开一个线程，否则会卡死主界面
thread.start() #开始游戏！



menu = tkinter.Menu(root)
game = tkinter.Menu(menu,tearoff=False)
game.add_command(label="重新开始",command=newgame)
game.add_command(label="暂停/继续",command=pausegame)
game.add_command(label="设置",command=settings)
game.add_command(label="退出游戏",command=exitgame)
menu.add_cascade(label="游戏",menu=game)
menu.add_cascade(label="关于",command=about)
root.config(menu=menu)



root.mainloop()
"""
Todo:
1. 把食物改成圆的
2. 把place改为pack
3. 增加超级食物
4. 增加墙，公寓等
"""

