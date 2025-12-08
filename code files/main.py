from nanonav import BLE, NanoBot
import time
from machine import Pin
Pin(28, Pin.OUT).on()

robot = NanoBot()

ble = BLE(name="NanoNav2")

SEARCH_SPEED   = 20
ALIGN_SPEED    = 15
TURN_SPEED     = 20
CROSS_SPEED    = 20
LOOP_DELAY     = 0.02

position_x = 0
position_y = 0
facing = 0

def find_and_center_on_line():
    print("Finding initial line...")
    
    while True:
        left  = robot.ir_left()
        right = robot.ir_right()

        if not left and not right:
            robot.m1_forward(SEARCH_SPEED)
            robot.m2_forward(SEARCH_SPEED)
        else:
            robot.stop()
            time.sleep(0.1)
            break
        time.sleep(LOOP_DELAY)

    print("Aligning to line...")
    while True:
        left  = robot.ir_left()
        right = robot.ir_right()

        if left and right:
            robot.stop()
            time.sleep(0.1)
            break

        if left and not right:
            robot.m1_forward(ALIGN_SPEED)
            robot.m2_backward(ALIGN_SPEED)

        elif right and not left:
            robot.m1_backward(ALIGN_SPEED)
            robot.m2_forward(ALIGN_SPEED)

        else:
            robot.m1_backward(ALIGN_SPEED)
            robot.m2_backward(ALIGN_SPEED)

        time.sleep(0.05)
        robot.stop()
        time.sleep(0.03)
    
    print("Centered on line!")

def drive_to_next_line():
    global position_x, position_y, facing
    
    print(f"Driving to next line... Current position: ({position_x}, {position_y}), Facing: {facing}")
    
    while True:
        left = robot.ir_left()
        right = robot.ir_right()
        
        if left and right:
            robot.stop()
            time.sleep(0.5)
            break
        
        robot.m1_forward(CROSS_SPEED)
        robot.m2_forward(CROSS_SPEED)
        time.sleep(LOOP_DELAY)
    
    robot.m1_forward(CROSS_SPEED)
    robot.m2_forward(CROSS_SPEED)
    time.sleep(0.3)
    robot.stop()
    time.sleep(0.2)
    
    if facing == 0:
        position_y += 1
    elif facing == 1:
        position_x -= 1
    elif facing == 2:
        position_y -= 1
    elif facing == 3:
        position_x += 1
    
    print(f"Reached next line! New position: ({position_x}, {position_y})")

def turn_right_90():
    global facing
    
    robot.set_enc1(0)
    robot.set_enc2(0)
    
    while abs(robot.get_enc1()) < robot.turn90ticks or abs(robot.get_enc2()) < robot.turn90ticks:
        robot.m1_forward(TURN_SPEED)
        robot.m2_backward(TURN_SPEED)
        time.sleep(0.02)
    
    robot.stop()
    time.sleep(0.3)
    
    facing = (facing + 1) % 4
    print(f"Turned right. Now facing: {facing}")

def turn_left_90():
    global facing
    
    robot.set_enc1(0)
    robot.set_enc2(0)
    
    while abs(robot.get_enc1()) < robot.turn90ticks or abs(robot.get_enc2()) < robot.turn90ticks:
        robot.m1_backward(TURN_SPEED)
        robot.m2_forward(TURN_SPEED)
        time.sleep(0.02)
    
    robot.stop()
    time.sleep(0.3)
    
    facing = (facing - 1) % 4
    print(f"Turned left. Now facing: {facing}")

def back_a_bit():
    robot.m1_backward(3)
    robot.m2_backward(3)
    time.sleep(0.5)

def go_up():
    drive_to_next_line()

def go_down():
    turn_left_90()
    turn_left_90()
    drive_to_next_line()
    drive_to_next_line()
    turn_left_90()
    turn_left_90()
    drive_to_next_line()

def go_right():
    turn_right_90()
    back_a_bit()
    drive_to_next_line()
    drive_to_next_line()
    turn_left_90()

def go_left():
    turn_left_90()
    back_a_bit()
    drive_to_next_line()
    drive_to_next_line()
    turn_right_90()

def get_bluetooth_signal(): #0 safe, dont add, 1 wumpus m, 2 pit p, 3 glitter g, 4 gold G 5 done
    response = ble.read()
    values=[]
    while response!=5 or response!=0: #signal done or safe respectively
        if response==1: #
            values.append("m") #wumpus
        elif response==2:
            values.append("p") #pit
        elif response==3:
            values.append("g") #gold surrounding
        elif response==4:
            values.append("G") #on gold
        response = ble.read()
        return values
try:
    find_and_center_on_line()
    go_up()
    go_down()
    go_left()
    go_right()
    robot.stop()

except KeyboardInterrupt:
    robot.stop()
    print("\nStopped by user")


##start of algorythm 

