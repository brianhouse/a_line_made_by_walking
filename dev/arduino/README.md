data collection shield -- assembly. compatible with my arduino?

so the accelerometers can wire directly into the arduino. need some code for the data collection.

constraining to a route is one thing. could even play back a day's worth.

this is not a minor project.


have to somehow log the precise start time of starting walking, and somehow that maps to the start time of the audio playback.

in theory you could do this with one accelerometer.

in theory you could do this, including playback, with iOS.


what would be more useful to me? getting hip to iOS? or arduino? arduino seems more fun.

does arduino even have a realtime clock? doesnt matter. just need relative time since the first footfall.

//

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

//

ok, so this is kind of working.

- second accelerometer
- map to music
- countdown / sync

then I can actually try it. 

materials needed:
- 9v.
- headers? just solder direct on this accel.

need better soldering iron.


this isnt going to acheive a realized project status. what did I accomplish in 5 hours?
- getting back up to speed with the code
- testing the RTC (to no avail)
- getting headers mounted and assembling everything
- getting a candidate signal processing sequence


it's going to be another session to get another accelerometer together, make an actual mounting, make the sound, etc.

dont have another session.

and then of course, having that data, and graphing it, and making sound, etc, is a lot more.







