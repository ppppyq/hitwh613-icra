import numpy as np
import math

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

costmap = []
costmap = np.copy(obst)

def line(tank_minex, tank_miney, tank_enemyx, tank_enemyy):
    tank_minx = min(tank_minex, tank_enemyx)
    tank_maxx = max(tank_minex, tank_enemyx)
    tank_miny = min(tank_miney, tank_enemyy)
    tank_maxy = max(tank_miney, tank_enemyy)
    tank = (tank_maxy - tank_miny) / (tank_maxx - tank_minx + 0.1)

    judge = 0

    if tank_minex == tank_enemyx:
        for i in range(0,abs(tank_miney - tank_enemyy)):
            if obst[tank_minex, tank_miny+i+1]:
                judge = 2  # 2代表有阻挡
                break
    for i in range(0, 10*abs(tank_minex - tank_enemyx)+1):
        tank_nowx1 = math.floor(tank_minx + i / 10)
        tank_nowx2 = math.ceil(tank_minx + i / 10)
        tank_nowy1 = math.floor(tank_miny + tank * i /10)
        tank_nowy2 = math.ceil(tank_miny + tank * i / 10)
        if obst[tank_nowx1, tank_nowy1] or obst[tank_nowx1, tank_nowy2] or\
                obst[tank_nowx2, tank_nowy1] or obst[tank_nowx2, tank_nowy2]:
            judge = 2  # 2代表有阻挡
            break

    return judge


def cost(rob1,rob2, enemy_number):
    tank_enemyx1 = rob1[0]
    tank_enemyy1 = rob1[1]
    tank_enemyx2 = rob2[0]
    tank_enemyy2 = rob2[1]
    for x in range(0, 44):
        for y in range(0, 80):
            costmap[x, y] = line(x, y, tank_enemyx1, tank_enemyy1)
            if enemy_number == 2:
                costmap[x, y] = line(x, y, tank_enemyx2, tank_enemyy2)
    return costmap
