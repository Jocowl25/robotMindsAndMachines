import array
import sys 
#new_limit = 200000 
#sys.setrecursionlimit(new_limit)
class tile(object):
    #constuctor
    def __init__(self,tuple_int_postion_temp,arr_ping_temp=" ", arr_pings_on_temp=[],safe_temp =False):
        self.arr_ping = arr_ping_temp
        self.arr_pings_on = arr_pings_on_temp
        self.tuple_int_postion = tuple_int_postion_temp 
        self.safe = safe_temp

    def print_tile(tile):
        print(" ("+str(tile.tuple_int_postion[0])+" , "+str(tile.tuple_int_postion[1])+") ")

    def determine_tile_safeness(tile ,arr_new_ping_on):
        if(tile.safe == True):
            return
        if( len(arr_new_ping_on) == 0):
            tile.safe =True
            tile.arr_pings_on = []
            return
            #add  wopus check to see if only one 
            #add  coins check to see if only one 
        if(len(tile.arr_pings_on) == 0 ):
            tile.arr_pings_on = arr_new_ping_on             
        else:

            return
        
        

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
    temp = input("Give the danger level").split()
    print(len(temp))
    return temp
    



def plot_movement(current_postion,nextpostion,found,set_of_locations):
    global total_board
    if(found):
        return
    cur_X = current_postion[0]
    cur_y = current_postion[1]


    temp = set_of_locations
    temp.append((cur_X,cur_y))
    #change to be checking for safe
    if(total_board[cur_X][cur_y].safe==True):
        #makes sure it leaves if it gets a good value aready
        if(found):
            return
        if(current_postion[0] == nextpostion[0] and current_postion[1] == nextpostion[1]):
            found = True
            print("hit here")
            set_of_locations =temp
            return True
        else:
            
            if((cur_X !=len(total_board)-1) and  (found ==False)):
                if(cur_X+1,cur_y) in temp:
                    print()
                else:
                    found = plot_movement((cur_X+1,cur_y),nextpostion,found,temp)
                    
            if(cur_y !=len(total_board[cur_X])-1 and (found ==False)):
                if(cur_X,cur_y+1) in temp:
                    print()
                else:
                    found =  plot_movement((cur_X,cur_y+1),nextpostion,found,temp)
                           

            if((cur_X !=0 ) and (found ==False)):
                if(cur_X-1,cur_y) in temp:
                    print()
                else:
                    found = plot_movement((cur_X-1,cur_y),nextpostion,found,temp)
                    
                    
                
            
                    
            
            if(cur_y!=0 and (found ==False)):
                if(cur_X,cur_y-1) in temp:
                    print()
                else:
                    found = plot_movement((cur_X,cur_y-1),nextpostion,found,temp)
                    
                    
                
    else:
        temp.pop()
        return

print("start of algorythm test")
temp_solution = []
plot_movement((0,0),(3,3),False,temp_solution)
for i in temp_solution:
    x= i[0]
    y=i[1]
    total_board[x][y].print_tile()



safes =[(0,0)]
print("start of printing test")  
for i in range(4):
    currentline =""
    for j in range(4):
        pos = (j,i)
        if pos in temp_solution:
            currentline = "X"+" "+currentline
        else:
            currentline = " "+" "+currentline
    print(currentline)
    
def alocating_pings(current_postion):
    global total_board
    global safes
    array_of_pings = input_of_danger(current_postion)
    cur_X = current_postion[0]
    cur_y = current_postion[1]
    if((cur_X !=len(total_board)-1)):
        next_x = cur_X+1
        next_y = cur_y
        total_board[next_x][next_y].determine_tile_safeness(array_of_pings)
        print((total_board[next_x][next_y].safe))
        if(total_board[next_x][next_y].safe ==True):
            if (next_x,next_y) in safes:
                print("is there")
            else:
                safes.append((next_x,next_y))

    if(cur_y !=len(total_board[cur_X])-1):
        next_x = cur_X
        next_y = cur_y+1
        total_board[next_x][next_y].determine_tile_safeness(array_of_pings)
        print((total_board[next_x][next_y].safe))
        if(total_board[next_x][next_y].safe ==True):
            if (next_x,next_y) in safes:
                print("is there")
            else:
                safes.append((next_x,next_y))

    if((cur_X !=0 )):
        next_x = cur_X-1
        next_y = cur_y
        total_board[next_x][next_y].determine_tile_safeness(array_of_pings)
        print((total_board[next_x][next_y].safe))
        if(total_board[next_x][next_y].safe ==True):
            if (next_x,next_y) in safes:
                print("is there")
            else:
                safes.append((next_x,next_y))
    if((cur_y !=0 )):
        next_x = cur_X
        next_y = cur_y
        total_board[next_x][next_y].determine_tile_safeness(array_of_pings)
        print((total_board[next_x][next_y].safe))
        if(total_board[next_x][next_y].safe ==True):
            if (next_x,next_y) in safes:
                print("is there")
            else:
                safes.append((next_x,next_y))
    print(len(safes))



i = 0
while(i<len(safes)):
    alocating_pings(safes[i])
    print(len(safes))
    next = i + 1
    found_set = []
    plot_movement(safes[i],safes[next],False,found_set)
    for k in range(4):
        currentline =""
        for j in range(4):
            pos = (j,k)
            if pos in found_set:
                currentline = "X"+" "+currentline
            else:
                currentline = " "+" "+currentline
        print(currentline)

    i+=1