import  cost
import path_planning as path
import math

def pursuit(my_robot,enemy_robot_1,enemy_robot_2,enemy_num,map):
    costmap = cost.cost(enemy_robot_1.coordinate[0],enemy_robot_2.coordinate[0],enemy_num)
    min_length = 100
    e_point = my_robot.coordinate
    for i in range(44):
        for j in range(80):
            length = math.sqrt((my_robot.coordinate[0][0]-i)**2+(my_robot.coordinate[0][1]-j)**2)
            if((costmap[i,j] == 0) & (length<min_length)):
                min_length = length
                e_point = [i,j]
    print(costmap[e_point[0],e_point[1]])
    return map.planning(my_robot.coordinate[0],e_point)


def escape(my_robot,enemy_robot_1,enemy_robot_2,enemy_num,map):
    costmap = cost.cost(enemy_robot_1.coordinate[0],enemy_robot_2.coordinate[0],enemy_num)
    min_length = 100
    e_point = my_robot.coordinate
    for i in range(44):
        for j in range(80):
            length = math.sqrt((float(my_robot.coordinate[0][0])-i)**2+(float(my_robot.coordinate[0][1])-j)**2)
            if((costmap[i,j] == 2) & (length<min_length)):
                min_length = length
                e_point = [i,j]
    return map.planning(my_robot.coordinate[0],e_point)