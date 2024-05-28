var map;
var markers = [];
var polylines = [];
var bounds;
var scheduleData = {};

function initMap() {
    map = new google.maps.Map(document.getElementById('map'), {
        zoom: 16,
        center: { lat: 25.0330, lng: 121.5654 }
    });

    bounds = new google.maps.LatLngBounds();
    loadSchedule();
}

function loadSchedule() {
    fetch('/schedules/get_schedule/')
        .then(response => response.json())
        .then(data => {
            scheduleData = groupByDate(data);
            const firstDate = Object.keys(scheduleData)[0];
            if (firstDate) {
                showScheduleForDate(firstDate);
            }
        })
        .catch(error => console.error('Error fetching schedule data:', error));
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
    document.querySelectorAll('.tab').forEach(tab => {
        tab.classList.remove('active-tab');
    });
    document.getElementById(buttonId).classList.add('active-tab');
    showScheduleForDate(date);
}

function showScheduleForDate(date) {
    var dayData = scheduleData[date];
    if (!dayData) {
        console.error("No schedule data for date: " + date);
        return;
    }

    markers.forEach(marker => marker.setMap(null));
    markers = [];
    polylines.forEach(polyline => polyline.setMap(null));
    polylines = [];
    bounds = new google.maps.LatLngBounds();

    dayData.sort((a, b) => new Date('1970/01/01 ' + a.start_time) - new Date('1970/01/01 ' + b.start_time));
    dayData.forEach(function(item, index) {
        var position = { lat: parseFloat(item.spot__latitude), lng: parseFloat(item.spot__longitude) };
        var markerLabel = String.fromCharCode(65 + index);
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