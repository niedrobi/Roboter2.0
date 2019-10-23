import wiringpi
import time

class Driver:
    def __init__(self):
        # Motoren
        self.MOTORS = {
            'MOTOR_VL_PWM': 7,
            'MOTOR_VL_CTRL': 11,
            'MOTOR_VR_PWM': 10,
            'MOTOR_VR_CTRL': 13,
            'MOTOR_HL_PWM': 12,
            'MOTOR_HL_CTRL': 14,
            'MOTOR_HR_PWM': 15,
            'MOTOR_HR_CTRL': 16
        }
        # LED's
        self.LEDs = {
            'LED_REAR': 4,
            'LED_FRONT': 5
        }
        # Sensoren
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
        wiringpi.wiringPiSetup()
        #wiringpi.wiringPiSetupGpio()
        wiringpi.mcp23017Setup(100, 0x20)
        self.init_LEDs()
        self.init_Sensors()
        self.init_Trace()
        self.init_Taster()
        self.init_Motors()
        #self.drive("drive_f")

    def drive(self, state):
        if state == "stop":
	    print "stop"
            wiringpi.digitalWrite(self.MOTORS['MOTOR_VL_CTRL'], 1)
            wiringpi.softPwmWrite(self.MOTORS['MOTOR_VL_PWM'], 100)

            wiringpi.digitalWrite(self.MOTORS['MOTOR_HL_CTRL'], 1)
            wiringpi.softPwmWrite(self.MOTORS['MOTOR_HL_PWM'], 100)

            wiringpi.digitalWrite(self.MOTORS['MOTOR_VR_CTRL'], 1)
            wiringpi.softPwmWrite(self.MOTORS['MOTOR_VR_PWM'], 100)

            wiringpi.digitalWrite(self.MOTORS['MOTOR_HR_CTRL'], 1)
            wiringpi.softPwmWrite(self.MOTORS['MOTOR_HR_PWM'], 100)

        elif state == "drive_f":
            print "i should be driving"
	    print self.MOTORS['MOTOR_VL_CTRL'], self.MOTORS['MOTOR_VL_PWM'], self.SPEED['speed_f']
            wiringpi.digitalWrite(self.MOTORS['MOTOR_VL_CTRL'], 1)
            wiringpi.softPwmWrite(self.MOTORS['MOTOR_VL_PWM'], self.SPEED['speed_f'])

            wiringpi.digitalWrite(self.MOTORS['MOTOR_HL_CTRL'], 1)
            wiringpi.softPwmWrite(self.MOTORS['MOTOR_HL_PWM'], self.SPEED['speed_f'])

            wiringpi.digitalWrite(self.MOTORS['MOTOR_VR_CTRL'], 1)
            wiringpi.softPwmWrite(self.MOTORS['MOTOR_VR_PWM'], self.SPEED['speed_f'])

            wiringpi.digitalWrite(self.MOTORS['MOTOR_HR_CTRL'], 1)
            wiringpi.softPwmWrite(self.MOTORS['MOTOR_HR_PWM'], self.SPEED['speed_f'])

        elif state == "drive_b":
	    print "drive  back"
            wiringpi.digitalWrite(self.MOTORS['MOTOR_VL_CTRL'], 1)
            wiringpi.softPwmWrite(self.MOTORS['MOTOR_VL_PWM'], self.SPEED['speed_b'])

            wiringpi.digitalWrite(self.MOTORS['MOTOR_HL_CTRL'], 1)
            wiringpi.softPwmWrite(self.MOTORS['MOTOR_HL_PWM'], self.SPEED['speed_b'])

            wiringpi.digitalWrite(self.MOTORS['MOTOR_VR_CTRL'], 1)
            wiringpi.softPwmWrite(self.MOTORS['MOTOR_VR_PWM'], self.SPEED['speed_b'])

            wiringpi.digitalWrite(self.MOTORS['MOTOR_HR_CTRL'], 1)
            wiringpi.softPwmWrite(self.MOTORS['MOTOR_HR_PWM'], self.SPEED['speed_b'])

        elif state == "turn_r":
	    print "trun right"
            wiringpi.digitalWrite(self.MOTORS['MOTOR_VL_CTRL'], 0)
            wiringpi.softPwmWrite(self.MOTORS['MOTOR_VL_PWM'], 100)

            wiringpi.digitalWrite(self.MOTORS['MOTOR_HL_CTRL'], 1)
            wiringpi.softPwmWrite(self.MOTORS['MOTOR_HL_PWM'], 0)

            wiringpi.digitalWrite(self.MOTORS['MOTOR_VR_CTRL'], 1)
            wiringpi.softPwmWrite(self.MOTORS['MOTOR_VR_PWM'], 0)

            wiringpi.digitalWrite(self.MOTORS['MOTOR_HR_CTRL'], 0)
            wiringpi.softPwmWrite(self.MOTORS['MOTOR_HR_PWM'], 100)

        elif state == "turn_l":
	    print "turn left"
            wiringpi.digitalWrite(self.MOTORS['MOTOR_VL_CTRL'], 1)
            wiringpi.softPwmWrite(self.MOTORS['MOTOR_VL_PWM'], 0)

            wiringpi.digitalWrite(self.MOTORS['MOTOR_HL_CTRL'], 0)
            wiringpi.softPwmWrite(self.MOTORS['MOTOR_HL_PWM'], 100)

            wiringpi.digitalWrite(self.MOTORS['MOTOR_VR_CTRL'], 0)
            wiringpi.softPwmWrite(self.MOTORS['MOTOR_VR_PWM'], 100)

            wiringpi.digitalWrite(self.MOTORS['MOTOR_HR_CTRL'], 1)
            wiringpi.softPwmWrite(self.MOTORS['MOTOR_HR_PWM'], 0)

    def init_LEDs(self):
        wiringpi.pinMode(self.LEDs['LED_FRONT'], wiringpi.GPIO.OUTPUT)
        wiringpi.pinMode(self.LEDs['LED_REAR'], wiringpi.GPIO.OUTPUT)
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

    def init_Trace(self):
        wiringpi.pinMode(self.TRACE['SPUR_L'], wiringpi.GPIO.INPUT)
        wiringpi.pinMode(self.TRACE['SPUR_R'], wiringpi.GPIO.INPUT)

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
