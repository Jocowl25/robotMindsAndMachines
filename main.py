import array
import sys 
new_limit = 200000 
sys.setrecursionlimit(new_limit)
class tile(object):
    
    def __init__(self,tuple_int_postion_temp,char_input_temp=" ", char_tile_state_temp=" "):
        self.char_input = char_input_temp
        self.char_tile_state = char_tile_state_temp
        self.tuple_int_postion = tuple_int_postion_temp 
    def print_tile(tile):
        print(" ("+str(tile.tuple_int_postion[0])+" , "+str(tile.tuple_int_postion[1])+") ")

first_row = [tile([0,0]),tile([0,1]),tile([0,2]),tile([0,3])]
second_row = [tile([1,0]),tile([1,1]),tile([1,2]),tile([1,3])]
third_row = [tile([2,0]),tile([2,1]),tile([2,2]),tile([2,3])]
fourth_row = [tile([3,0]),tile([3,1]),tile([3,2]),tile([3,3])]
total_board = [first_row,second_row,third_row,fourth_row]

visited =[]

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
    
def input_of_danger(current_postion):
    global total_board
    x = current_postion[0]
    y =current_postion[1]
    total_board[x][y].char_input = input("Give the danger level") 



def plot_movement(current_postion,nextpostion,found,set_of_locations):
    global total_board
    if(found):
        return
    cur_X = current_postion[0]
    cur_y = current_postion[1]


    temp = set_of_locations
    temp.append((cur_X,cur_y))
    if(total_board[cur_X][cur_y].char_tile_state==" "):
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
        return

print("start of algorythm test")
temp_solution = []
plot_movement((0,0),(3,3),False,temp_solution)
for i in temp_solution:
    x= i[0]
    y=i[1]
    total_board[x][y].print_tile()
    
for i in total_board:
    currentline =""
    for j in i:
        pos = j.tuple_int_postion
        if pos in temp_solution:
            currentline = currentline+"X"
        else:
            currentline = currentline+" "
    print(currentline)
    