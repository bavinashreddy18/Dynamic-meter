
# import fileinput
import fileinput
  
# Using fileinput.input() method
while True:
    for line in fileinput.input(files ='temp'):
        print(line)
    
    for packet in fileinput.input(files ='temp2'):
        print(packet)
    y =  (100000000 - (float(line)*1000))
    print(y)
    z = (long(packet) - y)*0.0000001
    print(z)
    t = (z/(long(packet)*0.0000001))
    print(t)
    x = 1 - t
    print(x)

    file= open('direct_commands.txt', 'r')
    data = file.readlines() 

    print(data) 
    data[4] = "meter_array_set_rates my_meter "+ str(x) +":1 0.96:1"

    with open('direct_commands.txt', 'w') as file: 

        file.writelines(data)