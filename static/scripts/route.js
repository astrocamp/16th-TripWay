let map;
let markers = [];
let bounds;
let scheduleData = {};
let tripId = getTripIdFromUrl();
let directionsService;
let directionsRenderer;


function initMap() {
    let spinner = document.getElementById("loading-spinner"); 
    map = new google.maps.Map(document.getElementById('map'), {
        zoom: 16,
        center: { lat: 25.0383401, lng: 121.5060706 }
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
                let pos = {
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

    google.maps.event.addListenerOnce(map, 'tilesloaded', function() {
        spinner.style.display = "none";
    });

    loadSchedule();
}

function getTripIdFromUrl() {
    let currentUrl = window.location.href;
    let urlParts = currentUrl.split('/');
    let idIndex = urlParts.indexOf('trips') + 1;
    return idIndex !== -1 ? urlParts[idIndex] : null; 
}

function loadSchedule() {
    fetch('/schedules/get_schedule/')
        .then(response => response.json())
        .then(data => {
            let filteredData = data.filter(item => item.trip_id == tripId);
            scheduleData = groupByDate(filteredData);
            const tabButtons = document.querySelectorAll('.tab');
            tabButtons.forEach(button => {
                button.addEventListener('click', function() {
                    const selectedDate = this.getAttribute('data-date');
                    showScheduleForDate(selectedDate);
                });
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

function updateMapMarkers() {
    // 獲取目前選擇的日期：
    const selectedDateButton = document.querySelector(".active-tab");
    const selectedDate = selectedDateButton.getAttribute("data-date");

    // 顯示所選日期的行程
    console.log(selectedDate);
    showScheduleForDate(selectedDate);
    
    // 重新載入地圖
    const mapElement = document.getElementById("map");
    if (mapElement) {
        loadSchedule();
    }
}

function showTab(date, buttonId) { 
    markers = [];
    scheduleData = {};
    document.querySelectorAll(".tab").forEach(tab => {
        tab.classList.remove("active-tab");
    });
    document.getElementById(buttonId).classList.add("active-tab");
    updateMapMarkers(); // 更新地圖標記
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
        
function showScheduleForDate(date){
    clearMarkers();
    let dayData = scheduleData[date];
    if (!dayData) {
        centerMapToUserLocation();
        return;
    }

    console.log(dayData);

    let waypoints = [];
    let tripMode = null;

    dayData.forEach(function(item, index) {
        let position = { lat: parseFloat(item.spot__latitude), lng: parseFloat(item.spot__longitude) };
        let markerLabel = (index + 1).toString();
        let marker = new google.maps.Marker({
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
        }
    });
    
    let routeLabel = null;
    let travelMode = google.maps.TravelMode.DRIVING;

    if (tripMode === '汽車') {
        routeLabel = '汽車';
        travelMode = google.maps.TravelMode.DRIVING;
    } else if (tripMode === '走路') {
        routeLabel = '走路';
        travelMode = google.maps.TravelMode.WALKING;
    }

    let routeOptions = {
        strokeColor: "#FF6D1F",
        strokeWeight: 6,
        label: routeLabel
    };

    if (markers.length > 1) {
        let origin = markers[0].getPosition();
        let destination = markers[markers.length - 1].getPosition();

        directionsService.route({
            origin: origin,
            destination: destination,
            waypoints: waypoints,
            travelMode: travelMode
        }, function(response, status) {
            if (status === google.maps.DirectionsStatus.OK) {
                directionsRenderer.setOptions({ polylineOptions: routeOptions });
                directionsRenderer.setDirections(response);

                let route = response.routes[0];
                let totalDistance = 0;
                let totalDuration = 0;
                route.legs.forEach(leg => {
                    totalDistance += leg.distance.value;
                    totalDuration += leg.duration.value;
                });
                let totalDistanceKm = totalDistance / 1000;
                let totalDurationMin = totalDuration / 60;
                let infoContent ='<div class="info-window">' +
                                '<div>總路程: ' + totalDistanceKm.toFixed(2) + ' 公里</div>' +
                                '<div>花費時間: ' + totalDurationMin.toFixed(0) + ' 分</div>' +
                                '<div>交通方式: ' + routeLabel + '</div>';
                let infoWindow = new google.maps.InfoWindow({
                    content: infoContent
                });
                infoWindow.open(map, markers[0]);
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