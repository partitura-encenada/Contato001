#Musica: Estrondo
#Mão direita

import serial
import time
import rtmidi
import sys


contato = 'COM15'
if len(sys.argv) > 1:
    contato = 'COM' + sys.argv[1]

serialPort = serial.Serial(port = contato, baudrate=115200, bytesize=8, timeout=2, stopbits=serial.STOPBITS_ONE, rtscts=True)
serialString = ''

midiout = rtmidi.MidiOut()
print(midiout.get_ports())
port = midiout.open_port(5)

#Variaveis do sensor
gyro = 0
accel = 0
touch = 0

#Variaveis 
note = ('a',0)
last_note = 0
notes = [51,53,56,59]
notes_delay = [0] * len(notes)
lastDebounceTime = 0.1  
noteHold = 0.005
soundEffectDuration = 2
previousSoundEffect = 3
soundeEffectInterval = 2
previousSoundEffectActiv = 0.1


def assignTimes(note):
    
    for i in range(len(notes)):
        if(note == notes[i]):
            notes_delay[i] == time.time()

while(1):

    if(serialPort.in_waiting > 0):

        serialString = serialPort.readline()

        sensorData = (serialString.decode('utf-8')).split('/')

        #print(serialString) 
        id = float(sensorData[0])
        gyro = float(sensorData[1])
        accel = float(sensorData[2])
        touch = float(sensorData[3])
        print(int(id), 'gyro:', gyro, 'acc:', accel, 't:', int(touch))
    
    if(-90 <= gyro <= -45):
        note = ('G4',notes[3])
    elif(-44 <= gyro <= 0):
        note = ('A4',notes[2])
    elif(1 <= gyro <= 45):
        note = ('B4',notes[1])
    elif(46 <= gyro <= 90):
        note = ('D5',notes[0])


    can = (note == last_note) and (time.time() - lastDebounceTime > 0.1)
    
    if(touch == 1):
        lastDebounceTime = time.time()
        if(note != last_note):
            assignTimes(note[1])
            last_note = note
            midiout.send_message([0x90,note[1],30])
            print("MIDI ON" + str(time.time()))
        else:
            if(can == True):
                last_note = note
                assignTimes(note[1])
                midiout.send_message([0x90,note[1],30])
                print("MIDI ON"+ str(time.time()))
    
    for i in range(len(notes)):
        if((time.time() - notes_delay[i] > noteHold)):
           #print(f"Off + " + str(note))
            if(notes[i] != note[1]):
                midiout.send_message([0x80,notes[i],30])
                pass
            elif(touch !=1):
                midiout.send_message([0x80,note[1],30])
                pass
