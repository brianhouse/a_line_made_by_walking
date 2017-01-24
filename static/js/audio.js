var buffers = {};  
var context = null;
var master_gain_node = null;   


function initAudio() {
    try {
        window.AudioContext = window.AudioContext || window.webkitAudioContext;
        context = new AudioContext();
    } catch(e) {
        alert("Your browser doesn't support Web Audio API");
    }        
    master_gain_node = context.createGain();
    master_gain_node.connect(context.destination);          // connect the master gain to the destination
}

function loadSound(name, url) {
    console.log("loadSound " + name);
    var request = new XMLHttpRequest();
    request.open('GET', url, true);
    request.responseType = 'arraybuffer';
    request.onload = function() {
        context.decodeAudioData(request.response, function(buffer) {
            buffers[name] = buffer;
            console.log("Loaded " + name + " (" + url +") [" + buffer + "]");                    
            playSound(name, context.currentTime, 0.0, 0.0); // helps iOS            
        }, null);
    }
    request.send();
}

function playSound(name, time, volume, pan, end_f=null) {    
    console.log("play " + name + " v(" + volume + ") p(" + pan + ") at " + time);
    buffer = buffers[name];
    var source = context.createBufferSource();       // creates a sound source
    source.buffer = buffer;                          // tell the source which sound to play
    var pan_node = context.createPanner();           // create the panning node
    pan_node.panningModel = "equalpower";
    var x = pan,
        y = 0,
        z = 1 - Math.abs(x);
    pan_node.setPosition(x, y, z);
    source.connect(pan_node);
    var gain_node = context.createGain();            // create a gain node
    pan_node.connect(gain_node);                     // connect the gain to the pan
    gain_node.gain.value = volume;                   // set the volume    
    gain_node.connect(master_gain_node);             // connect to master
    source.start(time);                              // play the source in x seconds
    if (end_f != null) {
        source.onended = end_f;
    }
}               

function duration(name) {
    return buffers[name].duration;
}