import time

from neopixel import *

# LED strip configuration:
LED_COUNT      = 1      # Number of LED pixels.
LED_PIN        = 18      # GPIO pin connected to the pixels (18 uses PWM!).
#LED_PIN        = 10      _# GPIO pin connected to the pixels (10 uses SPI /dev/spidev0.0).
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 5       # DMA channel to use for generating signal (try 5)
LED_BRIGHTNESS = 255     # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL    = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53
LED_STRIP      = ws.WS2811_STRIP_GRB   # Strip type and colour ordering

def wheel(pos):
	"""Generate rainbow colors across 0-255 positions."""
	if pos < 85:
		return Color(pos * 3, 255 - pos * 3, 0)
	elif pos < 170:
		pos -= 85
		return Color(255 - pos * 3, 0, pos * 3)
	else:
		pos -= 170
		return Color(0, pos * 3, 255 - pos * 3)

def rainbow(strip, wait_ms=20, iterations=1):
	"""Draw rainbow that fades across all pixels at once."""
	for j in range(256*iterations):
		for i in range(strip.numPixels()):
			strip.setPixelColor(i, wheel((i+j) & 255))
		strip.show()
		time.sleep(wait_ms/1000.0)

def time_in_range(start, end, x):
    """Return true if x is in the range [start, end]"""
    if start <= end:
        return start <= x <= end
    else:
        return start <= x or x <= end

# Main program logic follows:
if __name__ == '__main__':
        #from datetime import datetime
        #from datetime import time
        import datetime
        import time
        import pause
	# Create NeoPixel object with appropriate configuration.
        strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL, LED_STRIP)
	# Intialize the library (must be called once before other functions).
	strip.begin()
        #print datetime.time(datetime.now())
	print ('Press Ctrl-C to quit.')

        wake=datetime.time(6, 45, 0,0)
        leave_room=datetime.time(7, 0, 0,0)
        sleep=datetime.time(20, 00, 0,0)

        for x in range (0,2):
                print "TURN LIGHT YELLOW"
                strip.setPixelColorRGB(0, 200,240, 0)
                strip.show()
                time.sleep(1)
                print "TURN LIGHT GREEN"
                strip.setPixelColorRGB(0, 255, 0,0)
                strip.show()
                time.sleep(1)
                print "TURN LIGHT BLUE"
                strip.setPixelColorRGB(0, 0,0,255)
                strip.show()
                time.sleep(1)
                
        while True:   
                if time_in_range(wake, leave_room, datetime.datetime.now().time()) == True:
                        print "TURN LIGHT YELLOW"
                        strip.setPixelColorRGB(0, 200, 240, 0)
                        strip.show()
                        time.sleep(60)
                if time_in_range(leave_room, sleep, datetime.datetime.now().time()) == True:
                        print "TURN LIGHT GREEN"
                        strip.setPixelColorRGB(0, 255, 0, 0)
                        strip.show()
                        time.sleep(60)
                if time_in_range(sleep, wake, datetime.datetime.now().time()) == True:
                        print "TURN LIGHT BLUE"
                        strip.setPixelColorRGB(0, 0, 0,255)
                        strip.show()
                        time.sleep(60)


