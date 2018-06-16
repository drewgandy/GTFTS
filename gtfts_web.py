# this requires the following dependencies:
# * Adafruit Neopxiels
# * pause
# to install:
#sudo apt-get install build-essential python-dev git scons swig
#git clone https://github.com/jgarff/rpi_ws281x.git
#cd rpi_ws281x
#scons
#cd python
#wget https://pypi.python.org/packages/source/s/setuptools/setuptools-5.7.zip
#sudo python setup.py install
#sudo pip install pause
#sudo nano /etc/rc.local
###add "sudo python /home/pi/code/GTFTS/gtfts_web.py &" to end, just before "exit 0"
#sudo reboot

from neopixel import *
import logging

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

#def time_in_range(start, end, x):
#    """Return true if x is in the range [start, end]"""
#    if start <= end:
#        return start <= x <= end
#    else:
#        return start <= x or x <= end

def time_in_range(startTime, endTime, nowTime):
    if startTime < endTime:
        return nowTime >= startTime and nowTime <= endTime
    else: #Over midnight
        return nowTime >= startTime or nowTime <= endTime

# Main program logic follows:
if __name__ == '__main__':

    import ConfigParser
    from datetime import datetime
    import time
    
    logging.basicConfig(filename='gtfts_web.log',level=logging.INFO)
    config = ConfigParser.ConfigParser()
    config.read('/home/pi/code/GTFTS/schedule.ini')

    # Create NeoPixel object with appropriate configuration.
    strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL, LED_STRIP)
    # Intialize the library (must be called once before other functions).
    strip.begin()
    print 'loaded and starting loop'
    logging.info('loaded, cycling colors and starting loop at: %s', datetime.now())
    
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
        now = datetime.now()
        logging.debug('current time: %s', now)
        for sections in config.sections():
            cur_idx = config.sections().index(sections)
            period1 = config.get(sections, 'time')

            if cur_idx == len(config.sections())-1:
                period2 = config.get(config.sections()[0], 'time')
            else:
                period2 = config.get(config.sections()[cur_idx+1], 'time')
            logging.debug( period1 + " : " + period2)
            time_1 = now.replace(hour=datetime.strptime(period1,'%I:%M%p').time().hour, minute=datetime.strptime(period1,'%I:%M%p').time().minute, second=0, microsecond=0)
            time_2 = now.replace(hour=datetime.strptime(period2,'%I:%M%p').time().hour, minute=datetime.strptime(period2,'%I:%M%p').time().minute, second=0, microsecond=0)
            if time_in_range(time_1, time_2, now)== True:
                #strip.setPixelColorRGB(0, 200, 240, 0)
                color = tuple(map(int,config.get(sections, 'color').split(',')))
                brightness = config.get(sections, 'brightness')
                logging.debug('brightness: %s   |   color: %s', brightness, color)
                strip.setPixelColorRGB(0, *color)
                strip.setBrightness(int((float(brightness)/100)*255))
                logging.debug('brightness: %s   |   color: %s', float(brightness), int((float(brightness)/100)*255))
                strip.show()
        logging.debug("done with for loop")
        time.sleep(60)

