var mapbox_username = "brianhouse";
var mapbox_map_id = "yse7s0w5";
var map = null;
var current_location_marker = null;
// var walk_data = null;
// var walk_markers = [];
// var walk_paths = [];
// var walk_ids = [];
// var walk_id = null;
var trigger_radius = 30; // ft
// var start_point = new L.LatLng(40.72649,-73.991938); // nyc
var start_point = new L.LatLng(41.820427,-71.401595); // pvd
var walk_path = null;

function initMap () {
    map = new L.map('map', {
        layers: new L.TileLayer("http://a.tiles.mapbox.com/v3/" + mapbox_username + ".map-" + mapbox_map_id + "/{z}/{x}/{y}.png"),
        zoomControl: true,
        center: start_point, // need this before we can panTo elsewhere
        attributionControl: false,
        doubleClickZoom: false,
        scrollWheelZoom: false,
        boxZoom: false,
        touchZoom: true,
        dragging: true,
        keyboard: false,
        zoom: 17,
        minZoom: 13,                    
        maxZoom: 17
    });
    getGeoLocation();
    setInterval(function () {
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
    var latlng = new L.LatLng(location.coords.latitude, location.coords.longitude);
    console.log("--> " + latlng);
    map.panTo(latlng);
    if (current_location_marker == null) {
        current_location_marker = L.circleMarker(latlng, {radius: 10, color: "#fff", stroke: true, fillOpacity: 1.0, clickable: false}).addTo(map);
    } else {
        current_location_marker.setLatLng(latlng);
    } 
    if (walk_path != null) {
        map.removeLayer(walk_path);
    }
    walk_path = new L.Polyline([start_point, latlng], {color: "#fff", weight: 5, opacity: 1.0, smoothFactor: 2}).addTo(map);
    var distance = geoDistance(latlng, start_point);
    if (distance < trigger_radius) {
        map.removeLayer(walk_path);
        current_location_marker.setStyle({color: "#00f"});
        walk_marker.setStyle({color: "#00f"});
        window.location = "/walk";
    }
    // $.each(walk_markers, function(index, walk_marker) {
    //     var distance = geoDistance(latlng, walk_marker.getLatLng());
    //     if (distance < trigger_radius) {
    //         console.log("hit");
    //         walk_marker.setStyle({fillColor: "#fff"});
    //         walk_paths[index].setStyle({color: "#fff"});
    //         walk_id = walk_ids[index];
    //         // conflicts here are a problem
    //     } else {
    //         console.log("no hit " + distance);
    //         walk_marker.setStyle({fillColor: walk_marker.color});
    //         walk_paths[index].setStyle({color: walk_marker.color});            
    //     }
    // });               
}

function makeStart () {
    console.log("makeStart");
    var walk_marker = L.circleMarker(start_point, {radius: 15, color: "#0f0", stroke: true, fillOpacity: 0.75, clickable: false}).addTo(map);
}

// function loadWalks () {
//     console.log("loadWalks");
//     $.each(walk_data, function(w, walk) {
//         if (walk['geo_data'] == undefined) return;    
//         var points = [];
//         for (p in walk['geo_data']) {
//             points.push(new L.LatLng(walk['geo_data'][p]['lat'], walk['geo_data'][p]['lng']));
//         }
//         var color = '#' + Math.floor(Math.random() * 16777215).toString(16);
//         var walk_marker = L.circleMarker(points[0], {radius: 30, color: color, stroke: true, fillOpacity: 0.75, clickable: false}).addTo(map);
//         var walk_path = new L.Polyline(points, {color: color, weight: 5, opacity: 0.75, smoothFactor: 2}).addTo(map);
//         walk_markers.push(walk_marker);
//         walk_paths.push(walk_path);
//         walk_ids.push(walk['id']);
//     });
// }

$(document).ready(function() {                   
    initMap();
    makeStart();
});  



//// utilities ////

/* calculate the distance between two physical points in ft */
function geoDistance (latlng1, latlng2) {
    var R = 6371; // km
    var d_lat = (latlng2.lat - latlng1.lat).toRad();
    var d_lng = (latlng2.lng - latlng1.lng).toRad();
    lat1 = latlng1.lat.toRad();
    lat2 = latlng2.lat.toRad();
    var a = Math.sin(d_lat/2) * Math.sin(d_lat/2) + 
            Math.sin(d_lng/2) * Math.sin(d_lng/2) * Math.cos(lat1) * Math.cos(lat2); 
    var c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1-a)); 
    return (R * c) * 3280.84; // convert to ft
}

if (typeof(Number.prototype.toRad) === "undefined") {
    Number.prototype.toRad = function() {
        return this * Math.PI / 180;
    }
}
