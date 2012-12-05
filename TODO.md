### implementation notes

        // function loadSound () {
        //     console.log("Loading sound...");
        //     $.ajax({
        //         type: 'GET',
        //         url: 'snd.wav', 
        //         dataType: 'arraybuffer',    // not implemented in jquery!
        //         success: function (data, textStatus, jqXHR) {
        //             console.log("Success: " + textStatus);
        //             context.decodeAudioData(data, null);
        //         },
        //         error: function (jqXHR, textStatus, errorThrown) {
        //             console.log("Failed: " + textStatus);
        //         }
        //     });
        // }

### bugs

when the iphone sleeps, timeout events are no longer fired, so have to keep the phone on

webapp / homescreen mode doesnt support get gps coords, for some reason


### ml notes

ok, so looking at closeup data, we're missing peaks.

decreasing threshold, and now we've got more -- and they sound like doubles. crazy.

switching to valleys, and it's pretty close.

/

actually define the shape grouping, the triple of peak shallowvalley peak deepvalley peak, with the peaks around the deepvalley closer together

need some kind of relative expectation algorithm
alternate between expectation and looking for...



### todo

quantization?


for final:
+ stop sounds (used universal mute)
+ map paths (not possible with mapbox, lame)
+ integrate map view
+ fix long dataset audio event setup
+ have the sounds pan
- some type of total visualization/sonification


eventually:
- countdown sounds different sounds
- leaflet seems the better thing to use
- identity, based on phone


## PROBLEMS

everything works fine first time. 

with audio playback, it's not working.

try without pan.



### concept

make an equal-timed map. something like this has to exist.

the idea is just a map that is distorted so that two points are the distance apart they would take to traverse.

of course, that's totally dependent on mode of transportation, and stride.

so it can also be past-tense. 

this might work better with openpaths data.




