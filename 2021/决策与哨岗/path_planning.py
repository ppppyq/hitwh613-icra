#bfs求解算法
import numpy as np
import math
class node:
    def __init__(self, x=0, y=0, t=0):
        self.x = x
        self.y = y
        self.t = t  # t表示走到这个格子用的步数


class father:
    def __init__(self, x=0, y=0, cz=[]):
        self.x = x  # 当前格子的父节点坐标
        self.y = y
        self.cz = cz  # 由什么操作到达的这个格子,D,R,L,U


def bfs(s_point,e_point,mmap,mode):
    lj = []
    for i in range(0, 46):
        lj += [[]]
        for j in range(0, 85):
            lj[i] += [father()]  # 第i个元素是空列表，添加完以后每个第i元素都有十个father类的对象

    x1 = s_point[0]
    y1 = s_point[1]
    x2 = e_point[0]
    y2 = e_point[1]

    # vis = [[False]*10]*10
    vis = []
    for i in range(0, 46):
        vis += [[]]
        for j in range(0, 85):  # 10这个数大了,只不过没关系,vis与mmap是分开的
            vis[i] += [0]  # 先初始化为全部没访问过
    xx = [1,0,0,-1]  # 右、下、左、上
    yy = [0,1,-1,0]

    q = []
    s = node()
    f = node()
    n = 44
    m = 80

    s.x = x1
    s.y = y1
    s.t = 0   ##规定起点和终点的
    f.x = x2  ##f是终点，s是起点
    f.y = y2
    q.append(s)  # q这个空列表存储的是node类型的对象
    lj[s.x][s.y].x = 1000
    lj[s.x][s.y].y = 1000
    lj[s.x][s.y].cz = 0
    vis[x1][y1] = 0  # 起始点标为已经访问过
    # print("vis={}".format(vis))
    while q:  # 只要q中有值，就继续循环
        now = q[0]
        q.pop(0)  #删去最q列表开始的元素
        for i in range(0, 4):  # 为何是4,上下左右xx,yy
            new = node()
            new.x = now.x + xx[i]
            if(new.x == -1):
                continue
            new.y = now.y + yy[i]
            if (new.y == -1):
                continue
            new.t = now.t + 1
            # print("i={} new.x={} new.y={} now.x={} now.y={}".format(i, new.x, new.y, now.x, now.y))
            # print("new.x ={} new.y={} n={} m={} vis[new.x][new.y]={} mmap[new.x][new.y]={}".format(new.x, new.y, n, m, vis[new.x][new.y], mmap[new.x][new.y]))
            if ((new.x < 0 or new.y < 0 or new.x >= n or new.y >= m or vis[new.x][new.y] != 0 or mmap[new.x][new.y]) == 1):  # 下标越界或者访问过(vis)或者是障碍物
                continue
            q.append(new)# 新的点被加进q去
            lj[new.x][new.y].x = now.x  # 新点取代旧点成为new,此点是坐标不是+-1
            lj[new.x][new.y].y = now.y
            if i == 0:
                lj[new.x][new.y].cz = 'D'
            elif i == 1:
                lj[new.x][new.y].cz = 'R'
            elif i == 2:
                lj[new.x][new.y].cz = 'L'
            elif i == 3:
                lj[new.x][new.y].cz = 'U'
            vis[new.x][new.y] = new.t  # 走过的路变为1

            if(mode == 1):
                if(mmap[new.x][new.y] == 0):
                    return new.t, lj,[new.x,new.y]


            # print("value={} ({},{}) {}\n".format(mmap[new.x][new.y], new.x, new.y, lj[new.x][new.y].cz))
            # print("=============================================================")
            if(mode == 0):
                if new.x == f.x and new.y == f.y:
                    return new.t,lj,[new.x,new.y] # 到达终点
            if(mode == 2 ):
                if(mmap[new.x][new.y] == 2):
                    return new.t, lj,[new.x,new.y]
    return False



class map:
    def __init__(self):
        self.mmap = np.zeros([44, 80])
        self.cost_map = np.zeros([44, 80])
        self.RP=[0,0,0,0,0,0]
        self.way_lj = []  # 路径记载
        self.dir_lj = []  # 方向记载
        self.lj = []
    def reflashmap(self):
        obst = np.zeros([44, 80])
        obst[10:12, 0:10] = 1
        obst[21:24, 15:23] = 1
        obst[34:44, 15:17] = 1
        obst[9:12, 35:46] = 1
        obst[33:36, 35:46] = 1
        obst[21:24, 57:66] = 1
        obst[0:10, 63:66] = 1
        obst[32:35, 70:80] = 1
        obst[20:24, 38:42] = 1
        if self.RP[0] == 1:
            obst[15:20, 3:8] = 1
        if self.RP[1] == 1:
            obst[26:31, 17:22] = 1
        if self.RP[2] == 1:
            obst[38:43, 38:44] = 1
        if self.RP[3] == 1:
            obst[3:7, 38:44] = 1
        if self.RP[4] == 1:
            obst[15:20, 60:65] = 1
        if self.RP[5] == 1:
            obst[26:31, 74:79] = 1

        self.mmap = obst

        return


    def dfs(self,x1,y1,x,y):
        if x == x1 and y == y1:
            return
        else:
            self.dfs(x1,y1,self.lj[x][y].x,self.lj[x][y].y)
        # print(lj[x][y].cz)
        self.way_lj.append((self.lj[x][y].x,self.lj[x][y].y))
        self.dir_lj.append(self.lj[x][y].cz)


    def planning(self,s_point,e_point):
        if(s_point == e_point):
            return s_point
        self.way_lj = []  # 路径记载
        self.dir_lj = []  # 方向记载
        mypath = []
        for i in range(0, 46):
            self.lj += [[]]
            for j in range(0, 85):
                self.lj[i] += [father()]  # 第i个元素是空列表，添加完以后每个第i元素都有十个father类的对象
        ans,self.lj,point= bfs(s_point,e_point,self.mmap,0)

        x1 = s_point[0]
        y1 = s_point[1]
        x2 = e_point[0]
        y2 = e_point[1]
        if ans == False:
            print("error")
        else:

            #print("起点{}，终点{}，需要行走{}步".format((x1, y1), (x2, y2), ans))
            self.dfs(x1=x1,y1=y1,x=x2,y=y2)
            self.way_lj.append((x2, y2))
            mypath.append(self.way_lj[0])


            for i in range(ans):
                if(ans<10):
                    mypath.append(self.way_lj[i])
                if(10<ans<=40):
                    if ((i + 1) % 3 == 0):
                        mypath.append(self.way_lj[i])
                if(ans > 40):
                    if((i+1)%5==0):
                        mypath.append(self.way_lj[i])
            mypath.append(self.way_lj[ans])



            #print("行走经过{}".format(way_lj))
            #print("地图行走方式{}".format(dir_lj))
        return  mypath





