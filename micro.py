import numpy as np
import time
import RPi.GPIO as GPIO

#fornt sensor
def dis_front(wall_f):
    global min_distance
    start_f = 0
    end_f = 0
    GPIO.output(TRIG_F, False)
    time.sleep(0.01)
    GPIO.output(TRIG_F, True)
    time.sleep(0.0001)
    GPIO.output(TRIG_F, False)

    while GPIO.input(ECHO_F) == False:
        start_f = time.time()

    while GPIO.input(ECHO_F) == True:
        end_f = time.time()

    sig_time_f = end_f-start_f

    #CM:
    distance_f = sig_time_f / 0.000058
    if distance_f > min_distance:
        return False
    else:
        return True
    
    time.sleep(0.01)

#left sensor
def dis_left(wall_l):
    global min_distance
    start_l = 0
    end_l = 0
    sig_time_l = 0
    GPIO.output(TRIG_L, False)
    time.sleep(0.01)
    GPIO.output(TRIG_L, True)
    time.sleep(0.0001)
    GPIO.output(TRIG_L, False)

    while GPIO.input(ECHO_L) == False:
        start_l = time.time()

    while GPIO.input(ECHO_L) == True:
        end_l = time.time()

    sig_time_l = end_l-start_l

    #CM:
    distance_l = sig_time_l / 0.000058
    if distance_l > min_distance:
        return False
    else:
        return True
    time.sleep(0.01)
   

#right sensor
def dis_right(wall_r):
    global min_distance
    start_r = 0
    end_r = 0
    GPIO.output(TRIG_R, False)
    time.sleep(0.01)
    GPIO.output(TRIG_R, True)
    time.sleep(0.0001)
    GPIO.output(TRIG_R, False)

    while GPIO.input(ECHO_R) == False:
        start_r = time.time()

    while GPIO.input(ECHO_R) == True:
        end_r = time.time()

    sig_time_r = end_r-start_r

    #CM:
    distance_r = sig_time_r / 0.000058
    if distance_r > min_distance:
        return False
    else:
        return True
    
    time.sleep(0.01)


#value of cell
def value():
    maps = []
    m=17
    for i in range(16):
        for j in range(16):
            if((i<=7) and (j<8)):                                   
                    m=m-1
                    values=m   
                       
            if((i<=7) and (j>=9)):
                m=m+1
                values=m
            if((i>=9) and (j<8)):
                    if i==9 and j==0:
                        m=m-1
                    m=m-1
                    values=m   
                       
            if((i>=9) and (j>=9)):

                m=m+1
                values=m
             
            if((i==8) and (j<8)):                                   
                values=m
                m=m-1
                       
            if((i==8) and (j>=8)):
                if i==8 and j==8 :
                    m=m+1
                values=m
                m=m+1
                         
            maps.append(values)
        if(i>=8):
            m=m+2
    return maps

#move predict
def move(r,c,face,maps,wall):
    neib = {}
    l_wall = wall[0]
    f_wall = wall[1]
    r_wall = wall[2]
    # print('l f r ',wall)
    if dis_front(f_wall) == False:
        if face == 'n' and r-1 >= 0:
            neib[(r-1,c)] = maps[r-1][c]
        elif face == 'e' and c+1 < 16:
            neib[(r,c+1)] = maps[r][c+1]
        elif face == 'w' and c-1 >= 0:
            neib[(r,c-1)] = maps[r][c-1]
        elif face == 's' and r+1 < 16:
            neib[(r+1,c)] = maps[r+1][c]              
                         
    if dis_left(l_wall) == False:
        if face == 'n' and c-1 >= 0:
            neib[(r,c-1)] = maps[r][c-1]
        elif face == 'e' and r-1 >= 0:
            neib[(r-1,c)] = maps[r-1][c]
        elif face == 'w' and r+1 < 16:
            neib[(r+1,c)] = maps[r+1][c]
        elif face == 's' and c+1 < 16:
            neib[(r,c+1)] = maps[r][c+1]                   
    
    if dis_right(r_wall) == False:
        if face == 'n' and c+1 < 16:
            neib[(r,c+1)] = maps[r][c+1]
        elif face == 'e' and r+1 < 16:
            neib[(r+1,c)] = maps[r+1][c]
        elif face == 'w' and r-1 >= 0:
            neib[(r-1,c)] = maps[r-1][c]
        elif face == 's' and c-1 >= 0:
            neib[(r,c-1)] = maps[r][c-1]
     
    if dis_right(r_wall) == True and dis_left(l_wall) == True and dis_front(f_wall) == True:
        if face == 'n' and r+1 < 16:
            neib[(r+1,c)] = maps[r+1][c]
        elif face == 'e' and c-1 >=0:
            neib[(r,c-1)] = maps[r][c-1]
        elif face == 'w' and c+1 < 16:
            neib[(r,c+1)] = maps[r][c+1]
        elif face == 's' and r-1 >= 0:
            neib[(r-1,c)] = maps[r-1][c]
    
    return neib
 
