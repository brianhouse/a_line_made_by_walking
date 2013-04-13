// mapbox
var mapbox_username = "brianhouse";
var mapbox_map_id = "124z30te";

// sequence data
var walk_index = null;
var num_walks = 0;
var walk_data = null;
var sequence = null;

// map
var map = null;
var current_location_marker;
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
        center: new L.LatLng(41.8205209, -72.400848), // need this before we can panto elsewhere
        attributionControl: false,
        doubleClickZoom: false,
        scrollWheelZoom: false,
        boxZoom: false,
        touchZoom: false,
        dragging: false,
        keyboard: false,
        zoom: 17,
        minZoom: 10,                    
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
        geo_data.push([location.coords.longitude, location.coords.latitude, timestamp()]);
    }
    var latlng = new L.LatLng(location.coords.latitude, location.coords.longitude);
    console.log("--> " + latlng);
    map.panTo(latlng);
    if (current_location_marker == null) {
        current_location_marker = L.circleMarker(latlng, {radius: 10, color: "#009dff", stroke: false, fillOpacity: 1.0, clickable: false}).addTo(map);
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
    pan_node.panningModel = webkitAudioPannerNode.equalpower;    
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

// function checkSelection () {
//     console.log("checkSelection");
//     walk_index = $('#walk_select option:selected').val();
//     num_walks = $('#walk_select option').length;
//     if (num_walks <= 1 || walk_index.length) {
//         $('#start_btn').show();
//         loadWalk();
//     } else {
//         $('#start_btn').hide();
//     }
// }

// function loadWalk () {
//     console.log("loadWalk " + walk_index);
//     // $.ajax({
//     //     type: 'GET',
//     //     url: 'sequence.py',
//     //     data: {'index': walk_index},
//     //     dataType: 'json',
//     //     success: function (data, textStatus, jqXHR) {
//     //         walk_data = data;
//     //         var start_location = data['geo_data'][0].slice(0, 2);
//     //         var stop_location = data['geo_data'][data['geo_data'].length - 1].slice(0, 2);
//     //         markers = [];
//     //         markers.push({  geometry: {coordinates: start_location}, 
//     //                         properties: {'marker-color': '#000', 'marker-symbol': 'circle', 'marker-size': 'large'}
//     //                     });                    
//     //         markers.push({  geometry: {coordinates: stop_location}, 
//     //                         properties: {'marker-color': '#000', 'marker-symbol': 'embassy', 'marker-size': 'large'}
//     //                     });    
//     //         for (var i=0; i<data['geo_data'].length - 2; i++) {
//     //             markers.push({  geometry: {coordinates: data['geo_data'][i].slice(0, 2)},
//     //                             properties: {'marker-color': '#9cf', 'marker-size': 'small', 'image': "http://upload.wikimedia.org/wikipedia/commons/2/2a/Dot.png"}
//     //                         });                        
//     //         }                
//     //         marker_layer.features(markers);
//     //         // .factory(function(f) {
//     //         //     if (f.properties.image) {
//     //         //         var img = document.createElement('img');
//     //         //         img.className = 'marker-image';
//     //         //         img.setAttribute('src', f.properties.image);
//     //         //         return img;
//     //         //     }
//     //         // });
//     //         map.zoom(17).center({ lon: start_location[0], lat: start_location[1] });                                        
//     //     },
//     //     error: function (jqXHR, textStatus, errorThrown) {
//     //         console.log(jqXHR);                    
//     //         alert("Sequence request failed:\n" + errorThrown);
//     //         window.location.reload();
//     //     }
//     // }); 
// }        

// function startWalk () {
//     console.log("startWalk");
//     $('#walk_select').hide();
//     $('#start_btn').hide();            
//     playSound('left', 0, 0.0, 0.0); // iOS needs this
//     playSound('right', 0, 0.0, 0.0); // iOS needs this
//     startAudio();
// }

// function startAudio () {
//     console.log("startAudio");
//     $('#stop_btn').show();
//     sequence = walk_data['steps'];
//     audio_start_time = context.currentTime;
//     for (var i=0; i<4; i++) {
//         if (i % 2 == 0) {
//             playSound('left', audio_start_time + i, 1.0, 0.0);
//         } else {
//             playSound('right', audio_start_time + i, 1.0, 1.0);
//         }
//     }
//     audio_start_time += 4;  // now starting from after countoff
//     setTimeout(startRecording, 4000 - 500); // half second for the accelerometer to get going (step starting is corrected for in process.py)
//     queueAudio();
//     sequence_interval = setInterval(queueAudio, 9000); // overlap a little so we dont have gaps
// }

// function queueAudio () {
//     console.log("queueAudio " + sequence.length);
//     // schedule notes from the queue that are happening in the next 10s or so
//     do {
//         if (sequence.length == 0) {
//             clearInterval(sequence_interval);
//             return;
//         }
//         var note = sequence.shift()
//         var time = audio_start_time + (note[0] / 1000.0);
//         var name = note[1];                        
//         playSound(name, time, 1.0, name == 'left' ? 0.0 : 1.0);
//     } while ((time - context.currentTime) < 10);    
// }

// function startRecording () {
//     console.log("startRecording");
//     $('#readings').show();
//     getGeoLocation();
//     geo_interval = setInterval(getGeoLocation, 10000);            
//     start_time = timestamp();
//     window.ondevicemotion = function(event) {
//         var d = [timestamp(), event.accelerationIncludingGravity.x, event.accelerationIncludingGravity.y, event.accelerationIncludingGravity.z];                
//         $('#display_x').html(d[1]);
//         $('#display_y').html(d[2]);
//         $('#display_z').html(d[3]);
//         accel_data.push(d);
//     }
// }

// function getGeoLocation () {
//     console.log("getGeoLocation");
//     navigator.geolocation.getCurrentPosition(receiveGeoLocation);
// }

// function receiveGeoLocation (location) {
//     geo_data.push([location.coords.longitude, location.coords.latitude, timestamp()]);
//     map.panTo([location.coords.latitude, location.coords.longitude]);    
// }                                

// function stopWalk () {
//     console.log("stopWalk");
//     stop_time = timestamp();
//     window.ondevicemotion = function(event) { };            
//     master_gain_node.gain.value = 0.0;
//     getGeoLocation();
//     clearInterval(geo_interval);
//     sendLog();
// }

// function sendLog () {
//     console.log("sendLog");
//     $('#stop_btn').hide();
//     $('#readings').hide();
//     var duration = stop_time - start_time;
//     var walk_data = {'accel_data': accel_data, 'geo_data': geo_data, 'start_time': start_time, 'duration': duration};
//     walk_data = JSON.stringify(walk_data);            
//     $.ajax({
//         type: 'POST',
//         url: 'index.py', 
//         data: {'walk_data': walk_data}, 
//         success: function () {
//             alert("Success!");
//             window.location.reload();
//         },
//         error: function (jqXHR, textStatus, errorThrown) {
//             alert("Log failed: " + errorThrown);
//             window.location.reload();
//         }
//     });
// }

$(document).ready(function() {                   

    initMap();

    // $('#start_btn').hide();
    // $('#stop_btn').hide();
    // $('#readings').hide();   

    try {
        context = new webkitAudioContext();
        master_gain_node = context.createGainNode();
        master_gain_node.connect(context.destination);          // connect the master gain to the destination
    } catch(e) {
        alert("Web Audio API is not supported in this browser");
    }            

    loadSound('left', "snd/left.wav");
    loadSound('right', "snd/right.wav");    

});  
