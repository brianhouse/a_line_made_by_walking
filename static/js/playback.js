var absolute_time = null;
var start_time = null;
var stop_time = null;
var audio_start_time = null;

var sequence = null;
var accel_data = [];
var geo_data = [];
var ref_id = null;

var geo_interval = null;
var sequence_interval = null;

function getGeoLocation () {
    console.log("getGeoLocation");
    // doing this explicitly instead of with leaflet because it appears to be more accurate
    navigator.geolocation.getCurrentPosition(receiveGeoLocation);
}

function receiveGeoLocation (location) {
    console.log("receiveGeoLocation");
    if (start_time != null) {
        geo_data.push([timestamp() - start_time, location.coords.latitude, location.coords.longitude]);
    }
} 

function timestamp () {
    if (absolute_time == null) {
        absolute_time = new Date().getTime() - Math.floor(context.currentTime * 1000);
    }
    return Math.floor(context.currentTime * 1000) + absolute_time;  // have an absolute time, but keep the clock the same as the audio
    // return new Date().getTime();
}

function startWalk () {
    console.log("startWalk");
    getGeoLocation();    
    geo_interval = setInterval(getGeoLocation, 10000);    
    startAudio();
    startAccelerometer();
}

function startRecording () {
    console.log("startRecording");
    setTimeout(stopWalk, 5 * 60 * 1000); // timeout at 5 mins    
    start_time = timestamp();
    audio_start_time = context.currentTime;
    playSound('go', audio_start_time, 1.0, 0.0);    
    queueAudio();
    sequence_interval = setInterval(queueAudio, 9000); // overlap a little so we dont have gaps    
}

function startAudio () {
    console.log("startAudio");
    playSound('countdown', context.currentTime, 1.0, 0.0, startRecording);
}

function queueAudio () {
    // console.log("queueAudio " + sequence.length);
    // schedule notes from the queue that are happening in the next 10s or so
    do {
        if (sequence.length == 0) {
            clearInterval(sequence_interval);
            return;
        }
        var note = sequence.shift()
        var time = audio_start_time + (note[0] / 1000.0);
        var name = note[1];              
        playSound(name, time, 2.0, name == 'left' ? -1.0 : 1.0);
    } while ((time - context.currentTime) < 10);    
}

function startAccelerometer () {
    console.log("startAccelerometer");
    $('#readings').show();    
    window.ondevicemotion = function(e) {
        var a = [e.accelerationIncludingGravity.x, e.accelerationIncludingGravity.y, e.accelerationIncludingGravity.z];
        $('#display_x').html("x: " + a[0]);
        $('#display_y').html("y: " + a[1]);
        $('#display_z').html("z: " + a[2]);
        if (start_time == null) return;        
        var d = [timestamp() - start_time, a[0], a[1], a[2]];                
        accel_data.push(d);
    }
}

function stopWalk () {
    console.log("stopWalk");
    playSound('go', context.currentTime, 1.0, 0.0);        
    $('#start_btn').hide();
    $('#readings').hide();    
    stop_time = timestamp();
    window.ondevicemotion = function(event) { };            
    master_gain_node.gain.value = 0.0;
    getGeoLocation();
    sendWalk();
    start_time = null;
    stop_time = null;
    audio_start_time = null;
}

function sendWalk () {
    console.log("sendWalk");
    var duration = stop_time - start_time;
    if (start_time == null) {
        duration == null;
    }
    var walk_data = {'accel_data': accel_data, 'geo_data': geo_data, 'start_time': start_time, 'duration': duration, 'ref_id': ref_id};
    walk_data = JSON.stringify(walk_data);   
    // alert(walk_data.length);
    walk_data = btoa(RawDeflate.deflate(walk_data));
    // alert(walk_data.length);           
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
    initAudio();
    loadSound('left', "/static/snd/left.wav");
    loadSound('right', "/static/snd/right.wav");                
    loadSound('go', "/static/snd/go.wav");                
    loadSound('countdown', "/static/snd/countdown.wav");
    $('#start_btn').click(function () {
        $('#title').html("Walking...");
        $('#text').html("<br /><br /><br /><br /><br /><br /><br /><br /><br /><br />");
        $('#pocket').html("(phone in pocket)");
        $('#start_btn').html("STOP");
        $('#start_btn').unbind("click");
        $('#start_btn').click(function () {
            stopWalk();
        });
        startWalk();        
    });
});

