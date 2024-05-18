let map;
let currentPosition;
let directionsService;
let directionsRenderer;
let infowindow;
const markers = [];

function initMap() {
    navigator.geolocation.getCurrentPosition(function (position) {
        currentPosition = {
            lat: position.coords.latitude,
            lng: position.coords.longitude,
        };

        map = new google.maps.Map(document.getElementById("map"), {
            center: currentPosition,
            zoom: 16,
        });

        directionsService = new google.maps.DirectionsService();
        directionsRenderer = new google.maps.DirectionsRenderer();
        directionsRenderer.setMap(map);

        infowindow = new google.maps.InfoWindow();

        const input = document.getElementById("pac-input");
        const autocomplete = new google.maps.places.Autocomplete(input, {
            fields: ["place_id", "geometry", "formatted_address", "name"],
        });

        autocomplete.bindTo('bounds', map);

        autocomplete.addListener('place_changed', () => {
            infowindow.close();
            const place = autocomplete.getPlace();
            if (!place.geometry || !place.geometry.location) {
                window.alert("No details available for input: '" + place.name + "'");
                return;
            }

            if (place.geometry.viewport) {
                map.fitBounds(place.geometry.viewport);
            } else {
                map.setCenter(place.geometry.location);
                map.setZoom(17);
            }

            // Create marker and show details immediately
            createMarkerWithDetails(place);
        });

        const circle = new google.maps.Circle({
            center: currentPosition,
            radius: 1000,
        });

        autocomplete.setBounds(circle.getBounds());
        map.controls[google.maps.ControlPosition.TOP_LEFT].push(input);
    }, function () {
        alert("Error: The Geolocation service failed.");
    });
}

function searchNearby(type) {
    if (!currentPosition) {
        alert("請先獲取用戶位置！");
        return;
    }

    map.setCenter(currentPosition); // 重新定位到用户当前位置
    map.setZoom(16);
    const request = {
        location: currentPosition,
        radius: 1000,
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
        }
    } else {
        alert("附近搜索失敗，原因：" + status);
    }
}

function createMarker(place) {
    const marker = new google.maps.Marker({
        map: map,
        position: place.geometry.location
    });

    google.maps.event.addListener(marker, "click", function () {
        showPlaceDetails(place, marker);
    });

    markers.push(marker);
}

function createMarkerWithDetails(place) {
    const marker = new google.maps.Marker({
        map: map,
        position: place.geometry.location
    });

    markers.push(marker);
    showPlaceDetails(place, marker);
}

function showPlaceDetails(place, marker) {
    const service = new google.maps.places.PlacesService(map);
    service.getDetails({ placeId: place.place_id }, (details, status) => {
        if (status === google.maps.places.PlacesServiceStatus.OK) {
            const contentString = `
                <div class="info-window">
                    <h3>${details.name}</h3>
                    <img src="${details.photos ? details.photos[0].getUrl({ maxWidth: 200, maxHeight: 200 }) : ''}" alt="${details.name}">
                    <p><strong>地址:</strong> ${details.formatted_address}</p>
                    <p><strong>電話:</strong> ${details.formatted_phone_number || 'N/A'}</p>
                    <p><strong>營業時間:</strong> ${details.opening_hours ? details.opening_hours.weekday_text.join('<br>') : 'N/A'}</p>
                    <button class="add-to-favorite-button">加入喜愛名單</button>
                </div>
                
            `;
            infowindow.setContent(contentString);
            infowindow.open(map, marker);
        }
    });
}

function clearMarkers() {
    for (let i = 0; i < markers.length; i++) {
        markers[i].setMap(null);
    }
    markers.length = 0;
}

window.initMap = initMap;
window.searchNearby = searchNearby;
export default initMap
