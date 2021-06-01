import math
import threading
from socket import *
import mymath
import path_planning as path
import time,mode
import blue

global weizhix, weizhiy
global decision_path,angle,connect_flag
global path_change_flag
global data


decision_path = []

class RP():
    def __init__(self):
        self.state =[0,-1,-1,-1,-1,-1] #奖罚区标记 0己方回血 1己方补弹 2敌方回血 3敌方补弹 4禁止射击 5禁止移动
        self.coordinate = [[18,7],[29,20],[41,41],[5,41],[18,63],[29,77]]    #惩罚区中心点位置
        self.RPmatch = [0,0,0,0]


class robot():
    def __init__(self,enemy,coord=[[0,0]]):
        self.coordinate=coord
        self.life = 1300        #初始血量
        self.round = 50         #初始弹药量
        self.if_enemy = enemy
        self.RPstate=[0,0,1,0]#第一位禁止射击 第二位禁止移动 第三位寻找加血区 第四位寻找加弹区 1生效





    def reflash_coordinate(self):    #我们的初始位置

        if self.if_enemy == 1:
            address1 = blue.return_adress()     #我要写的cam,列表里套列表
            # adress与mycoordinate格式转换
            if len(address1[0])!=2 or len(address1[1])!=2:
                address1 = [[0, 0], [0, 0]]
            for i in range(5):
                self.coordinate[i + 1] = self.coordinate[i]
                self.coordinate[0] = [int(math.ceil((address1[0][0]+address1[1][0])/2*10)),int(math.ceil((address1[0][1]+address1[1][1]+1.275)/2*10))]
        else:
            self.coordinate = [0,0]##mycoordinate     #我方的位置tcp，裁判系统，敌方的视觉识别
        return






def robot_angle(my_coordinate,enemy_coordinate):


    #不知道ros那里0度，我要改



    if (enemy_coordinate[0][0]-my_coordinate[0][0]==0)and(enemy_coordinate[0][1]-my_coordinate[1]>0):
        return math.pi/2
    elif (enemy_coordinate[0][0]-my_coordinate[0]==0)and(enemy_coordinate[0][1]-my_coordinate[1]<0):
        return -1*math.pi/2
    elif (enemy_coordinate[0][0]-my_coordinate[0]>0):
        return math.atan((enemy_coordinate[0][1]-my_coordinate[1])/(enemy_coordinate[0][0]-my_coordinate[0]))
    elif (enemy_coordinate[0][0]-my_coordinate[0]<0):
        return math.atan((enemy_coordinate[0][1] - my_coordinate[1]) / (enemy_coordinate[0][0] - my_coordinate[0]))+math.pi
    return 0




def rec(tcpCliSock,BUFSIZ):
    global connect_flag
    global data
    while(connect_flag):
        data = tcpCliSock.recv(BUFSIZ).decode("utf-8")
        print(data)

        if not data:
            connect_flag = 0
            print('connect error')
            break




def send(tcpCliSock):
    global connect_flag
    global decision_path
    global path_change_flag
    global data
    delay = 0.5

    while(connect_flag):
        time.sleep(delay)
        num = len(decision_path)
        path_change_flag = 0
        for i in range(num):
            if(path_change_flag == 1):
                break

            x = decision_path[i][0]        #
            y = decision_path[i][1]        #

            #校准还没做
            tcpCliSock.send(('%d%.2f%.2f' %(data[0],x/10,y/10)).encode("utf-8"))    #%(x,y,robot_angle([[x],[y]],enemy_coordinate))
        #tcpCliSock.send(('0%.2f%.2f%.2f' % (1.00, 2.00, math.pi/2)).encode("utf-8"))
    tcpCliSock.close()


#def shaogang():
#    global weizhix, weizhiy



