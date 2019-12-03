# Load configuration file
import configparser


config = configparser.ConfigParser()
config.read('rover/pin_configuration.ini')

RIGHT_IN1 = int(config['MOTOR']['RIGHT_IN1'])
RIGHT_IN2 = int(config['MOTOR']['RIGHT_IN2'])
LEFT_IN3 = int(config['MOTOR']['LEFT_IN3'])
LEFT_IN4 = int(config['MOTOR']['LEFT_IN4'])
RIGHT_PWM_ENA = int(config['MOTOR']['RIGHT_PWM_ENA'])
RIGHT_PWM_ENB = int(config['MOTOR']['RIGHT_PWM_ENB'])
COMP_SPEED_R = int(config['MOTOR']['COMP_SPEED_R'])
COMP_SPEED_L = int(config['MOTOR']['COMP_SPEED_L'])
print(RIGHT_IN1)
