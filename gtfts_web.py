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

def time_in_range(start, end, x):
    """Return true if x is in the range [start, end]"""
    if start <= end:
        return start <= x <= end
    else:
        return start <= x or x <= end


# Main program logic follows:
if __name__ == '__main__':

    import ConfigParser
    from datetime import datetime

    now = datetime.now()
    config = ConfigParser.ConfigParser()
    config.read('/home/pi/Projects/GTFTS/schedule.ini')

    # Create NeoPixel object with appropriate configuration.
    strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL, LED_STRIP)
    # Intialize the library (must be called once before other functions).
    strip.begin()


    for sections in config.sections():
        print sections
#        print "length " + str(len(config.sections()))
#        print 'index ' + str(config.sections().index(sections))
        cur_idx = config.sections().index(sections)
        period1 = config.get(sections, 'time')

        print 'period 1 ' + period1
        if cur_idx == len(config.sections())-1:
            period2 = config.get(config.sections()[0], 'time')
        else:
            period2 = config.get(config.sections()[cur_idx+1], 'time')
        print 'period 2 ' + period2
        time_1 = now.replace(hour=datetime.strptime(period1,'%I:%M%p').time().hour, minute=datetime.strptime(period1,'%I:%M%p').time().minute, second=0, microsecond=0)
        time_2 = now.replace(hour=datetime.strptime(period2,'%I:%M%p').time().hour, minute=datetime.strptime(period2,'%I:%M%p').time().minute, second=0, microsecond=0)
        if time_in_range(time_1, time_2, now)== True:
            strip.setPixelColorRGB(0, 200, 240, 0)
            color = tuple(map(int,config.get(sections, 'color').split(',')))
            brightness = config.get(sections, 'brightness')
            print period1 + " : " + period2
            print brightness, color
            strip.setPixelColorRGB(0, *color)
            strip.setBrightness(int((float(brightness)/100)*255))
            print float(brightness), int((float(brightness)/100)*255)
            strip.show()

 
