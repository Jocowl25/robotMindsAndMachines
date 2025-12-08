import array
import sys 


class tile(object):
    #constuctor
    def __init__(self,tuple_int_postion_temp,arr_ping_temp=" ", arr_pings_on_temp=[],safe_temp =False):
        self.arr_ping = arr_ping_temp
        self.arr_pings_on = arr_pings_on_temp
        self.tuple_int_postion = tuple_int_postion_temp 
        self.safe = safe_temp
        self.gold = False
        self.wumpus_possiblity =False

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
        
        
one_wopus_space =False
first_row = [tile([0,0]),tile([0,1]),tile([0,2]),tile([0,3])]
second_row = [tile([1,0]),tile([1,1]),tile([1,2]),tile([1,3])]
third_row = [tile([2,0]),tile([2,1]),tile([2,2]),tile([2,3])]
fourth_row = [tile([3,0]),tile([3,1]),tile([3,2]),tile([3,3])]
total_board = [first_row,second_row,third_row,fourth_row]
total_board[0][0].safe =True


for i in range(4):
    for j in range(4):
        total_board[i][j].print_tile()
        




def next_square(rotation,tuplecurrentpostion):
    rotation = rotation%360
    if(rotation ==0):
        if(tuplecurrentpostion[1]==0):
            return "ERROR cannot do that"
        else:
            tuplecurrentpostion[1]=tuplecurrentpostion[1]-1
            total_board.append(total_board)
            return "completed"
    elif(rotation==90):
        if(tuplecurrentpostion[0]==3):
            return "ERROR cannot do that"
        else:
            tuplecurrentpostion[0]=tuplecurrentpostion[0]+1

            return "completed"
    elif(rotation==180):
        if(tuplecurrentpostion[1]==3):
            return "ERROR cannot do that"
        else:
            tuplecurrentpostion[1]=tuplecurrentpostion[1]+1
            return "completed"
    elif(rotation==270):
        if(tuplecurrentpostion[0]==0):
            return "ERROR cannot do that"
        else:
            tuplecurrentpostion[0]=tuplecurrentpostion[0]-1
            return "completed"
    

#takes input and return list of pings    
def input_of_danger(current_postion):

    print("at location " +str(current_postion[0])+ ","+str(current_postion[1]))
    temp = input("Give the danger level ").split()
    

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
            return True
        else:
            
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
        return False


safes =[(0,0)]
total_board[0][0].safe =True
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
def  update_the_knowns_golds(current_postion):
    global total_board
    
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
        if((cur_x,cur_y+1) ==next_postion):
            rotation = "South"
        elif((cur_x,cur_y-1) ==next_postion):
            rotation ="North"
        elif((cur_x-1,cur_y) ==next_postion):
            rotation ="East"
        elif((cur_x+1,cur_y) ==next_postion):
            rotation ="West"
        print(rotation)




i = 0
while((i<len(safes))):
    
    if(alocating_pings(safes[i])):
        found_set = []
        plot_movement(safes[i],(0,0),False,found_set)
        print(len(found_set))
       
        break 

    update_the_knowns_golds(safes[i])
    update_the_knowns_wompus(safes[i])
    print(len(safes))
    next = i + 1
    found_set = []
    if( i == len(safes)-1):
        if(one_wopus_space==True):
            print("shot wompus")
            

            plot_movement(safes[i],wompus_detected_cord,False,found_set)
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
        doing_moveing(found_set)
        print(len(found_set))
        i=i+1
    #where to put move function
    for k in range(4):
        currentline =""
        for j in range(4):
            pos = (j,k)
            if pos in found_set:

                currentline = "X"+"|"+currentline
            else:
                if(total_board[pos[0]][pos[1]].gold):
                    currentline = "G"+"|"+currentline
                elif(not(total_board[pos[0]][pos[1]].safe)and len(total_board[pos[0]][pos[1]].arr_pings_on) >0):
                    currentline = "D"+"|"+currentline
                else:
                    currentline = " "+"|"+currentline
        print(currentline)
doing_moveing(found_set)
for l in found_set:
    total_board[l[0]][l[1]].print_tile()
for k in range(4):
    currentline =""
    for j in range(4):
        pos = (j,k)
        if pos in found_set:
            currentline = "X"+"X"+currentline
        else:
            if(total_board[pos[0]][pos[1]].gold):
                currentline = "G"+"|"+currentline
            else:
                currentline = " "+"|"+currentline
    print(currentline)




    
