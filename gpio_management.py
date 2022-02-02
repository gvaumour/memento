import time
import RPi.GPIO as GPIO
import config


# Configure the 3 I2C MCP23017: input with pull up resistors enabled
# Correspondance bouton -> pictos

# Adresses of I2C components: 0, 1 and 2
def gpio_init():
	GPIO.setmode(GPIO.BCM)

	GPIO.setup(4, GPIO.IN, pull_up_down=GPIO.PUD_UP)


# Return the list of currently pressed buttons
def check_buttons():
	config.NB_BUTTONS
    
	# Read all button states 
    # data = bus.read_i2c_block_data(0x48, 0) 