def correct(r,c,face,maps,path,wall):
    global count
    neib = move(r=r,c=c,face=face,maps=maps,wall=wall)
    n = {}
    # print(path)
    for each in neib.keys():
        
        count.append(each)

    ''' for each in list(neib.keys()):
        if count.count(each)>3:
            x={,}
            x.append(count.count(each)
            
            del neib[each]'''
        

    if len(neib)>= 2:
        for i in list(neib.keys()):
            if i in path:
                n[i]=neib[i]
                del neib[i]
    # print(neib)
    
    if len(neib) >= 1:
        minm = []
        for i in neib.values():
            minm.append(i)
        min_val = min(minm)
        a = list(neib.keys())[list(neib.values()).index(min_val)]
        return a

    if len(neib) < 1:
        minm = []
        for i in n.values():
            minm.append(i)
        min_val = min(minm)
        a = list(n.keys())[list(n.values()).index(min_val)]
        return a

#move from start to center
def make_move(r,c,rs,cs,face):
    #print('r ',r,' c ',c,' cs ',cs,' rs ',rs)
    if face =='n':
        if rs > r and cs==c:
            return 'f'
        elif rs < r and cs == c :
            return 'b'
        elif cs > c and rs == r:
            return 'l'
        elif cs < c and rs == r:
            return 'r'
    
    if face == 'e':
        if rs < r and cs==c:
            return 'r'
        elif rs > r and cs==c :
            return 'l'
        elif cs > c and rs==r:
            return 'b'
        elif cs < c and rs==r:
            return 'f'
    if face == 'w':
        if rs < r and cs==c:
            return 'l'
        elif rs > r and cs==c:
            return 'r'
        elif cs > c and rs==r:
            return 'f'
        elif cs < c and rs==r:
            return 'b'
    if face == 's':
        if rs < r and cs==c:
            return 'f'
        elif rs > r and cs==c:
            return 'b'
        elif cs > c and rs==r:
            return 'r'
        elif cs < c and rs==r:
            return 'l'


'''move forward'''
def forw(r,c,face):
        # print("r_poss: ",r," c_poss: ",c," face: ",face)
    if face == 'n':
        r = r - 1       
    elif face == 's':
        r = r + 1    
    elif face == 'e':
        c = c + 1    
    elif face == 'w':
        c = c - 1        
    
    # print("r_poss: ",r_pos," c_poss: ",c_pos," face: ",face)
    return r,c


'''turn right'''
def right(face):
    if face == 'n':
        face = 'e'        
    elif face == 's':
        face = 'w'    
    elif face == 'e':
        face = 's'    
    elif face == 'w':
        face = 'n'     
    

    return  face


'''turn left'''
def left(face):
    
    if face == 'n':
        face = 'w'
        
    elif face == 's':
        face = 'e'
    
    elif face == 'e':
        face = 'n'
    
    elif face == 'w':
        face = 's' 
    #moter move
    
    return  face


'''turn back'''
def back(face):
    if face == 'n':
        face = 's'
        
    elif face == 's':
        face = 'n'
    
    elif face == 'e':
        face = 'w'
    
    elif face == 'w':
        face = 'e' 
    
    return  face


def robot_move(r,c,face,m):
    if m == 'f':
       r,c = forw(r=r,c=c,face=face)
    elif m == 'r':
       face = right(face=face)
       r,c = forw(r=r,c=c,face=face)
    elif m == 'l':
        face = left(face=face)
        r,c = forw(r=r,c=c,face=face)
    elif m == 'b':
        face = back(face=face)
        r,c = forw(r=r,c=c,face=face)

    return r,c,face        

