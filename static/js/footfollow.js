// mapbox
var mapbox_username = "brianhouse";
var mapbox_map_id = "yse7s0w5";

// data for loaded walk
var walk_id = null;
var walk_data = null;
var sequence = null;

// map
var map = null;
var current_location_marker = null;
var marker_layer = null;        

// audio
var context = null;
var buffers = {};  
var master_gain_node = null;   
var audio_start_time = null;   

// data collection
var recording = false;
var accel_data = [];
var geo_data = [];
var start_time = null;
var stop_time = null;

// polling
var geo_interval = null;
var sequence_interval = null;

/* create the map */
function initMap () {
    map = new L.map('map', {
        layers: new L.TileLayer("http://a.tiles.mapbox.com/v3/" + mapbox_username + ".map-" + mapbox_map_id + "/{z}/{x}/{y}.png"),
        zoomControl: true,
        center: new L.LatLng(41.8205, -71.40083), // need this before we can panTo elsewhere
        attributionControl: false,
        doubleClickZoom: false,
        scrollWheelZoom: false,
        boxZoom: false,
        touchZoom: false,
        dragging: false,
        keyboard: false,
        zoom: 17,
        minZoom: 13,                    
        maxZoom: 17
    });
    getGeoLocation();
    geo_interval = setInterval(function () {
        getGeoLocation();        
    }, 10000);                
}

function getGeoLocation () {
    console.log("getGeoLocation");
    // doing this explicitly instead of with leaflet because it appears to be more accurate
    navigator.geolocation.getCurrentPosition(receiveGeoLocation)
}

function receiveGeoLocation (location) {
    console.log("receiveGeoLocation");
    if (recording) {
        geo_data.push([timestamp() - start_time, location.coords.longitude, location.coords.latitude]);
    }
    var latlng = new L.LatLng(location.coords.latitude, location.coords.longitude);
    console.log("--> " + latlng);
    map.panTo(latlng);
    if (current_location_marker == null) {
        current_location_marker = L.circleMarker(latlng, {radius: 10, color: "#fff", stroke: false, fillOpacity: 1.0, clickable: false}).addTo(map);
    } else {
        current_location_marker.setLatLng(latlng);
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
    console.log("play " + name + " at " + time);
    buffer = buffers[name];
    var source = context.createBufferSource();       // creates a sound source
    source.buffer = buffer;                          // tell the source which sound to play
    var pan_node = context.createPanner();           // create the panning node
    source.connect(pan_node);                        // connect the pan to the source        
    pan_node.panningModel = webkitAudioPannerNode.EQUALPOWER;    
    pan_node.setPosition((pan * 20.0) - 10.0, 0, 0); // set panning value (0-1)
    var gain_node = context.createGainNode();        // create a gain node
    pan_node.connect(gain_node);                     // connect the gain to the pan
    // source.connect(gain_node);                       // connect the gain to the source    
    gain_node.gain.value = volume;                   // set the volume    
    gain_node.connect(master_gain_node);             // connect to master
    source.noteOn(time);                             // play the source in x seconds
}                

function timestamp () {
    return new Date().getTime()
}

function checkSelection () {
    console.log("checkSelection");
    walk_id = $('#walk_select option:selected').val();
    num_walks = $('#walk_select option').length;
    if (num_walks <= 1 || walk_id.length) {
        $('#start_btn').show();
        if (walk_id.length) {
            loadWalk();
        } else {
            $('#walk_select').hide();
        }
    } else {
        $('#start_btn').hide();
    }
}

function loadWalk () {
    console.log("loadWalk " + walk_id);
    $.ajax({
        type: 'GET',
        url: '/sequence/' + walk_id,
        dataType: 'json',
        success: function (data, textStatus, jqXHR) {
            walk_data = data;
            var start_location = data['geo_data'][0].slice(0, 2);
            var stop_location = data['geo_data'][data['geo_data'].length - 1].slice(0, 2);
            markers = [];
            markers.push({  geometry: {coordinates: start_location}, 
                            properties: {'marker-color': '#000', 'marker-symbol': 'circle', 'marker-size': 'large'}
                        });                    
            markers.push({  geometry: {coordinates: stop_location}, 
                            properties: {'marker-color': '#000', 'marker-symbol': 'embassy', 'marker-size': 'large'}
                        });    
            for (var i=0; i<data['geo_data'].length - 2; i++) {
                markers.push({  geometry: {coordinates: data['geo_data'][i].slice(0, 2)},
                                properties: {'marker-color': '#9cf', 'marker-size': 'small', 'image': "http://upload.wikimedia.org/wikipedia/commons/2/2a/Dot.png"}
                            });                        
            }                
            marker_layer.features(markers);
            // .factory(function(f) {
            //     if (f.properties.image) {
            //         var img = document.createElement('img');
            //         img.className = 'marker-image';
            //         img.setAttribute('src', f.properties.image);
            //         return img;
            //     }
            // });
            map.zoom(17).center({ lon: start_location[0], lat: start_location[1] });                                        
        },
        error: function (result) {
            alert(result.responseText.substr(5));
            window.location.reload();
        }
    }); 
}        

function startWalk () {
    console.log("startWalk");
    $('#walk_select').hide();
    $('#start_btn').hide();            
    $('#stop_btn').show();    
    playSound('left', 0, 0.0, 0.0); // iOS needs this
    playSound('right', 0, 0.0, 0.0); // iOS needs this
    setTimeout(startRecording, 4000 - 500); // 4s for countoff, 0.5s for the accelerometer to get going
    startAudio();
}

function startAudio () {
    console.log("startAudio");
    audio_start_time = context.currentTime;
    for (var i=0; i<4; i++) {
        if (i % 2 == 0) {
            playSound('left', audio_start_time + i, 1.0, 0.0);
        } else {
            playSound('right', audio_start_time + i, 1.0, 1.0);
        }
    }
    if (walk_id != null && walk_id.length) {
        audio_start_time += 4;  // now starting from after countoff
        sequence = walk_data['steps'];    
        queueAudio();
        sequence_interval = setInterval(queueAudio, 9000); // overlap a little so we dont have gaps
    }
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
        var time = audio_start_time + (note[0] / 1000.0);
        var name = note[1];                        
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
        $('#display_x').html(d[1]);
        $('#display_y').html(d[2]);
        $('#display_z').html(d[3]);
        accel_data.push(d);
    }
}

function stopWalk () {
    console.log("stopWalk");
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
    $('#stop_btn').hide();
    $('#readings').hide();
    var duration = stop_time - start_time;
    if (start_time == null) {
        duration == null;
    }
    var walk_data = {'accel_data': accel_data, 'geo_data': geo_data, 'start_time': start_time, 'duration': duration};
    walk_data = JSON.stringify(walk_data);            
    $.ajax({
        type: 'POST',
        url: '/', 
        data: {'walk_data': walk_data}, 
        success: function (result) {
            alert("Success!");
            window.location.reload();
        },
        error: function (result) {
            alert(result.responseText.substr(5));
            window.location.reload();
        }
    });
}

$(document).ready(function() {                   

    initMap();

    $('#start_btn').hide();
    $('#stop_btn').hide();
    $('#readings').hide();   

    try {
        context = new webkitAudioContext();
        master_gain_node = context.createGainNode();
        master_gain_node.connect(context.destination);          // connect the master gain to the destination
    } catch(e) {
        alert("Web Audio API is not supported in this browser");
    }            

    loadSound('left', "/static/snd/left.wav");
    loadSound('right', "/static/snd/right.wav");    

    checkSelection();

});  
