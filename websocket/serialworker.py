import serial
import time
import multiprocessing
import json
import RPi.GPIO as GPIO
#import drive
import wiringpi

## Change this to match your local settings
#SERIAL_PORT = '/dev/ttyACM0'
#SERIAL_BAUDRATE = 115200

class SerialProcess(multiprocessing.Process):
 
    def __init__(self, input_queue, output_queue):
        multiprocessing.Process.__init__(self)
        self.input_queue = input_queue
        self.output_queue = output_queue
        self.pan_time = 0
        self.tilt_time = 0
        #self.driver = drive.Driver()
        #self.sp = serial.Serial(SERIAL_PORT, SERIAL_BAUDRATE, timeout=1)
        
 
    def close(self):
        print "closed"

    def camera_tilt(self,dc):
        self.tilt.ChangeDutyCycle(dc)
        self.tilt_time = time.time()

    def camera_pan(self,dc):
        self.pan.ChangeDutyCycle(dc)
        self.pan_time = time.time()

    def drive(self, state):
        if state == "stop":
            #wiringpi.digitalWrite(self.MOTORS['MOTOR_VL_CTRL'], self.HIGH)
            #vl = GPIO.PWM(self.MOTORS['MOTOR_VL_PWM'], 100)
            #vl.start(1)
            #hier nur noch dc nder und ganzes PWM fr jeden Motor in init
            #wiringpi.softPwmWrite(self.MOTORS['MOTOR_VL_PWM'], 100)

            wiringpi.digitalWrite(self.MOTORS['MOTOR_HL_CTRL'], self.HIGH)
            wiringpi.softPwmWrite(self.MOTORS['MOTOR_HL_PWM'], 100)

            wiringpi.digitalWrite(self.MOTORS['MOTOR_VR_CTRL'], self.HIGH)
            wiringpi.softPwmWrite(self.MOTORS['MOTOR_VR_PWM'], 100)

            wiringpi.digitalWrite(self.MOTORS['MOTOR_HR_CTRL'], self.HIGH)
            wiringpi.softPwmWrite(self.MOTORS['MOTOR_HR_PWM'], 100)

        elif state == "drive_f":
            wiringpi.digitalWrite(self.MOTORS['MOTOR_VL_CTRL'], self.HIGH)
            wiringpi.softPwmWrite(self.MOTORS['MOTOR_VL_PWM'], self.SPEED['speed_f'])

            wiringpi.digitalWrite(self.MOTORS['MOTOR_HL_CTRL'], self.HIGH)
            wiringpi.softPwmWrite(self.MOTORS['MOTOR_HL_PWM'], self.SPEED['speed_f'])

            wiringpi.digitalWrite(self.MOTORS['MOTOR_VR_CTRL'], self.HIGH)
            wiringpi.softPwmWrite(self.MOTORS['MOTOR_VR_PWM'], self.SPEED['speed_f'])

            wiringpi.digitalWrite(self.MOTORS['MOTOR_HR_CTRL'], self.HIGH)
            wiringpi.softPwmWrite(self.MOTORS['MOTOR_HR_PWM'], self.SPEED['speed_f'])

        elif state == "drive_b":
            wiringpi.digitalWrite(self.MOTORS['MOTOR_VL_CTRL'], self.LOW)
            wiringpi.softPwmWrite(self.MOTORS['MOTOR_VL_PWM'], self.SPEED['speed_b'])

            wiringpi.digitalWrite(self.MOTORS['MOTOR_HL_CTRL'], self.LOW)
            wiringpi.softPwmWrite(self.MOTORS['MOTOR_HL_PWM'], self.SPEED['speed_b'])

            wiringpi.digitalWrite(self.MOTORS['MOTOR_VR_CTRL'], self.LOW)
            wiringpi.softPwmWrite(self.MOTORS['MOTOR_VR_PWM'], self.SPEED['speed_b'])

            wiringpi.digitalWrite(self.MOTORS['MOTOR_HR_CTRL'], self.LOW)
            wiringpi.softPwmWrite(self.MOTORS['MOTOR_HR_PWM'], self.SPEED['speed_b'])

        elif state == "turn_r":
            wiringpi.digitalWrite(self.MOTORS['MOTOR_VL_CTRL'], self.LOW)
            wiringpi.softPwmWrite(self.MOTORS['MOTOR_VL_PWM'], 100)

            wiringpi.digitalWrite(self.MOTORS['MOTOR_HL_CTRL'], self.HIGH)
            wiringpi.softPwmWrite(self.MOTORS['MOTOR_HL_PWM'], 0)

            wiringpi.digitalWrite(self.MOTORS['MOTOR_VR_CTRL'], self.HIGH)
            wiringpi.softPwmWrite(self.MOTORS['MOTOR_VR_PWM'], 0)

            wiringpi.digitalWrite(self.MOTORS['MOTOR_HR_CTRL'], self.LOW)
            wiringpi.softPwmWrite(self.MOTORS['MOTOR_HR_PWM'], 100)

        elif state == "turn_l":
            wiringpi.digitalWrite(self.MOTORS['MOTOR_VL_CTRL'], self.HIGH)
            wiringpi.softPwmWrite(self.MOTORS['MOTOR_VL_PWM'], 0)

            wiringpi.digitalWrite(self.MOTORS['MOTOR_HL_CTRL'], self.LOW)
            wiringpi.softPwmWrite(self.MOTORS['MOTOR_HL_PWM'], 100)

            wiringpi.digitalWrite(self.MOTORS['MOTOR_VR_CTRL'], self.LOW)
            wiringpi.softPwmWrite(self.MOTORS['MOTOR_VR_PWM'], 100)

            wiringpi.digitalWrite(self.MOTORS['MOTOR_HR_CTRL'], self.HIGH)
            wiringpi.softPwmWrite(self.MOTORS['MOTOR_HR_PWM'], 0)

    #def init_LEDs(self):
        #wiringpi.pinMode(self.LEDs['LED_FRONT'], wiringpi.GPIO.OUTPUT)
        #wiringpi.pinMode(self.LEDs['LED_REAR'], wiringpi.GPIO.OUTPUT)
        #pinMode(LED_FRONT, self.OUTPUT)
        #pinMode(LED_REAR, self.OUTPUT)

    def init_Sensors(self):
        wiringpi.pinMode(self.SENSORS['DISTANZSENSOR_B'], wiringpi.GPIO.INPUT)

        wiringpi.pinMode(self.SENSORS['DISTANZSENSOR_F'], wiringpi.GPIO.INPUT)
        wiringpi.pullUpDnControl(self.SENSORS['DISTANZSENSOR_F'], wiringpi.GPIO.PUD_UP)

        wiringpi.pinMode(self.SENSORS['DISTANZSENSOR_L'], wiringpi.GPIO.INPUT)
        wiringpi.pullUpDnControl(self.SENSORS['DISTANZSENSOR_L'], wiringpi.GPIO.PUD_UP)

        wiringpi.pinMode(self.SENSORS['DISTANZSENSOR_R'], wiringpi.GPIO.INPUT)
        wiringpi.pullUpDnControl(self.SENSORS['DISTANZSENSOR_R'], wiringpi.GPIO.PUD_UP)

    #def init_Trace(self):
        #wiringpi.pinMode(self.TRACE['SPUR_L'], wiringpi.GPIO.INPUT)
        #wiringpi.pinMode(self.TRACE['SPUR_R'], wiringpi.GPIO.INPUT)
        #sssgflskljdg
    def init_Motors(self):
        wiringpi.pinMode(self.MOTORS['MOTOR_VL_CTRL'], wiringpi.GPIO.OUTPUT)
        wiringpi.pinMode(self.MOTORS['MOTOR_VL_PWM'], wiringpi.GPIO.PWM_OUTPUT)
        wiringpi.softPwmCreate(self.MOTORS['MOTOR_VL_PWM'], 0, 100)

        wiringpi.pinMode(self.MOTORS['MOTOR_VR_CTRL'], wiringpi.GPIO.OUTPUT)
        wiringpi.pinMode(self.MOTORS['MOTOR_VR_PWM'], wiringpi.GPIO.PWM_OUTPUT)
        wiringpi.softPwmCreate(self.MOTORS['MOTOR_VR_PWM'], 0, 100)

        wiringpi.pinMode(self.MOTORS['MOTOR_HL_CTRL'], wiringpi.GPIO.OUTPUT)
        wiringpi.pinMode(self.MOTORS['MOTOR_HL_PWM'], wiringpi.GPIO.PWM_OUTPUT)
        wiringpi.softPwmCreate(self.MOTORS['MOTOR_HL_PWM'], 0, 100)

        wiringpi.pinMode(self.MOTORS['MOTOR_HR_CTRL'], wiringpi.GPIO.OUTPUT)
        wiringpi.pinMode(self.MOTORS['MOTOR_HR_PWM'], wiringpi.GPIO.PWM_OUTPUT)
        wiringpi.softPwmCreate(self.MOTORS['MOTOR_HR_PWM'], 0, 100)

    def init_Taster(self):
        wiringpi.pinMode(self.TASTER, wiringpi.GPIO.INPUT)
        wiringpi.pullUpDnControl(self.TASTER, wiringpi.GPIO.PUD_UP)

    def init_Camera(self):       
        tiltPin = 13
        panPin = 12
        GPIO.setup(tiltPin, GPIO.OUT)
        GPIO.setup(panPin, GPIO.OUT)
        self.tilt = GPIO.PWM(tiltPin,50)
        self.pan = GPIO.PWM(panPin,50)
        self.tilt.start(0)
        self.pan.start(0)

    def init(self):
        #self.sp.flushInput()
	    # GPIO-Pin-configuration for motors
        self.MOTORS = {
            'MOTOR_VL_PWM': 23, #PWM-signal front-left
            'MOTOR_VL_CTRL': 21, #Controll-signal front-left
            'MOTOR_VR_PWM': 15, #
            'MOTOR_VR_CTRL': 19,
            'MOTOR_HL_PWM': 11,
            'MOTOR_HL_CTRL': 7,
            'MOTOR_HR_PWM': 3,
            'MOTOR_HR_CTRL': 5
        }
        # Not in use
        # LED's
        #self.LEDs = {
        #    'LED_REAR': 4,
        #    'LED_FRONT': 5
        #}
        # GPIO-Pin-configuration for sensors
        self.SENSORS = {
            'DISTANZSENSOR_F': 101,
            'DISTANZSENSOR_L': 102,
            'DISTANZSENSOR_R': 103,
            'DISTANZSENSOR_B': 0
        }
        # trace
        self.TRACE = {
            'SPUR_L': 1,
            'SPUR_R': 3
        }
        # speed
        self.SPEED = {
            'speed_f': 0,
            'speed_b': 40
        }
        self.TASTER = 104
        self.OUTPUT = 1
        self.INPUT = 0
        self.PWM_OUTPUT = 1
        self.PUD_UP = 2
        self.HIGH = 1
        self.LOW = 0
        wiringpi.wiringPiSetup()

        GPIO.setmode(GPIO.BOARD)
        wiringpi.wiringPiSetupGpio()
        wiringpi.mcp23017Setup(100, 0x20)
        #self.init_LEDs()
        self.init_Sensors()
        #self.init_Trace()
        self.init_Taster()
        self.init_Motors()
        self.init_Camera()
        self.drive("stop")
 
         
    def run(self):

        self.init()
        t_right = t_left = driving = driving_b = False
        #while 1: #make camera movement more smooth
            #for i in range(30,120,1):
                #a = i/10
                #self.camera_pan(a)
                #self.camera_tilt(a)
                #time.sleep(0.01)
            #for i in range(120,30,-1):
                #a = i/10
                #self.camera_pan(a)
                #self.camera_tilt(a)
                #time.sleep(0.01)
        self.camera_pan(7.5)
        self.camera_tilt(7.5)
    	
        while True:
            # look for incoming tornado request
            if not self.input_queue.empty():
                data = self.input_queue.get()
                json_data = json.loads(data)
                if json_data['Axis0'] == '1' and t_right == False:
                    self.output_queue.put("Turning Right")
                    t_right = True
                    driving = False
                    driving_b = False
                    self.drive("stop")
                    self.drive("turn_r")
                elif json_data['Axis0'] != '1' and t_right == True:
                    self.output_queue.put("No longer turning Right")
                    t_right = False
                    self.drive("stop")
                if json_data['Axis0'] == '-1' and t_left == False:
                    self.output_queue.put("Turning Left")
                    t_left = True
                    driving = False
                    driving_b = False
                    self.drive("stop")
                    self.drive("turn_l")
                elif json_data['Axis0'] != '-1' and t_left == True:
                    self.output_queue.put("No longer turning Left")
                    t_left = False
                    self.drive("stop")
                if json_data['Button7'] == 'true' and t_left == False and t_right == False and driving == False and driving_b == False:
                    self.output_queue.put("Driving")
                    driving = True
                    self.drive("drive_f")
                elif json_data['Button7'] == 'false' and driving == True:
                    self.output_queue.put("No longer Driving")
                    driving = False
                    self.drive("stop")
                #if driving == True and (t_left == True or t_right == True):
                    #self.output_queue.put("No longer Driving")
                    #driving = False
                    #self.drive("stop")
                if json_data['Button6'] == 'true' and driving == False and driving_b == False and t_right == False and t_left == False:
                    self.output_queue.put("Driving backwards")
                    driving_b = True
                    self.drive("drive_b")
                elif json_data['Button6'] == 'false' and driving_b == True:
                    self.output_queue.put("No longer driving backwards")
                    driving_b = False
                    self.drive("stop")
                #if #Camera:
                    #todo
            if self.tilt_time != 0 or self.pan_time != 0:
                t = time.time()
                if (t - self.tilt_time) >= 0.5:
                    self.camera_tilt(0)
                if (t - self.pan_time) >= 0.5:
                    self.camera_pan(0)
                # send it to the serial device
                #self.writeSerial(data)
                #print "Done"

		#self.output_queue.put(data)
 
            # look for incoming serial data
            #if (self.sp.inWaiting() > 0):
            	#data = self.readSerial()
                #print "reading from serial: " + data
                # send it back to tornado
            	#self.output_queue.put(data)