def duplicate(lst,item):
    return [i for i,x in enumerate(lst) if x==item]


#path reduce
def path_opt(pos,pat):
    ck = []
    a = 0
    b = 1
    print(len(pat))
    # print(poss)
    for i in pat:
        x = duplicate(pat,i)
        if len(x) > 1 and x[0] > b:
            a = x[0]
            b = x[-1]
            ck.append(a)
            ck.append(b)

    print(ck)
    for i in range(0,len(ck),2):
        if i == 0:
            a = ck[i]
            b = ck[i+1]
            del pat[a:b]
            # print(pat)
        else:
            pat = path_opt(pos=pos,pat=pat)

    # for i in range(0,len(ck),2)
    # for i in poss.keys():
    #     if i in path:
    #         for j in path:
    #             if j in poss[i]:
    #                 ck.append(j)

    
    # for i in range(0,len(ck),2):
    #     try:
    #         a = path.index(ck[i])
    #         b = path.index(ck[i+1])
    #         if ck[i] and ck[i+1] in path:
    #             del path[a+1:b]
    #     except:
    #         break

    return pat


#pin setup mode
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

min_distance = 10

TRIG_F = 18 #trigger front
ECHO_F = 23 #echo front
TRIG_L = 20 #trigger left
ECHO_L = 8 #echo front
TRIG_R = 27 #trigger right
ECHO_R = 17 #echo front

#pin setup
GPIO.setup(TRIG_F,GPIO.OUT)
GPIO.setup(ECHO_F,GPIO.IN)
GPIO.setup(TRIG_L,GPIO.OUT)
GPIO.setup(ECHO_L,GPIO.IN)
GPIO.setup(TRIG_R,GPIO.OUT)
GPIO.setup(ECHO_R,GPIO.IN)
poss = {}
count = []
path = []
r_poss = 15
c_poss = 0
face = 'n'
maps = value() #map cell value
maps = np.array(maps).reshape(16,16)
min_distance = 10


#To find path
def find_path(wall):
    global path
    global r_poss
    global c_poss
    global face
    global maps
    global poss
    center = False
    while not center:    
        cell_value = maps[r_poss][c_poss]
        if cell_value == 2:
            center = True
            break
        p = move(r_pos=r_poss,c_pos=c_poss,face=face,maps=maps,wall=wall)
        if len(p) > 1:
            poss[(r_poss,c_poss)] = list(p.keys())
        mov = correct(r_pos=r_poss,c_pos=c_poss,face=face,maps=maps,path=path,wall=wall)
        r,c = mov[0][0],mov[0][1]
        m =  make_move(r=r,c=c,r_pos=r_poss,c_pos=c_poss,face=face)
        r_poss,c_poss,face = robot_move(r_poss=r_poss,c_poss=c_poss,face=face,m=m)
        path.append(mov)
        print("r_poss: ",r_poss," c_poss: ",c_poss," cell_value: ",cell_value," move: ",m," face:",face)          
    
    path.append(mov)
    path = path_opt(pos=poss,pat=path)
    

def reset():
    global r_poss
    global c_poss
    global face
    r_poss =15
    c_poss = 0
    face = 'n'

def speed_comp(i):
    global path
    global r_poss
    global c_poss
    global face
    for i in path:
        r,c = i
        m =  make_move(r=r,c=c,rs=r_poss,cs=c_poss,face=face)
        r_poss,c_poss,face = robot_move(r=r_poss,c=c_poss,face=face,m=m)
# GPIO.setup(21, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) # Set pin 21 to be an input pin and set initial value to be pulled low (off)
# GPIO.add_event_detect(21,GPIO.RISING,callback=find_path) # Setup event on pin 21 rising edge
# GPIO.setup(20, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) # Set pin 20 to be an input pin and set initial value to be pulled low (off)
# GPIO.add_event_detect(20,GPIO.RISING,callback=speed_comp) # Setup event on pin 20 rising edge
# message = input("Press enter to quit\n\n") # Run until someone presses enter

# find_path()
# re_start()
# speed_comp()
GPIO.cleanup() # Clean up
