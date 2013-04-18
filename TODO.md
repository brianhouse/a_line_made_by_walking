### todo

- check: readings dont reappear
- set domain (needs to propagate)

### bugs


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

webapp / homescreen mode doesnt support get gps coords, for some reason

when the iphone sleeps, timeout events are no longer fired, so have to keep the phone on.

is that the case with leaflet?


### ml notes

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


### refs

[http://en.wikipedia.org/wiki/Hamish_Fulton](http://en.wikipedia.org/wiki/Hamish_Fulton)

Long, A Line Made by Walking (1967)

