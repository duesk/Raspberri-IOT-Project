from printrun.printcore import printcore
import sys
import time

def temp_callback(a):
    print('temp_cfasdfallback', a)

p = printcore('/dev/ttyACM0',  115200)
p.tempcb = temp_callback
while not p.online:
    time.sleep(0.1)
print('online')
p.send_now("M105")
time.sleep(10)
#p._listen()

#disconnect to exit the listening thread and the main thread
#p.disconnect()