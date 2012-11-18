

http://www.ladyada.net/make/logshield/rtc.html
http://www.ladyada.net/make/logshield/sd.html

installed:
https://github.com/adafruit/RTClib

(had to rename to RTClib and put in Documents/Arduino/libraries/)

change the pin in the SD code.

watch that your bauds are set the same in the code, in the monitor, etc.


more current: http://arduino.cc/en/Tutorial/Datalogger


ok, shit is no longer ticking for some reason. that sucks.
but is actually not essential for current purposes. can just take the RTC out of the code and use millis.

replaced the RTC chip, same issue. so maybe it's the crystal?

//

hmm. how fast can this thing record? because we'll need to sample the pins at like 100hz

actually seems to sample ok.


need: header sockets, more wire. battery situation.

http://www.arduino.cc/playground/Learning/9VBatteryAdapter


http://arduino.cc/forum/index.php?topic=98898.0


25hz. is ok. enough to proceed.