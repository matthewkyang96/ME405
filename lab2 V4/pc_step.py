import serial
from matplotlib import pyplot


ser = serial.Serial('COM4',38400)
print('Press a key to start')
input()

print('please input theta ref')
x = input()
x = str(x) + '\r'
ser.write(x.encode('utf-8'))

print('please input Kp')
y = input()
y = str(y) + '\r'
ser.write(y.encode('utf-8'))

while ser.in_waiting > 0:
    data = ser.readline()
    data = data.decode('utf-8')
    theta_ref = data
    data = ser.readline()
    data = data.decode('utf-8')
    Kp = data
    data = ser.readline()
    data = data.decode('utf-8')
    time = data
    data = ser.readline()
    data = data.decode('utf-8')
    position = data
    
time= time.split(',')
time= [s.strip('\n') for s in time]
time= [s.strip('\r') for s in time]
time= [s.strip('[') for s in time]
time= [s.strip(']') for s in time]

position = position.split(',')
position = [s.strip('\n') for s in position]
position = [s.strip('\r') for s in position]
position = [s.strip('[') for s in position]
position = [s.strip(']') for s in position]

    
time= list(time)
time = [float(i) for i in time]
print(time)
position = list(position)
position = [float(i) for i in position]
print(position)
pyplot.plot(time,position)
pyplot.show()
 
 
    

#ser.flush()
#inputs = []
#for line in range(3):
#    inputs.append(ser.readline())
#time = ser.readline()
#position = ser.readline()
#print(time)
#print(position)

     
     
        
        