#creation of tile objects
class tile(object):
    #constuctor
    def __init__(self,tuple_int_postion_temp,arr_ping_temp=" ", arr_pings_on_temp=[],safe_temp =False):
        self.arr_ping = arr_ping_temp
        self.arr_pings_on = arr_pings_on_temp
        self.tuple_int_postion = tuple_int_postion_temp 
        self.safe = safe_temp
        self.gold = False
        self.wumpus_possiblity =False
        self.visted = False

    def print_tile(tile):
        print(" ("+str(tile.tuple_int_postion[0])+" , "+str(tile.tuple_int_postion[1])+") ")

    def determine_tile_safeness(tile ,arr_new_ping_on):
        if(tile.gold):
            return
        
        if(tile.safe == True and len(tile.arr_pings_on) ==0 ):
            tile.wumpus_possiblity =False
            return
        if( len(arr_new_ping_on) == 0):
            tile.safe =True
            tile.arr_pings_on = []
            return
            
            
        # p = pit
        # m = wompus
        # g = gold
        if "m" in arr_new_ping_on:
            tile.wumpus_possiblity = True

        
        if(len(tile.arr_pings_on) == 0 ):
            
            if(len(arr_new_ping_on)==1 and arr_new_ping_on[0]== "g"):
                    
                    tile.safe =True
                    return
            tile.arr_pings_on = arr_new_ping_on             
        else:
            
            if(len(arr_new_ping_on)==len(tile.arr_pings_on)):
                if((len(arr_new_ping_on)==1) and not(arr_new_ping_on[0] == tile.arr_pings_on[0] ) ):
                    tile.arr_pings_on =[]
                    tile.safe =True
                return

            if(len(arr_new_ping_on)<len(tile.arr_pings_on)):
                tile.arr_pings_on = arr_new_ping_on  
                if(len(arr_new_ping_on)==1 and arr_new_ping_on[0]== "g"):
                    
                    tile.safe =True
                    return
      
            return
        


#creates boards
one_wopus_space =False
first_row = [tile([0,0]),tile([0,1]),tile([0,2]),tile([0,3])]
second_row = [tile([1,0]),tile([1,1]),tile([1,2]),tile([1,3])]
third_row = [tile([2,0]),tile([2,1]),tile([2,2]),tile([2,3])]
fourth_row = [tile([3,0]),tile([3,1]),tile([3,2]),tile([3,3])]
total_board = [first_row,second_row,third_row,fourth_row]
total_board[0][0].safe =True

#takes input and return list of pings    
def input_of_danger(current_postion):

    print("at location " +str(current_postion[0])+ ","+str(current_postion[1]))
    temp = get_bluetooth_signal()
    

    return temp
    



def plot_movement(current_postion,nextpostion,found,set_of_locations):
    global total_board
    if(found):
        return True
    cur_X = current_postion[0]
    cur_y = current_postion[1]

    total_board[cur_X][cur_y].print_tile
    temp = set_of_locations
    temp.append((cur_X,cur_y))

    #change to be checking for safe
    if(total_board[cur_X][cur_y].safe==True):
        #makes sure it leaves if it gets a good value aready
        if(found):
            return True

        if(current_postion[0] == nextpostion[0] and current_postion[1] == nextpostion[1]):
            found = True
            
            set_of_locations =temp
            return found

        if(total_board[cur_X][cur_y].visted==True):

            
            if((cur_X !=len(total_board)-1) and  (found ==False)):
                if(cur_X+1,cur_y) in temp:
                    t = False
                else:
                    found = plot_movement((cur_X+1,cur_y),nextpostion,found,temp)
                    
            if(cur_y !=len(total_board[cur_X])-1 and (found ==False)):
                if(cur_X,cur_y+1) in temp:
                    t = False
                    
                else:
                    found =  plot_movement((cur_X,cur_y+1),nextpostion,found,temp)
                           

            if((cur_X !=0 ) and (found ==False)):
                if(cur_X-1,cur_y) in temp:
                    t = False
                    
                else:
                    found = plot_movement((cur_X-1,cur_y),nextpostion,found,temp)
             
            if(cur_y!=0 and (found ==False)):
                if(cur_X,cur_y-1) in temp:
                    t = False
                else:
                    found = plot_movement((cur_X,cur_y-1),nextpostion,found,temp)
            if(not(found)):
                temp.pop()
            return found        
        else:
            temp.pop()
            return found 
    else:
        temp.pop()
        return False


