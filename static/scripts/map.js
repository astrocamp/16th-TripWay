let map;
let trafficLayer;
let transitLayer;
let bicycleLayer;
let currentPosition;
let directionsRenderer;
let infowindow;
const markers = [];

document.addEventListener("DOMContentLoaded", function() {
    let spinner = document.getElementById("loading-spinner");
    let content = document.getElementById("map");

    initMap();

    google.maps.event.addListenerOnce(map, 'tilesloaded', function() {
        spinner.style.display = "none";
        content.style.display = "block";
    });

    let input = document.getElementById('pac-input');
    let autocomplete = new google.maps.places.Autocomplete(input);
    autocomplete.bindTo('bounds', map);

    autocomplete.addListener('place_changed', function() {
        let place = autocomplete.getPlace();
        if (!place.geometry) {
            console.log("No details available for input: '" + place.name + "'");
            return;
        }

        if (place.geometry.viewport) {
            map.fitBounds(place.geometry.viewport);
        } else {
            map.setCenter(place.geometry.location);
            map.setZoom(16);
        }

        createMarker(place);
    });
});

function initMap() {
    map = new google.maps.Map(document.getElementById("map"), {
        zoom: 15,
        center: { lat: 25.0383401, lng: 121.5060706 }
    });

    directionsRenderer = new google.maps.DirectionsRenderer();
    directionsRenderer.setMap(map);

    infowindow = new google.maps.InfoWindow();

    navigator.geolocation.getCurrentPosition(function(position) {
        currentPosition = {
            lat: position.coords.latitude,
            lng: position.coords.longitude,
        };

        map.setCenter(currentPosition);

        const marker = new google.maps.Marker({
            position: currentPosition,
            map: map,
            title: 'Your Location'
        });
    }, function() {
        alert("Error: The Geolocation service failed.");
    });
    trafficLayer = new google.maps.TrafficLayer();
    transitLayer = new google.maps.TransitLayer();
    bicycleLayer = new google.maps.BicyclingLayer();
    
}
function toggleLayer(layerName) {
    const layers = {
        'trafficLayer': trafficLayer,
        'transitLayer': transitLayer,
        'bicycleLayer': bicycleLayer
    };

    for (let key in layers) {
        if (layers[key].getMap()) {
            layers[key].setMap(null);
        }
    }

    if (layerName && layers[layerName]) {
        layers[layerName].setMap(map);
    }
}

function showCurrentPosition() {
    navigator.geolocation.getCurrentPosition(function(position) {
        currentPosition = {
            lat: position.coords.latitude,
            lng: position.coords.longitude,
        };

        const marker = new google.maps.Marker({
            position: currentPosition,
            map: map,
            title: 'Your Location'
        });

        map.setCenter(currentPosition);
    }, function() {
        alert("Error: The Geolocation service failed.");
    });
}

function searchNearby(type) {
    showCurrentPosition();
    
    if (!currentPosition) {
        return;
    }

    const request = {
        location: currentPosition,
        radius: 2000,
        type: [type]
    };

    const service = new google.maps.places.PlacesService(map);
    service.nearbySearch(request, nearbyCallback);
}

function nearbyCallback(results, status) {
    if (status === google.maps.places.PlacesServiceStatus.OK) {
        clearMarkers();
        
        for (let i = 0; i < results.length; i++) {
            createMarker(results[i]);
            map.setZoom(15);
        }
    } else {
        alert("搜索附近失敗，原因：" + status);
    }
}

function createMarker(place) {
    const marker = new google.maps.Marker({
        map: map,
        position: place.geometry.location
    });

    google.maps.event.addListener(marker, "click", function() {
        showPlaceDetails(place, marker);
    });

    markers.push(marker);
}

function showPlaceDetails(place, marker) {
    const service = new google.maps.places.PlacesService(map);
    service.getDetails({ placeId: place.place_id }, (details, status) => {
        if (status === google.maps.places.PlacesServiceStatus.OK) {
            const contentString = `
                <div class="info-window rounded-5xl card bg-base-100x p-2 flex items-center flex-col overflow-scroll">
                    <div class=" flex card-actions justify-between w-full">
                        <p class="text-lg sm:text-xl font-bold overflow-scroll">${details.name}</p> 
                        <div>
                            <i class="hidden fa-solid fa-star" style="color: #FFD43B;"></i>
                            <div class="badge badge-outline">${place.rating}</div> 
                        </div>
                    </div>
                    <div class="flex w-full justify-center">
                        <img src="${details.photos ? details.photos[0].getUrl({ maxWidth: 200, maxHeight: 200 }) : ''}" alt="${details.name}">
                    </div>
                    <div class="w-full justify-center overflow-scroll break-words">
                        <p class="text-sm sm:text-lg font-medium">${details.formatted_address}</p>
                        <p class=" text-sm sm:text-sm font-medium">${details.formatted_phone_number || 'N/A'}</p>
                        <p class="text-sm sm:text-sm font-medium">${details.opening_hours ? details.opening_hours.weekday_text.join('<br>') : 'N/A'}</p>
                    </div>
                </div>
            `;
            infowindow.setContent(contentString);
            infowindow.open(map, marker);
            map.setCenter(marker.getPosition());
        }
    });
}

function clearMarkers() {
    for (let i = 0; i < markers.length; i++) {
        markers[i].setMap(null);
    }
    markers.length = 0;
}

