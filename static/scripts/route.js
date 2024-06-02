var map;
var markers = [];
var bounds;
var scheduleData = {};
var tripId = getTripIdFromUrl();
var directionsService;
var directionsRenderer;

function initMap() {
    map = new google.maps.Map(document.getElementById('map'), {
        zoom: 16,
    });

    directionsService = new google.maps.DirectionsService();
    directionsRenderer = new google.maps.DirectionsRenderer({
        map: map,
        suppressMarkers: true, 
        polylineOptions: {
            strokeColor: "#FF6D1F",
            strokeWeight: 6
        }
    });

    bounds = new google.maps.LatLngBounds();
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(
            function(position) {
                var pos = {
                    lat: position.coords.latitude,
                    lng: position.coords.longitude
                };
                map.setCenter(pos);
            },
            function() {
                handleLocationError(true, map.getCenter());
            }
        );
    } else {
        handleLocationError(false, map.getCenter());
    }
    loadSchedule();
}

function getTripIdFromUrl() {
    var currentUrl = window.location.href;
    var urlParts = currentUrl.split('/');
    var idIndex = urlParts.indexOf('trips') + 1;
    return idIndex !== -1 ? urlParts[idIndex] : null; 
}

function loadSchedule() {
    fetch('/schedules/get_schedule/')
        .then(response => response.json())
        .then(data => {
            var filteredData = data.filter(item => item.trip_id == tripId);
            scheduleData = groupByDate(filteredData);
        });

    const tabButtons = document.querySelectorAll('.tab');
    tabButtons.forEach(button => {
        button.addEventListener('click', function() {
            const selectedDate = this.getAttribute('data-date');
            showScheduleForDate(selectedDate);
        });
    });
}

function groupByDate(data) {
    return data.reduce((acc, item) => {
        const date = item.date;
        if (!acc[date]) {
            acc[date] = [];
        }
        acc[date].push(item);
        return acc;
    }, {});
}

function showTab(date, buttonId) {
    markers = [];
    scheduleData = {};
    document.querySelectorAll('.tab').forEach(tab => {
        tab.classList.remove('active-tab');
    });
    document.getElementById(buttonId).classList.add('active-tab');
    showScheduleForDate(date);
}

function centerMapToUserLocation() {
            if (navigator.geolocation) {
                navigator.geolocation.getCurrentPosition(
                    function(position) {
                        const userLocation = {
                            lat: position.coords.latitude,
                            lng: position.coords.longitude
                        };
                        map.setCenter(userLocation);
                        map.setZoom(16);
                    },
                    function(error) {
                        console.error("Error getting user's location:", error);
                    }
                );
            }
        }
        
function showScheduleForDate(date) {
    var dayData = scheduleData[date];
    clearMarkers();
    if (!dayData) {
        centerMapToUserLocation();
        return;
    }

    var waypoints = [];
    var tripMode = null;

    dayData.forEach(function(item, index) {
        var position = { lat: parseFloat(item.spot__latitude), lng: parseFloat(item.spot__longitude) };
        var markerLabel = (index + 1).toString();
        var marker = new google.maps.Marker({
            map: map,
            position: position,
            icon: createMarkerIcon(markerLabel),
            title: item.spot__name
        });
        markers.push(marker);
        bounds.extend(position);

        if (index > 0 && index < dayData.length - 1) {
            waypoints.push({
                location: position,
                stopover: true
            });
        }
        if (index === 0) {
            tripMode = item.trip__transportation;
            console.log(tripMode);
        }
    });
    
    var routeLabel = null;
    var travelMode = google.maps.TravelMode.DRIVING;

    if (tripMode === '汽車') {
        routeLabel = '汽車';
        travelMode = google.maps.TravelMode.DRIVING;
    } else if (tripMode === '大眾運輸') {
        routeLabel = '大眾運輸';
        travelMode = google.maps.TravelMode.TRANSIT;
    } else if (tripMode === '機車') {
        routeLabel = '機車';
        travelMode = google.maps.TravelMode.DRIVING; 
    } else if (tripMode === '走路') {
        routeLabel = '走路';
        travelMode = google.maps.TravelMode.WALKING;
    }

    // 根據交通方式設置路線的繪製選項
    var routeOptions = {
        strokeColor: "#FF6D1F",
        strokeWeight: 6,
        label: routeLabel
    };

    if (markers.length > 1) {
        var origin = markers[0].getPosition();
        var destination = markers[markers.length - 1].getPosition();

        directionsService.route({
            origin: origin,
            destination: destination,
            waypoints: waypoints,
            travelMode: travelMode
        }, function(response, status) {
            if (status === google.maps.DirectionsStatus.OK) {
                directionsRenderer.setOptions({ polylineOptions: routeOptions }); // 設置路線的繪製選項
                directionsRenderer.setDirections(response);
                // 在 info 框顯示總長
                var route = response.routes[0];
                var totalDistance = 0;
                var totalDuration = 0;
                route.legs.forEach(leg => {
                    totalDistance += leg.distance.value;
                    totalDuration += leg.duration.value;
                });
                var totalDistanceKm = totalDistance / 1000;
                var totalDurationMin = totalDuration / 60;
                var infoContent ='<div class="info-window">' +
                                '<div>總路程: ' + totalDistanceKm.toFixed(2) + ' 公里</div>' +
                                '<div>花費時間: ' + totalDurationMin.toFixed(0) + ' 分</div>' +
                                '<div>交通方式: ' + routeLabel + '</div>';
                var infoWindow = new google.maps.InfoWindow({
                    content: infoContent
                });
                infoWindow.open(map, markers[0]); // 在起點 marker 上顯示 info 框
            } else {
                Toast.fire({
                    icon: 'error',
                    title: '此模式規劃困難。請使用其他交通方式，如開車模式。'
                })
            }
        });
    }

    map.fitBounds(bounds);
}


function createMarkerIcon(label) {
    const canvas = document.createElement('canvas');
    const size = 30;
    canvas.width = size;
    canvas.height = size;
    const context = canvas.getContext('2d');

    context.beginPath();
    context.arc(size / 2, size / 2, size / 2, 0, 2 * Math.PI);
    context.fillStyle = '#FF6D1F';
    context.fill();

    context.fillStyle = '#FFFFFF';
    context.font = 'bold 14px Arial';
    context.textAlign = 'center';
    context.textBaseline = 'middle';
    context.fillText(label, size / 2, size / 2);

    return {
        url: canvas.toDataURL(),
        scaledSize: new google.maps.Size(size, size)
    };
}

function clearMarkers() {
    markers.forEach(marker => marker.setMap(null));
    markers = [];
    directionsRenderer.set('directions', null);
    bounds = new google.maps.LatLngBounds();
}