safes =[(0,0)]
total_board[0][0].safe =True
total_board[0][0].visted = True
wompus_detected_cord = (-1,-1)
def alocating_pings(current_postion):
    global total_board
    global safes
    global wompus_detected_cord
    array_of_pings = input_of_danger(current_postion)
    if "G" in array_of_pings:
        return True

    if "m" in array_of_pings:
        wompus_detected_cord = current_postion
    cur_X = current_postion[0]
    cur_y = current_postion[1]
    if((cur_X !=len(total_board)-1)):
        next_x = cur_X+1
        next_y = cur_y
        total_board[next_x][next_y].determine_tile_safeness(array_of_pings)
        
        if(total_board[next_x][next_y].safe ==True):
            if (next_x,next_y) in safes:
                temp =True
            else:
                safes.append((next_x,next_y))

    if(cur_y !=len(total_board[cur_X])-1):
        next_x = cur_X
        next_y = cur_y+1
        total_board[next_x][next_y].determine_tile_safeness(array_of_pings)
        if(total_board[next_x][next_y].safe ==True):
            if (next_x,next_y) in safes:
                temp =True
            else:
                safes.append((next_x,next_y))

    if((cur_X !=0 )):
        next_x = cur_X-1
        next_y = cur_y
        total_board[next_x][next_y].determine_tile_safeness(array_of_pings)
        if(total_board[next_x][next_y].safe ==True):
            if (next_x,next_y) in safes:
                temp =True
            else:
                safes.append((next_x,next_y))
    if((cur_y !=0 )):
        next_x = cur_X
        next_y = cur_y
        total_board[next_x][next_y].determine_tile_safeness(array_of_pings)
        if(total_board[next_x][next_y].safe ==True):
            if (next_x,next_y) in safes:
                temp =True
            else:
                safes.append((next_x,next_y))
    
    return False
 

wompus_cords = (-1,-1)
gold_found = False
gold_cords = (-1,-1)
def  update_the_knowns_golds(current_postion):
    global total_board
    global gold_found
    global gold_cords
    num_gold = 0
    ping_of_one =(-1,-1)
    removing = True
    if(total_board[current_postion[0]][current_postion[1]].gold):
        removing = True
    for k in range(4):
        
        for j in range(4):
            pos = (j,k)
            if(total_board[j][k].safe):
                continue
            elif(len(total_board[j][k].arr_pings_on)==0):
                continue
            else:
                for temp in range(len(total_board[j][k].arr_pings_on)):
                    if (total_board[j][k].arr_pings_on[temp] =="g"):
                        if(removing):
                            total_board[j][k].arr_pings_on.pop(temp)
                        elif(num_gold == 0):
                            ping_of_one = (j,k)
                        num_gold = num_gold +1
    if(num_gold ==1):
        total_board[ping_of_one[0]][ping_of_one[1]].gold = True
        gold_cords = ping_of_one
        gold_found = True



def  update_the_knowns_wompus(current_postion):
    global total_board
    global one_wopus_space
    global wompus_cords
    ping_of_one =(-1,-1)
    num_wompus = 0
    
    for k in range(4):
        
        for j in range(4):
            pos = (j,k)
            if(total_board[j][k].safe):
                continue
            elif(len(total_board[j][k].arr_pings_on)==0):
                continue
            else:
                for temp in range(len(total_board[j][k].arr_pings_on)):
                    if (total_board[j][k].arr_pings_on[temp] =="m"):
                        if(num_wompus == 0):
                            ping_of_one = (j,k)
                        num_wompus = num_wompus +1
    if(num_wompus==1):
        one_wopus_space =True
        wompus_cords = ping_of_one


rotation = "North"
def doing_moveing(temp_found_set):
    global total_board
    global rotation
    for i in range(len(temp_found_set)):
        current_postion = temp_found_set[i]
        if (i == len(temp_found_set)-1):
            return
        next_postion = temp_found_set[i+1]
        cur_x = current_postion[0]
        cur_y = current_postion[1]
        #go south
        if((cur_x,cur_y+1) ==next_postion):
            rotation = "South"
            go_down()
        #go North
        elif((cur_x,cur_y-1) ==next_postion):
            rotation ="North"
            go_up()
        #go east
        elif((cur_x-1,cur_y) ==next_postion):
            rotation ="East"
            go_right()
        #go west
        elif((cur_x+1,cur_y) ==next_postion):
            rotation ="West"
            go_left()
        

def marking_as_vistited(temp_found_set):
    global total_board 
    for i in temp_found_set:
        total_board[i[0]][i[1]].visted = True

#START OF CODE
i = 0
while((i<len(safes))):
    update_the_knowns_golds(safes[i])
    if(gold_found):
        plot_movement(safes[i],gold_cords,False,found_set)
        i=i+1
        
    if(alocating_pings(safes[i])):
        found_set = []
        plot_movement(safes[i],(0,0),False,found_set)
        marking_as_vistited(found_set)
        print(len(found_set))
       
        break 

    
    update_the_knowns_wompus(safes[i])
    print(len(safes))
    next = i + 1
    found_set = []
    if( i == len(safes)-1):
        if(one_wopus_space==True):
            print("shot wompus")
            

            plot_movement(safes[i],wompus_detected_cord,False,found_set)
            marking_as_vistited(found_set)
            doing_moveing(found_set)
            total_board[wompus_cords[0]][wompus_cords[1]].wumpus_possiblity =False
            total_board[wompus_cords[0]][wompus_cords[1]].safe =True
            safes.append(wompus_cords)
            one_wopus_space =False
            i=i+1
            
        else:
            print("not possible")
            break
    else:
        
        plot_movement(safes[i],safes[next],False,found_set)
        marking_as_vistited(found_set)
        for l in found_set:
            total_board[l[0]][l[1]].print_tile()
        doing_moveing(found_set)
        
        i=i+1
    #where to put move function
    
doing_moveing(found_set)


