var map;
var markers = [];
var polylines = [];
var bounds;
var scheduleData = {};
var tripId = getTripIdFromUrl();

function initMap() {
    map = new google.maps.Map(document.getElementById('map'), {
        zoom: 16,
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
    var idIndex = urlParts.indexOf('trips') + 1; // 找到 "trips" 后面的部分
    return idIndex !== -1 ? urlParts[idIndex] : null; // 获取 ID
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

function showScheduleForDate(date) {
    var dayData = scheduleData[date];
    clearMarkers();
    if (!dayData) {
        centerMapToUserLocation();
        return;
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

    dayData.forEach(function(item, index) {
        var position = { lat: parseFloat(item.spot__latitude), lng: parseFloat(item.spot__longitude) };
        var markerLabel = (index + 1).toString();
        var marker = new google.maps.Marker({
            map: map,
            position: position,
            label: markerLabel,
            title: item.spot__name
        });
        markers.push(marker);
        bounds.extend(position);
    });
    var path = markers.map(marker => marker.getPosition());
    var polyline = new google.maps.Polyline({
        path: path,
        strokeColor: '#FF0000',
        strokeWeight: 3,
        map: map
    });

    polylines.push(polyline);
    map.fitBounds(bounds);
}

function clearMarkers() {
    markers.forEach(marker => marker.setMap(null));
    markers = [];
    polylines.forEach(polyline => polyline.setMap(null));
    polylines = [];
    bounds = new google.maps.LatLngBounds();
}