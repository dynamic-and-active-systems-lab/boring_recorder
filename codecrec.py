#import sounddevice as sd
#from scipy.io.wavfile import write
#import wavio as wv
#from sense_hat import SenseHat
import os
import time
from datetime import datetime
from gpiozero import LED
from gpiozero import Button
import sys

#sense = SenseHat()
#GPIO Pin Numers (BCM not Board Pins nums) 
relayChannel1 = 26 #Board pin 37, BCM pin 26
relayChannel2 = 20 #Board pin 38, BCM pin 20
relayChannel3 = 21 #Board pin 40, BCM pin 21
codecLEDGreen = 23
codecLEDRed   = 24
codecSwitch   = 27

haltFlag = False

greenLED = LED(codecLEDGreen)
redLED   = LED(codecLEDRed)
relayCh1 = LED(relayChannel1)
relayCh1.on() #Energize to turn off voltage to signal conditioner
codecButton = Button(codecSwitch)

primaryPath = "/home/dasl/repos/boring_recorder/"

# 
def makewavefile(fs = 48000, duration=5, channels = 1, filename="test.wav"):
    relayCh1.off() #Denergize to turn on voltage to signal conditioner
    time.sleep(3) #give voltage in signal condition time to settle
    print('Recording')
    redLED.on()
    recordString = "arecord -D 'plughw:CARD=IQaudIOCODEC,DEV=0' -t wav -c "+str(int(channels))+" -f dat -d " + str(duration) + " " + filename
    os.system(recordString)
    print(recordString)
    relayCh1.on() #Denergize to turn on voltage to signal conditioner
    redLED.off()
    print('Done.')

def playwavefile(filename="test.wav"):
    print(filename)
    os.system("aplay -f dat "+ filename)

def setupRecordingFolder(path = "/home/dasl/Desktop/Recordings"):
    try:
        dirContents = os.listdir(path)
    except:
        os.mkdir(path)

def setnextwakeup(timeSeconds = 10):
    timeSecondsStr = str(int(timeSeconds))
    os.system("echo 0 | sudo tee /sys/class/rtc/rtc0/wakealarm") #Disable the alarm before writing a new one to avoid the resource busy error
    alarmSetString = "echo +" + timeSecondsStr + " | sudo tee /sys/class/rtc/rtc0/wakealarm"
    #print("Setting alarm set for " + timeSecondsStr + " seconds from now.")
    #sense.show_message("Alarm = " + timeSecondsStr + "s")
    os.system(alarmSetString)
    #os.system("sudo halt")
    
def shutdownsystem():
    print("Preparing to shut system down...")
    #sense.show_message("Shutting down.")
    os.system("sudo halt")

def setHaltFlag():
    global haltFlag
    print("Setting Halt Flag!")
    haltFlag = True

def setdeviceparameters(fileNum=1):
    setupPath = "Pi-Codec/"
    setupFilename1 = "Codec_Zero_AUXIN_record_and_HP_playback.state"
    setupFilename2 = "Codec_Zero_OnboardMIC_record_and_SPK_playback.state"
    setupFilename3 = "Codec_Zero_Playback_only.state"
    setupFilename4 = "Codec_Zero_StereoMIC_record_and_HP_playback.state"
    if fileNum==1:
        setupFilename = setupFilename1
    elif fileNum==2:
        setupFilename = setupFilename2
    elif fileNum==3:
        setupFilename = setupFilename3
    elif fileNum==4:
        setupFilename = setupFilename4
    cwdir=os.getcwd()
    print(cwdir)
    os.system("sudo alsactl restore -f "+primaryPath+setupPath+setupFilename)
    #os.system("amixer")
    #os.system("amixer sset Master unmute")#use Master when running for debugging. Use PCM when executing as shell script
    #os.system("amixer sset Master 50%")

# setdeviceparameters(4)
# makewavefile(44100, 5, 1, "test2.wav")
# setdeviceparameters(2)
# playwavefile("test2.wav")

print(haltFlag)
codecButton.when_pressed = setHaltFlag

if __name__=="__main__":
    recordingDir = "/home/dasl/Desktop/Recordings"
    recordingDuration = sys.argv[1]
    if len(sys.argv)>2:
        recordingInterval = sys.argv[2]
    else:
        recordingInterval = 0
    
    print(sys.argv[0])
    print("Duration="+str(recordingDuration))
    print("Interval="+str(recordingInterval))

    setupRecordingFolder(recordingDir)
    #print("Program initialized. Sleeping for 10 s to enable joystick execution termination.")
    #time.sleep(2)
    print(haltFlag)
    if haltFlag:
        print("Exiting Program - Halt Flag Set")
        exit(1)
    nowTimeStamp = datetime.now()
    nowTimeStampStr = nowTimeStamp.strftime("%Y-%m-%d_%H_%M_%S")
    fileName = nowTimeStampStr+".wav"
    # redLED.on()
    # time.sleep(5)
    # redLED.off()
    fullPathName = recordingDir+"/"+fileName
    setdeviceparameters(4)
    makewavefile(48000, recordingDuration, 1, fullPathName)
    #setdeviceparameters(2)
    #playwavefile(fullPathName)
    time.sleep(5)
    if haltFlag or recordingInterval == 0:
        print("Exiting Program - Halt Flag Set")
        exit(1)
    else:
        setnextwakeup(recordingInterval)
        shutdownsystem()