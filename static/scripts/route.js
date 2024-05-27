var map;
var markers = [];
var totalDistance = 0;
var geocoder;
var distanceService;
var autocomplete;
var polyline;
var spots = {}; 

function initMap() {
    map = new google.maps.Map(document.getElementById('map'), {
        zoom: 14,
        center: { lat: 25.0330, lng: 121.5654 } 
    });
    geocoder = new google.maps.Geocoder();
    distanceService = new google.maps.DistanceMatrixService();
    polyline = new google.maps.Polyline({
        strokeColor: '#FF0000',
        strokeOpacity: 1.0,
        strokeWeight: 3,
        map: map
    });

    
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(function (position) {
            var pos = {
                lat: position.coords.latitude,
                lng: position.coords.longitude
            };
            map.setCenter(pos);
        }, function () {
            handleLocationError(true, map.getCenter());
        });
    } else {
        handleLocationError(false, map.getCenter());
    }
}

function handleLocationError(browserHasGeolocation, pos) {
    window.alert(browserHasGeolocation ?
        'Error: The Geolocation service failed.' :
        'Error: Your browser doesn\'t support geolocation.');
}

function addSpotToMap(spotName) {
    geocoder.geocode({ address: spotName }, function (results, status) {
        if (status === 'OK') {
            var location = results[0].geometry.location;
            addMarker(location);
            spots[spotName] = location; 
        } else {
            alert('Geocode was not successful for the following reason: ' + status);
        }
    });
}

function addMarker(location,spotName) {
    var markerLabel = String.fromCharCode(65 + markers.length); 
    var marker = new google.maps.Marker({
        map: map,
        position: location,
        label: markerLabel,
        title: spotName 
    });
    markers.push(marker);
    updateRoute();
    updateTotalDistance(distanceService);
}

function updateRoute() {
    var path = markers.map(marker => marker.getPosition());
    polyline.setPath(path);
}

function updateTotalDistance(distanceService) {
    if (markers.length < 2) {
        document.getElementById('totalDistance').innerText = 'Total Distance: 0 km';
        return;
    }

    var origins = markers.map(marker => marker.getPosition());
    var destinations = markers.map(marker => marker.getPosition());

    distanceService.getDistanceMatrix({
        origins: origins,
        destinations: destinations,
        travelMode: 'DRIVING',
        unitSystem: google.maps.UnitSystem.METRIC
    }, function (response, status) {
        if (status !== 'OK') {
            alert('Error was: ' + status);
            return;
        }

        var totalDistance = 0;
        var segmentDistances = []; 
        var results = response.rows;
        for (var i = 0; i < results.length - 1; i++) {
            var segmentDistance = results[i].elements[i + 1].distance.value;
            segmentDistances.push(segmentDistance / 1000); 
            totalDistance += segmentDistance;
        }

        
        var totalDistanceText = 'Total Distance: ' + (totalDistance / 1000).toFixed(2) + ' km';
        document.getElementById('totalDistance').innerHTML = totalDistanceText
    });
}

function connectAllSpots() {
    var spotNames = Object.keys(spots);
    for (var i = 0; i < spotNames.length; i++) {
        addMarker(spots[spotNames[i]]);
    }
    updateRoute();
    updateTotalDistance();
}

function addAllSpotsToMap(date) {
    
    markers.forEach(function(marker) {
        marker.setMap(null);
    });
    markers = []; 

    
    polyline.setMap(null);

    
    polyline = new google.maps.Polyline({
        strokeColor: '#FF0000',
        strokeOpacity: 1.0,
        strokeWeight: 4,
        geodesic: true,
        map: map
    });

    document.querySelectorAll('#schedule' + date + ' .spot').forEach(function(spotElement) {
        var spotName = spotElement.dataset.spotName;
        addSpotToMap(spotName); 
    });
}

document.addEventListener('DOMContentLoaded', initMap);

