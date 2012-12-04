
ok, not bad. so there are still some sp/ml issues that could improve with process. some learning. but can press forward.

each time it runs, it goes into crashdb. which is great.

process then runs, extracts footstep onset information. adds an addendum to the file. throws it out if it isnt good enough. makes a second crashdb file.

should be able to list the walks in crashdb in the user interface.

on selection, there is playback.

not bad.

///

make the activate sound zero volume
have the sounds pan
need to log the GPS coordinates and real start time




///////

conceptual justifications:

- being in someone else's shoes, enforces a rhythm
- data feedback: this happens on a media and society scale, meaning in demonstrating locally
- constrained in public space


for testing, simultaneously record audio for ground truth





///

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




//

for presentation:

make a presentation outline, with talking points

add gps, make sure we have real start time

need several real walks
show the signal processing charts
make some overlayed walk charts

points:
- also doing the video analysis, a bit stalled. almanac needs a larger effort, going to make it a class unit.
- needed to bang something out here

- mention previous attempts, show the arduino, apologize for all the technical work
- relate it to the almanac (is it one aspect?)

- being in someone else's shoes, enforces a rhythm

- data feedback: this happens on a media and society scale, meaning in demonstrating locally
- constrained in public space
- could be distributed as an app


//


panning: view-source:http://chromium.googlecode.com/svn/trunk/samples/audio/shiny-drum-machine.html


dude, incidentally, you can totally make a web synthesizer for a server running a braid sequencer. sick!



//


now:

try with just the y-sensor. need better algorithms. dampened model might be necessary, or we could autocorrelate the whole thing, and then throw out stuff that falls outside of a tolerance?

but that's kind of a bummer in missing taking off running, for instance.

///


ok, so looking at closeup data, we're missing peaks.

decreasing threshold, and now we've got more -- and they sound like doubles. crazy.

switching to valleys, and it's pretty close. but seems fast!

/

actually define the shape grouping, the triple of peak shallowvalley peak deepvalley peak, with the peaks around the deepvalley closer together

need some kind of relative expectation algorithm
alternate between expectation and looking for...

is that what wavelets are?

interesting. so you might chunk the data (problematic, windows, or?) and then run features on them (spectrum, etc), and then do an svm perhaps.

[
so I have my basic signal processing techniques. so it's really dynamically learning patterns within that (SVM) or applying a preset template or recognizer thing (wavelet?) to extract known forms?

- could add high-pass filter (smooth, and then subtract the smoothed signal)
- also fft, etc

would have to be more exact for audio, right?

ugh. I just need a more practical DIY course than what DSP was. no math. just techniques.
]

ok, so...

//

quantization?


for final:
+ stop sounds (used universal mute)
+ map paths (not possible with mapbox, lame)
+ integrate map view
- fix long dataset audio event setup
- some type of total visualization/sonification


eventually:
- countdown sounds different sounds
- leaflet seems the better thing to use
- identity, based on phone


