var sequence = null;
var context = null;
var buffers = {};  
var master_gain_node = null;   
var audio_start_time = null;   
var recording = false;
var accel_data = [];
var geo_data = [];
var start_time = null;
var stop_time = null;
var geo_interval = null;
var sequence_interval = null;

function getGeoLocation () {
    console.log("getGeoLocation");
    // doing this explicitly instead of with leaflet because it appears to be more accurate
    navigator.geolocation.getCurrentPosition(receiveGeoLocation)
}

function receiveGeoLocation (location) {
    console.log("receiveGeoLocation");
    if (recording) {
        geo_data.push([timestamp() - start_time, location.coords.latitude, location.coords.longitude]);
    }
} 

function loadSound (name, url) {
    console.log("loadSound " + name);
    var request = new XMLHttpRequest();
    request.open('GET', url, true);
    request.responseType = 'arraybuffer';
    request.onload = function() {
        context.decodeAudioData(request.response, function(buffer) {
            buffers[name] = buffer;
            console.log("Loaded " + name + " (" + url +")");                    
        }, null);
    }
    request.send();
}

function playSound (name, time, volume, pan) {    
    console.log("play " + name + "(" + volume + ") at " + time);
    buffer = buffers[name];
    var source = context.createBufferSource();       // creates a sound source
    source.buffer = buffer;                          // tell the source which sound to play
    var pan_node = context.createPanner();           // create the panning node
    source.connect(pan_node);                        // connect the pan to the source        
    // pan_node.panningModel = webkitAudioPannerNode.EQUALPOWER;    this seems to have been broken; boosting levels to compensate
    volume = volume * 4
    pan_node.setPosition((pan * 20.0) - 10.0, 0, 0); // set panning value (0-1)
    var gain_node = context.createGainNode();        // create a gain node
    pan_node.connect(gain_node);                     // connect the gain to the pan
    gain_node.gain.value = volume;                   // set the volume    
    gain_node.connect(master_gain_node);             // connect to master
    source.noteOn(time);                             // play the source in x seconds
}                

function timestamp () {
    return new Date().getTime()
}

function startWalk () {
    console.log("startWalk");
    playSound('left', 0, 0.0, 0.0); // iOS needs this
    playSound('right', 0, 0.0, 0.0); // iOS needs this
    setTimeout(startRecording, 3820 - 500); // 4s for countoff, 0.5s for the accelerometer to get going
    startAudio();
}

function startAudio () {
    console.log("startAudio");
    audio_start_time = context.currentTime;
    playSound('countdown', audio_start_time, 0.125, 0.5);
    audio_start_time += 3.82;  // now starting from after countoff (file is 3:49)
    queueAudio();
    sequence_interval = setInterval(queueAudio, 9000); // overlap a little so we dont have gaps
}

function queueAudio () {
    console.log("queueAudio " + sequence.length);
    // schedule notes from the queue that are happening in the next 10s or so
    do {
        if (sequence.length == 0) {
            clearInterval(sequence_interval);
            return;
        }
        var note = sequence.shift()
        var time = audio_start_time + (note['t'] / 1000.0);
        var name = note['foot'];                        
        playSound(name, time, 1.0, name == 'left' ? 0.0 : 1.0);
    } while ((time - context.currentTime) < 10);    
}

function startRecording () {
    console.log("startRecording");
    $('#readings').show();    
    start_time = timestamp();
    recording = true;
    getGeoLocation();    
    window.ondevicemotion = function(event) {
        var d = [timestamp() - start_time, event.accelerationIncludingGravity.x, event.accelerationIncludingGravity.y, event.accelerationIncludingGravity.z];                
        $('#display_x').html("x: " + d[1]);
        $('#display_y').html("y: " + d[2]);
        $('#display_z').html("z: " + d[3]);
        accel_data.push(d);
    }
}

function stopWalk () {
    console.log("stopWalk");
    $('#start_btn').hide();
    $('#readings').hide();    
    stop_time = timestamp();
    window.ondevicemotion = function(event) { };            
    master_gain_node.gain.value = 0.0;
    getGeoLocation();
    sendWalk();
    start_time = null;
    stop_time = null;
}

function sendWalk () {
    console.log("sendWalk");
    var duration = stop_time - start_time;
    if (start_time == null) {
        duration == null;
    }
    var walk_data = {'accel_data': accel_data, 'geo_data': geo_data, 'start_time': start_time, 'duration': duration};
    walk_data = JSON.stringify(walk_data);            
    $.ajax({
        type: 'POST',
        url: '/', 
        data: {walk_data: walk_data, _xsrf: _xsrf()}, 
        success: function (result) {
            window.location = "/thanks";
        },
        error: function (result) {
            alert(result.responseText.substr(5));
            window.location = "/";
        }
    });
}

$(document).ready(function () {
    getGeoLocation();
    geo_interval = setInterval(function () {
        getGeoLocation();        
    }, 10000);                            
    try {
        context = new webkitAudioContext();
        master_gain_node = context.createGainNode();
        master_gain_node.connect(context.destination);          // connect the master gain to the destination
    } catch(e) {
        alert("Web Audio API is not supported in this browser");
        window.location = "/";
    }            
    loadSound('left', "/static/snd/left.wav");
    loadSound('right', "/static/snd/right.wav");                
    loadSound('countdown', "/static/snd/countdown.wav");
    $('#start_btn').click(function () {
        $('#title').html("Walking...");
        $('#text').hide();
        $('#pocket').html("(phone in pocket)");
        $('#start_btn').html("STOP");
        $('#start_btn').unbind("click");
        $('#start_btn').click(function () {
            stopWalk();
        });
        startWalk();        
    });
    $('#compass_holder').hide();
    window.ondeviceorientation = function (e) {
        if (e.webkitCompassHeading != undefined) {
            $('#compass_holder').show();
            $('#compass').rotate(-1 * (e.webkitCompassHeading + window.orientation) + 270); // west
        }
    }
    setTimeout(stopWalk, 10 * 60 * 1000); // safety timeout at 10min
});

