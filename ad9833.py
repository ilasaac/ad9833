import spidev
import time
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)

GPIO.setup(22, GPIO.OUT)
GPIO.output(22, GPIO.HIGH)

# Create an instance of the SpiDev class
spi = spidev.SpiDev()

# Open bus 0, device (chip select) 0
# The RPi has two CS pins for bus 0: CE0 and CE1
spi.open(0, 0)

# Set SPI speed and mode
# Max speed depends on your device (e.g., 1MHz = 1000000)
spi.max_speed_hz = 100000
spi.mode = 0b00  # Mode 0: CPOL=0, CPHA=0

def send_data(input):
    tx_msb=input>>8
    tx_lsb=input & 0xFF
    spi.xfer([tx_msb,tx_lsb])
    print(input)

def read_data():
    try:
        while True:
            # Data to send (list of bytes)
            # Example: Sending [0x01, 0x80, 0x00] often used for ADC chips
            GPIO.output(22, GPIO.LOW)
            time.sleep(.0001)
            send_data(0x2100) # Send a reset

            send_data(0x50c7) # Select the MSB Register
            send_data(0x4000) # Write MSB = 0x0001 to FREQ0

            send_data(0xc000) # Select the LSB Register
            send_data(0x2000)  # Write LSB = 0x20F0 to FREQ0
            time.sleep(.0001)
            GPIO.output(22, GPIO.HIGH)
           # send_data(0x0008) # Sine
            
            time.sleep(1)
            break
    except KeyboardInterrupt:
        print("\nStopping...")
    finally:
        # Always close the connection when finished
        spi.close()

if __name__ == "__main__":
    read_data()
