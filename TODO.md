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

Web Audio API + iPhone:
- cant queue too many note events
- HRTF spatialization is too much for the processer if we're also recording accel data


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

/

so the peak detection works, and you can see the two levels. the lesser peaks must be lefts.
take all the peaks, and cluster them into two clusters? k-means?

/

from kyle:

http://en.wikipedia.org/wiki/Dynamic_time_warping

it does matching like this:

http://www.atasoyweb.net/resimgoster.php?resim=DinamikZamanBukmeAlgoritmasi.png


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


### concept

make an equal-timed map. something like this has to exist.

the idea is just a map that is distorted so that two points are the distance apart they would take to traverse.

of course, that's totally dependent on mode of transportation, and stride.

so it can also be past-tense. 

this might work better with openpaths data.

/

could straight layer the walks and build sound with partials

could have a melody that then turns into a kind of cannon

could link the footsteps with space, and then move through space instead of time
(what would that do? compensate if people we're going different speeds)

use speed (from GPS) 

what do we have, really?

a collection of onsets, on different voices, grouped together by what number step it is

what kind of variation are we expecting? not a ton, if it's just me on a walk

the canon, with a different line for each walk is probably best, most doable

kind of a deconstruction

could use a historical piece, even, and have it performed...

4 part choral harmony?

/

variations:

- coupling. two people are stuck together in realtime, listening to footfalls and having to conform.
- group. pick a specific location, and everyone listens to the same pattern. either that pattern is defined by an individual, or is the average of all previous goers.
- group. everyone goes along a particular route. and then that's averaged, and then I walk that.

bridge reference.

richard long reference.

/

in terms of personal documentation, it's the route I take between two significant places, and how the journey between those places is inscribed / takes on meaning over time.

/

presentation:

coupling, group 1, group2, location sig
show graph, show music, show app

record some more trips on the way tomorrow


### indexes

1354851814868
1354851377010
1354852238877
1354852692081


### refs

http://en.wikipedia.org/wiki/Hamish_Fulton

Long, A Line Made by Walking (1967)


### future issues

crashdb is not going to be scaleable



