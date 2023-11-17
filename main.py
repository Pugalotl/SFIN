import sys
import math
import sys
#import os

ARRAY_LENGTH = 4

array = bytearray((ARRAY_LENGTH//8)+1)

command_line_args = sys.argv[1:]
program = ""

counts = 0
pointer = 0
memory = 0
jump = -1

notes = []
note_num = 0

binary_rep = {
    ">": 0,
    "?": 1,
    "v": 2,
    "|": 3
}

def set_2_bit(arr,pos,val):
    return arr | (val << ((3-pos)*2))

while (counts < len(command_line_args)):
    if (command_line_args[counts] == "-h"):
        print("""
            SFIN: A simplistic esolang
            Command-line arguments:
            -h  Prints this menu
            -f  Reads the program from a text file
            -s  Reads the program from a string
            -n  Reads notes from a file based on lines (used for debugging)
            -b  Reads from a binary file (to be added)
            -c  Compiles the current program into a binary file
            
            For example:
            python main.py -s ">>>>" -c awesome.bin
            """)
        sys.exit()
    if (command_line_args[counts] == "-s"):
        if (counts + 1 < len(command_line_args)):
            counts += 1
            program = command_line_args[counts]
    if (command_line_args[counts] == "-f"):
        if (counts + 1 < len(command_line_args)):
            counts += 1
            with open(command_line_args[counts]) as f:
                program = f.read()
    if (command_line_args[counts] == "-n"):
        if (counts + 1 < len(command_line_args)):
            counts += 1
            with open(command_line_args[counts]) as f:
                notes = f.readlines()
    if (command_line_args[counts] == "-b"):
        if (counts + 1 < len(command_line_args)):
            counts += 1
            with open(command_line_args[counts],"rb") as f:
                read_array = f.read()
                for b in read_array:
                    for i in range(4):
                        program += list(binary_rep.keys())[list(binary_rep.values()).index((b>>((3-i)*2))&3)]
    if (command_line_args[counts] == "-c"):
        if (counts + 1 < len(command_line_args)):
            counts += 1
            write_array = bytearray(((len(program)-1)//4)+1)
            counter = 0
            byte = 0
            for p in program:
                if p in binary_rep:
                    write_array[byte] = set_2_bit(write_array[byte],counter,binary_rep[p])
                    counter += 1
                    if (counter == 4):
                        byte += 1
                        counter = 0
            with open(command_line_args[counts],"wb") as f:
                f.write(write_array)
            sys.exit()
                
    counts += 1



def clamp(n, smallest, largest): 
    return max(smallest, min(n, largest))
    
def nand(a, b):
    return not (a and b) 

def get_bit(pos):
    global array
    return (array[pos//8] >> (7-(pos%8)) & 1)
    
def set_bit(pos, val):
    global array
    array[pos//8] = array[pos//8] & ~(1 << (7-(pos%8)))
    array[pos//8] = array[pos//8] | (val << (7-(pos%8)))
    
   

    
jumps = []
  
x = 0  
while x < (len(program)):
    if (program[x] == "|"):
        if (x+2>len(program)):
            jumps.append(x)
        elif (program[x+1] != "|"):
            jumps.append(x)
        else:
            while(x+1<len(program) and program[x] == "|"):
                x += 1
    x += 1
    
i = 0
 
while (i < len(program)):
    char = program[i]
    if (char == ">"):
        pointer = pointer + 1
        if (pointer > ARRAY_LENGTH-1):
            pointer = 0
    if (char == "v"):
        set_bit(pointer, nand(get_bit(pointer), memory))
    if (char == "?"):
        if (i+1<len(program) and program[i+1] == "?"):
            while (i+1<len(program) and program[i+1] == "?"):
                if (get_bit(pointer) == 0 and memory == 0):
                    array.extend(bytearray((ARRAY_LENGTH//8)+1))
                    ARRAY_LENGTH = ARRAY_LENGTH * 2
                elif (get_bit(pointer) == 1 and memory == 0):
                    set_bit(pointer, input("> ")[0] == "1")
                elif (memory == 1):
                    print("0" if get_bit(pointer) == 0 else "1")
                i += 1
        else:
            memory = get_bit(pointer)
    if (char == "d"):
        print(bin(array[pointer//8])[2:].rjust(8,"0"),"\t",memory,",",pointer,"\t",notes[note_num] if note_num < len(notes) else "")
        note_num += 1
    if (char == "|"):
        counter = -1
        while (i+1<len(program) and program[i+1] == "|"):
            counter += 1
            i += 1
        if (counter > -1 and memory == 0):
            i = jumps[counter]
        
        
    #os.system("pause > nul")
    i += 1
   