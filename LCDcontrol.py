#!/usr/bin/python

#resource monitor [cpu/mem] on lcd

from Adafruit_CharLCDPlate import Adafruit_CharLCDPlate
import psutil
import sys
import time
import threading
import Queue

global lcdMsg
global button_queue
global threads_run

threads_run = True

#create buffer for CPU usage
lcdMsg = 'Starting up!'
buffSize = 30
waitTime = 0.1
cpuBuff = []
dispRefresh = 0.1
buttonRefresh = 0.1

button_queue = Queue.Queue()

#init cpu buffer
for n in range(0, buffSize):
  cpuBuff.append(0.0)

lcd = Adafruit_CharLCDPlate()

lcd.clear()
lcd.message("Initialising.....")

col = (lcd.RED , lcd.YELLOW, lcd.GREEN, lcd.TEAL,
       lcd.BLUE, lcd.VIOLET, lcd.ON)
for c in col:
    lcd.backlight(c)
    time.sleep(.1)

btn = ((lcd.LEFT  , 'cmdLeft', 'left'),
       (lcd.UP    , 'cmdUp', 'prev'),
       (lcd.DOWN  , 'cmdDown', 'next'),
       (lcd.RIGHT , 'cmdRight', 'right'),
       (lcd.SELECT, 'cmdSelect', 'select'))


def resource_monitor():
  global lcdMsg
  runFunc = 1
  mem = 0.0
  while runFunc:
    cpuVal = float(sum(cpuBuff)/len(cpuBuff))
    cpuS = "{:5.1f}".format(cpuVal)
    memS = "{:5.1f}".format(mem)
    lcdMsg = "CPU: %s%%\nMEM: %s%%" % (cpuS, memS)
  
    for poll in range(0, buffSize):
      cpu = psutil.cpu_percent()
      mem = psutil.virtual_memory()[2]
      cpuBuff.pop(0)
      cpuBuff.append(cpu)

    button = getButton()
    if (button == 4):       #select button
      return
  time.sleep(waitTime)
  #endWhile
#endDef

def network_monitor():
  global lcdMsg
  runFunc = 1
  while runFunc:
    lcdMsg = 'Network_Monitor'
    button = getButton()
    if (button == 4):
      return
  time.sleep(waitTime)
  #endWhile  
#endDef

def LTC_miner():
  global lcdMsg
  runFunc = 1
  while runFunc:
    lcdMsg = 'LTC_miner'
    button = getButton()
    if (button == 4):
      return
  time.sleep(waitTime)
  #endWhile  
#endDef

def BOINC():
  global lcdMsg
  runFunc = 1
  while runFunc:
    lcdMsg = 'BOINC'
    button = getButton()
    if (button == 4):
      return
  time.sleep(waitTime)
  #endWhile  
#endDef

def camera():
  global lcdMsg
  runFunc = 1
  while runFunc:
    lcdMsg = 'Camera'
    button = getButton()
    if (button == 4):
      return
  time.sleep(waitTime)
  #endWhile  
#endDef

def lcd_colour():
  global lcdMsg
  runFunc = 1
  colIndex = 0
  while runFunc:
    lcdMsg = 'Select Colour\n Up/Down'
    button = getButton()
    if (button == 4):
      return
    elif (button == 1):   #up
      colIndex = (colIndex - 1) % len(col)
      lcd.backlight(colIndex)
    elif (button == 2):   #down
      colIndex = (colIndex + 1) % len(col)
      lcd.backlight(colIndex)
    time.sleep(waitTime)
  #endWhile  
#endDef

def show_menu():
  global lcdMsg
  menuPos = 0
  while True:
    lcdMsg = "Menu:\n %s" % menuList[menuPos]['title']
    button = getButton()
    if (button != 'NONE'):
      btn_loop = btn[button][2]         #execute menu command in btn array
      if ((btn_loop == 'prev') | (btn_loop == 'next')):
        menuPos = menuList[menuPos][btn_loop]
      elif (btn_loop == 'select'):
        return menuList[menuPos]['function']
    time.sleep(waitTime)
    #endWhile
#endDef

def getButton():
  try:
    pressed = button_queue.get(False)
  except:
    pressed = 'NONE'
  return pressed
#endDef

def controlThread():
  while threads_run:
    command = show_menu()
    command()
  return
#endDef

def btnThread():
  while threads_run:
    ind = 0
    for b in btn:
      if lcd.buttonPressed(b[0]):
        button_queue.put(ind)
        time.sleep(0.3)
      ind+=1
    time.sleep(buttonRefresh)
  return
#endDef

def dispThread():
  global lcdMsg
  prevMsg = lcdMsg
  while threads_run:
    if (lcdMsg != prevMsg):
      lcd.clear()
      lcd.message(lcdMsg)
      prevMsg = lcdMsg
    time.sleep(dispRefresh)
  return
#endDef

menuList = [{'title': '0: Resource Monitor', 'function': resource_monitor, 'next': 1, 'prev': 5},
            {'title': '1: Networking', 'function': network_monitor, 'next': 2, 'prev': 0},
            {'title': '2: LTC Miner', 'function': LTC_miner, 'next': 3, 'prev': 1},
            {'title': '3: BOINC', 'function': BOINC, 'next': 4, 'prev': 2},
            {'title': '4: Camera', 'function': camera, 'next': 5, 'prev': 3},
            {'title': '5: LCD Colour', 'function': lcd_colour, 'next': 0, 'prev': 4}
            ]


dspThr = threading.Thread(target=dispThread)
dspThr.setName("DisplayThread")
dspThr.start()
print "Display Thread started..."

btnThr = threading.Thread(target=btnThread)
btnThr.setName("ButtonThread")
btnThr.start()
print "Button Thread started..."

ctrlThr = threading.Thread(target=controlThread)
ctrlThr.setName("ControlThread")
ctrlThr.start()
print "Control Thread started..."

while True:
  time.sleep(1000)
