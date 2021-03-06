import serial
import time
import multiprocessing
import json
import RPi.GPIO as GPIO
import signal
import sys
#import drive

## Change this to match your local settings
#SERIAL_PORT = '/dev/ttyACM0'
#SERIAL_BAUDRATE = 115200

def signal_handler(sig, frame):
    print "Closing Programm ..."
    GPIO.cleanup()
    sys.exit(0)

class SerialProcess(multiprocessing.Process):
 
    def __init__(self, input_queue, output_queue):
        multiprocessing.Process.__init__(self)
        self.input_queue = input_queue
        self.output_queue = output_queue
        self.pan_angle = 7.5
        self.tilt_angle = 7.5
        #self.driver = drive.Driver()
        #self.sp = serial.Serial(SERIAL_PORT, SERIAL_BAUDRATE, timeout=1)
 
    def close(self):
        print "closed"

    def camera_tilt(self,dc):
        self.tilt.ChangeDutyCycle(dc)

    def camera_pan(self,dc):
        self.pan.ChangeDutyCycle(dc)

    def pan_camera(self, state):
        if self.center_pan == True:
            if self.pan_angle > 7.5:
                self.pan_angle -= 0.01
                self.pan.ChangeDutyCycle(self.pan_angle)
            elif self.pan_angle < 7.5:
                self.pan_angle += 0.01
                self.pan.ChangeDutyCycle(self.pan_angle)
            elif self.pan_angle == 7.5:
                self.center_pan = False
                self.pan.ChangeDutyCycle(0)
        elif state == "pan_r":
            if self.pan_angle >= 3:
                self.pan_angle -= 0.01
                self.pan.ChangeDutyCycle(self.pan_angle)
            else:
                self.pan.ChangeDutyCycle(0)

        elif state == "pan_l":
            if self.pan_angle <= 13:
                self.pan_angle += 0.01
                self.pan.ChangeDutyCycle(self.pan_angle)
            else:
                self.pan.ChangeDutyCycle(0)

        elif state == "pan_stop":
            self.pan.ChangeDutyCycle(0)

    def tilt_camera(self, state):
        if self.center_tilt == True:
            if self.tilt_angle > 7.5:
                self.tilt_angle -= 0.01
                self.tilt.ChangeDutyCycle(self.tilt_angle)
            elif self.tilt_angle < 7.5:
                self.tilt_angle += 0.01
                self.tilt.ChangeDutyCycle(self.tilt_angle)
            elif self.tilt_angle == 7.5:
                self.center_tilt = False
                self.tilt.ChangeDutyCycle(0)

        elif state == "tilt_u":
            if self.tilt_angle >= 3:
                self.tilt_angle -= 0.01
                self.tilt.ChangeDutyCycle(self.tilt_angle)
            else:
                self.tilt.ChangeDutyCycle(0)

        elif state == "tilt_d":
            if self.tilt_angle <= 13:
                self.tilt_angle += 0.01
                self.tilt.ChangeDutyCycle(self.tilt_angle)
            else:
                self.tilt.ChangeDutyCycle(0)

        elif state == "tilt_stop":
            self.tilt.ChangeDutyCycle(0)

    def drive(self, state):
        if state == "stop":
            GPIO.output(self.MOTORS['MOTOR_VL_CTRL'], GPIO.HIGH)
            self.motot_vl_pwm.ChangeDutyCycle(100)

            GPIO.output(self.MOTORS['MOTOR_HL_CTRL'], GPIO.HIGH)
            self.motot_hl_pwm.ChangeDutyCycle(100)

            GPIO.output(self.MOTORS['MOTOR_VR_CTRL'], GPIO.HIGH)
            self.motot_vr_pwm.ChangeDutyCycle(100)

            GPIO.output(self.MOTORS['MOTOR_HR_CTRL'], GPIO.HIGH)
            self.motot_hr_pwm.ChangeDutyCycle(100)

        elif state == "drive_f":

            GPIO.output(self.MOTORS['MOTOR_VL_CTRL'], GPIO.HIGH)
            self.motot_vl_pwm.ChangeDutyCycle(self.SPEED['speed_f'])

            GPIO.output(self.MOTORS['MOTOR_HL_CTRL'], GPIO.HIGH)
            self.motot_hl_pwm.ChangeDutyCycle(self.SPEED['speed_f'])

            GPIO.output(self.MOTORS['MOTOR_VR_CTRL'], GPIO.HIGH)
            self.motot_vr_pwm.ChangeDutyCycle(self.SPEED['speed_f'])

            GPIO.output(self.MOTORS['MOTOR_HR_CTRL'], GPIO.HIGH)
            self.motot_hr_pwm.ChangeDutyCycle(self.SPEED['speed_f'])

        elif state == "drive_b":

            GPIO.output(self.MOTORS['MOTOR_VL_CTRL'], GPIO.LOW)
            self.motot_vl_pwm.ChangeDutyCycle(self.SPEED['speed_b'])

            GPIO.output(self.MOTORS['MOTOR_HL_CTRL'], GPIO.LOW)
            self.motot_hl_pwm.ChangeDutyCycle(self.SPEED['speed_b'])

            GPIO.output(self.MOTORS['MOTOR_VR_CTRL'], GPIO.LOW)
            self.motot_vr_pwm.ChangeDutyCycle(self.SPEED['speed_b'])

            GPIO.output(self.MOTORS['MOTOR_HR_CTRL'], GPIO.LOW)
            self.motot_hr_pwm.ChangeDutyCycle(self.SPEED['speed_b'])

        elif state == "turn_r":

            GPIO.output(self.MOTORS['MOTOR_VL_CTRL'], GPIO.LOW)
            self.motot_vl_pwm.ChangeDutyCycle(100)

            GPIO.output(self.MOTORS['MOTOR_HL_CTRL'], GPIO.HIGH)
            self.motot_hl_pwm.ChangeDutyCycle(0)

            GPIO.output(self.MOTORS['MOTOR_VR_CTRL'], GPIO.HIGH)
            self.motot_vr_pwm.ChangeDutyCycle(0)

            GPIO.output(self.MOTORS['MOTOR_HR_CTRL'], GPIO.LOW)
            self.motot_hr_pwm.ChangeDutyCycle(100)

        elif state == "turn_l":

            GPIO.output(self.MOTORS['MOTOR_VL_CTRL'], GPIO.HIGH)
            self.motot_vl_pwm.ChangeDutyCycle(0)

            GPIO.output(self.MOTORS['MOTOR_HL_CTRL'], GPIO.LOW)
            self.motot_hl_pwm.ChangeDutyCycle(100)

            GPIO.output(self.MOTORS['MOTOR_VR_CTRL'], GPIO.LOW)
            self.motot_vr_pwm.ChangeDutyCycle(100)

            GPIO.output(self.MOTORS['MOTOR_HR_CTRL'], GPIO.HIGH)
            self.motot_hr_pwm.ChangeDutyCycle(0)

    def init_Sensors(self):

        GPIO.setup(self.SENSORS['DISTANZSENSOR_B'], GPIO.IN)

        GPIO.setup(self.SENSORS['DISTANZSENSOR_F'], GPIO.IN)

        GPIO.setup(self.SENSORS['DISTANZSENSOR_L'], GPIO.IN)
        #pull_up_down=GPIO.PUD_UP
        GPIO.setup(self.SENSORS['DISTANZSENSOR_R'], GPIO.IN )

    def init_Motors(self):

        GPIO.setup(self.MOTORS['MOTOR_VL_CTRL'], GPIO.OUT)
        GPIO.setup(self.MOTORS['MOTOR_VL_PWM'], GPIO.OUT)
        self.motot_vl_pwm = GPIO.PWM(self.MOTORS['MOTOR_VL_PWM'],50)
        self.motot_vl_pwm.start(100)

        GPIO.setup(self.MOTORS['MOTOR_VR_CTRL'], GPIO.OUT)
        GPIO.setup(self.MOTORS['MOTOR_VR_PWM'], GPIO.OUT)
        self.motot_vr_pwm = GPIO.PWM(self.MOTORS['MOTOR_VR_PWM'],50)
        self.motot_vr_pwm.start(100)

        GPIO.setup(self.MOTORS['MOTOR_HL_CTRL'], GPIO.OUT)
        GPIO.setup(self.MOTORS['MOTOR_HL_PWM'], GPIO.OUT)
        self.motot_hl_pwm = GPIO.PWM(self.MOTORS['MOTOR_HL_PWM'],50)
        self.motot_hl_pwm.start(100)

        GPIO.setup(self.MOTORS['MOTOR_HR_CTRL'], GPIO.OUT)
        GPIO.setup(self.MOTORS['MOTOR_HR_PWM'], GPIO.OUT)
        self.motot_hr_pwm = GPIO.PWM(self.MOTORS['MOTOR_HR_PWM'],50)
        self.motot_hr_pwm.start(100)

    def init_Taster(self):
        GPIO.setup(self.TASTER, GPIO.IN, pull_up_down=GPIO.PUD_UP)

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
            'DISTANZSENSOR_F': 29,
            'DISTANZSENSOR_L': 31,
            'DISTANZSENSOR_R': 33,
            'DISTANZSENSOR_B': 36
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
        #wiringpi.wiringPiSetup()

        GPIO.setmode(GPIO.BOARD)
        #wiringpi.wiringPiSetupGpio()
        #wiringpi.mcp23017Setup(100, 0x20)
        #self.init_LEDs()
        self.init_Sensors()
        #self.init_Trace()
        #self.init_Taster()
        self.init_Motors()
        self.init_Camera()
        self.drive("stop")
 
         
    def run(self):

        self.init()
        signal.signal(signal.SIGINT, signal_handler)
        t_right = t_left = driving = driving_b = pan_l = pan_r = tilt_u = tilt_d = self.center_pan = self.center_tilt = sensor_stop = False
        pan_state = "pan_stop"
        tilt_state = "tilt_stop"


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
        time.sleep(1)

        while True:

            self.pan_camera(pan_state)
            self.tilt_camera(tilt_state)
            time.sleep(0.002)

            if not GPIO.input(self.SENSORS['DISTANZSENSOR_L']) and sensor_stop == False:
                sensor_stop == True
                self.drive("stop")

            if GPIO.input(self.SENSORS['DISTANZSENSOR_L']) and sensor_stop == True:
                sensor_stop = False

            # look for incoming tornado request
            if not self.input_queue.empty():

                #Load Json data
                data = self.input_queue.get()
                json_data = json.loads(data)

                #Turn Right
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

                #Turn Left
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

                #Center Camera
                if json_data['Button2'] == 'true' and self.center_pan == False and self.center_tilt == False:
                    self.output_queue.put("Center Camera")
                    self.center_pan = True
                    self.center_tilt = True

                #Drive forward
                if json_data['Button7'] == 'true' and t_left == False and t_right == False and driving == False and driving_b == False and sensor_stop == False:
                    self.output_queue.put("Driving")
                    driving = True
                    self.drive("drive_f")
                elif json_data['Button7'] == 'false' and driving == True:
                    self.output_queue.put("No longer Driving")
                    driving = False
                    self.drive("stop")

                #Drive backwards
                if json_data['Button6'] == 'true' and driving == False and driving_b == False and t_right == False and t_left == False:
                    self.output_queue.put("Driving backwards")
                    driving_b = True
                    self.drive("drive_b")
                elif json_data['Button6'] == 'false' and driving_b == True:
                    self.output_queue.put("No longer driving backwards")
                    driving_b = False
                    self.drive("stop")

                    #Camera pan
                if json_data['Axis5'] == '1' and pan_l == False:
                    self.output_queue.put("Pan left")
                    pan_l = True
                    pan_r = False
                    pan_state = "pan_l"
                elif json_data['Axis5'] != '1' and pan_l == True:
                    self.output_queue.put("No longer pan left")
                    pan_l = False
                    pan_state = "pan_stop"
                if json_data['Axis5'] == '-1' and pan_r == False:
                    self.output_queue.put("Pan right")
                    pan_l = False
                    pan_r = True
                    pan_state = "pan_r"
                elif json_data['Axis5'] != '-1' and pan_r == True:
                    self.output_queue.put("No longer pan right")
                    pan_r = False
                    pan_state = "pan_stop"

                    #Camera tilt
                if json_data['Axis2'] == '1' and tilt_u == False:
                    self.output_queue.put("Tilt up")
                    tilt_u = True
                    tilt_d = False
                    tilt_state = "tilt_u"
                elif json_data['Axis2'] != '1' and tilt_u == True:
                    self.output_queue.put("No longer tilt up")
                    tilt_u = False
                    tilt_state = "tilt_stop"
                if json_data['Axis2'] == '-1' and tilt_d == False:
                    self.output_queue.put("Tilt down")
                    tilt_u = False
                    tilt_d = True
                    tilt_state = "tilt_d"
                elif json_data['Axis2'] != '-1' and tilt_d == True:
                    self.output_queue.put("No longer tilt down")
                    tilt_d = False
                    tilt_state = "tilt_stop"

            # if self.tilt_time != 0 or self.pan_time != 0:
            #     t = time.time()
            #     if (t - self.tilt_time) >= 0.5:
            #         self.camera_tilt(0)
            #     if (t - self.pan_time) >= 0.5:
            #         self.camera_pan(0)
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