def ComRecSend():
    global decision_path,connect_flag,data
    #HOST ='192.168.43.122'
    HOST = ''
    PORT = 2451
    BUFSIZ = 1024
    ADDR = (HOST,PORT)

    tcpSerSock = socket(AF_INET, SOCK_STREAM)
    tcpSerSock.bind(ADDR)  # 绑定IP地址和端口号
    tcpSerSock.listen(5)  # 监听，使得主动变为被动

    '''while True:
        print('正在等待连接....')
        tcpCliSock, addr = tcpSerSock.accept()  # 当来新的连接时，会产生一个的新的套接字为客户端服务
        print(tcpCliSock)
        print(addr)
        print('连接成功')
        connect_flag =1
        while True:
            data = tcpCliSock.recv(BUFSIZ).decode("utf-8")
            if not data:
                break
            print(data)
            tcpCliSock.send(('%s'%(data)).encode("utf-8"))
        tcpCliSock.close()
    tcpSerSock.close()
    '''

    while True:
        print('正在等待连接....')
        tcpCliSock, addr = tcpSerSock.accept()  # 当来新的连接时，会产生一个的新的套接字为客户端服务
        print(tcpCliSock)
        print(addr)
        print('连接成功')
        connect_flag = 1
        myrec = threading.Thread(target=rec,args=(tcpCliSock,BUFSIZ,))
        myrec.start()
        mysend = threading.Thread(target=send, args=(tcpCliSock,))
        mysend.start()
    tcpSerSock.close()




def next_enemy_coordinate(robot):
    gm = mymath.GM()
    ls1 = robot.coordinate[:,0]
    gm.fit(ls1)
    x=gm.predict(m=1)[5]
    ls2 = robot.coordinate[:,1]
    gm.fit(ls2)
    y=gm.predict(m=1)[5]
    return [x,y]



def decision_tree(enemy_num,RP,my_robot,enemy_robot_1,enemy_robot_2,gamemap):
    global decision_path
    global path_change_flag

    life_low = 1500 #补血阈值
    round_low = 60  #补弹阈值
    life_away = 2200 #逃跑阈值
    relife_flag = -1
    reround_flag = -1
    for i in range(6):
        if(RP.state == 0):
            relife_flag = i
        if(RP.state == 1):
            reround_flag = i

    if((my_robot.life<life_low)&(relife_flag != -1)):
        decision_path = gamemap.planning(my_robot.coordinate[0],RP.coordinate[i])
        path_change_flag = 1
        print(decision_path)
    elif((my_robot.round<round_low)&(reround_flag != -1)):
        decision_path = gamemap.planning(my_robot.coordinate[0],RP.coordinate[i])
        path_change_flag = 1
        print(decision_path)
    elif(my_robot.life<life_away):
        decision_path = mode.escape(my_robot,enemy_robot_1,enemy_robot_2,enemy_num,gamemap)
        path_change_flag = 1
        print(decision_path)
    else:
        decision_path = mode.escape(my_robot,enemy_robot_1,enemy_robot_2,enemy_num,gamemap)
        path_change_flag = 1
        print(decision_path)


    return





if __name__ == '__main__':

    #map init
    RACE_RP=RP()

    gamemap = path.map()
    gamemap.reflashmap()

    #tcp_init
    tcp = threading.Thread(target=ComRecSend)  # 创建串口接收线程
    tcp.start()



    # cam init
    #cam = threading.Thread(target=blue.begin)
    #cam.start()

    #robot init
    enemy_num = 1
    my_bot = robot(enemy=0,coord=[[43,2]])#蓝方起始点为[3,2] [43,2]红方起始点为[3,76][43,76]


    enemy_bot_1 = robot(enemy=1, coord=[[3, 76], [3, 76], [3, 76], [3, 76], [3, 76], [3, 76]])
    enemy_bot_2 = robot(enemy=1, coord=[[43,76],[43,76],[43,76],[43,76],[43,76],[43,76]])



    while(1):
        if(enemy_num == 1):
            enemy_bot_1.reflash_coordinate()
        if (enemy_num == 2):
            enemy_bot_1.reflash_coordinate()
            enemy_bot_2.reflash_coordinate()
        my_bot.reflash_coordinate()
        gamemap.reflashmap()
        decision_tree(enemy_num=enemy_num,RP=RACE_RP,my_robot=my_bot,enemy_robot_1=enemy_bot_1,enemy_robot_2=enemy_bot_2,gamemap=gamemap)



