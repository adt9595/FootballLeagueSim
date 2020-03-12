# -*- coding: utf-8 -*-
"""
Function to return true if there are 2 numbers in a list that add up to n, else false
"""
import math
        

#coords = [[1,2], [2,3], [1,-3]]
#vertex = [2,2]
#num_points = 2

def find_closest(coords,vertex,num_points):
    if num_points < 0:
        raise ValueError("Cannot have a negative number of points")
    smallest_coord = [math.inf,math.inf]
    for coord in coords:
        if distance(coord,vertex) < distance(smallest_coord,vertex):
            smallest_coord = coord
    return smallest_coord
    
def distance(a,b):
    return math.sqrt((b[1]-a[1])**2 + (b[0] - a[0])**2)


#print(find_closest(coords,vertex,1))
def min_coins(pennies):
    if pennies == 0:
        return 0
    if pennies < 0:
        raise ValueError("Cannot have negative money")
    num = 0
    coins = [200, 100, 50, 20, 10, 5, 2, 1]
    while pennies > 0:
        for coin in coins:
            if pennies >= coin:
                pennies = pennies - coin
                num += 1
                break
    return num

meetings = [['9:00','10:00']]

def meeting_times(calendar,bounds):
    times = []
    num_meetings = len(calendar)
    bh1,bm1 = split_time(bounds[0])
    bh2,bm2 = split_time(bounds[1])
    for i in range(num_meetings-1):
        h1,m1 = split_time(calendar[i][1])
        h2,m2 = split_time(calendar[i+1][0])
        if (h1 > bh1) or (h1 == bh1 and m1 >= bm1):
            times.append(calendar[i][1])
        if (h2 < bh2) or (h2 == bh2 and m2 <= bm2):
            times.append(calendar[i+1][0])

        
        
        
    
def split_time(time):
    h,m = time.split(':')
    return int(h),int(m)

meeting_times(meetings,[])

              


#def give_change(wealth,price):
    

