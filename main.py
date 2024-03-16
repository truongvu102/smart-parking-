import RPi.GPIO as GPIO
import time
import easygui

GPIO.setmode(GPIO.BOARD)
GPIO.setup(8,GPIO.IN)
GPIO.setup(10,GPIO.IN)
GPIO.setup(16,GPIO.IN) 
GPIO.setup(12,GPIO.OUT)
GPIO.setup(18,GPIO.OUT)
pwm=GPIO.PWM(12, 50)
pwm.start(0)

num_parking_spots = 4

def SetAngle(angle):
    duty = angle / 18 + 2
    GPIO.output(12, True)
    pwm.ChangeDutyCycle(duty)
    time.sleep(1)
    GPIO.output(12, False)
    pwm.ChangeDutyCycle(0)



while True:
    if GPIO.input(8) == 0:
        SetAngle(90)
            #time.sleep(2)
        if GPIO.input(10) == 0:
                SetAngle(0)
                num_parking_spots -= 1
                print("Cho trong con lai: " + str(num_parking_spots))
            
        else:
                print("Bãi đỗ xe đã hết chỗ trống.")
                easygui.msgbox("hết chỗ trống ", title="canh bao")
            
        time.sleep(3)
    elif GPIO.input(10) == 0:
        if num_parking_spots < 4:
            num_parking_spots += 1
            print("Cho trong con lai: " + str(num_parking_spots))
            SetAngle(90)
            time.sleep(1)
            SetAngle(0)
        else:
            print("Trong bãi không còn xe.")
        time.sleep(1)
    elif GPIO.input(16)==0:
            GPIO.output(18,True)
            time.sleep(0.1)
            SetAngle(90)
            easygui.msgbox("co chay", title="canh bao")
            SetAngle(0)
    elif GPIO.input(16)==1:    
            GPIO.output(18,False)
            time.sleep(0.1)
            



