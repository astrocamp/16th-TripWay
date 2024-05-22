var map;
var markers = [];
var autocomplete;
let selectedPlace = null;

function initMap() {
    map = new google.maps.Map(document.getElementById('map'), {
        zoom: 16,
    });

    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(function(position) {
            var pos = {
                lat: position.coords.latitude,
                lng: position.coords.longitude
            };
            map.setCenter(pos);

            var currentLocationIcon = {
                url: 'http://maps.google.com/mapfiles/ms/icons/blue-dot.png',
                scaledSize: new google.maps.Size(50, 50),
            };
            var currentLocationMarker = new google.maps.Marker({
                map: map,
                position: pos,
                icon: currentLocationIcon
            });
        }, function() {
            handleLocationError(true, map.getCenter());
        });
    } else {
        handleLocationError(false, map.getCenter());
    }

    var input = document.getElementById('searchInput');
    autocomplete = new google.maps.places.Autocomplete(input);
    autocomplete.bindTo('bounds', map);
    autocomplete.addListener('place_changed', onPlaceChanged);
}

function handleLocationError(browserHasGeolocation, pos) {
    alert(browserHasGeolocation ?
        'Error: The Geolocation service failed.' :
        'Error: Your browser doesn\'t support geolocation.');
}

function onPlaceChanged() {
    var place = autocomplete.getPlace();
    if (!place.geometry) {
        window.alert("No details available for input: '" + place.name + "'");
        return;
    }
    selectedPlace = place;
    addMarker(place.geometry.location, place.name, place);
}

function addMarker(location, name, place) {
    var marker = new google.maps.Marker({
        map: map,
        position: location,
        icon: {
            url: 'http://maps.google.com/mapfiles/ms/icons/blue-dot.png',
            scaledSize: new google.maps.Size(50, 50)
        }
    });
    markers.push(marker);
    map.setCenter(location);
    var photos = place.photos;
    var photoUrl = photos ? photos[0].getUrl({ maxWidth: 200, maxHeight: 200 }) : '';


    place.address_components.forEach((element)=>{
        if (element.types[0] === 'administrative_area_level_1') {
            console.log(element.long_name);
            city = element.long_name;
        }
    })
    

    var infowindow = new google.maps.InfoWindow({
        content:
        `
        <div class="info-window">
            <h3>${name}</h3>
            <img src="${photoUrl}" alt="${name}">
            <p><strong>地址：</strong> ${place.formatted_address}</p>
            <p><strong>城市：</strong> ${city}</p>
            <p><strong>電話：</strong> ${place.formatted_phone_number || '無'}</p>
            <p><strong>營業時間：</strong> ${place.opening_hours ? place.opening_hours.weekday_text.join('<br>') : '無'}</p>
            <p><strong>網址：</strong> ${place.website ? `<a href="${place.website}" target="_blank">${place.website}</a>` : '無'}</p>
            <p><strong>評分：</strong> ${place.rating ? place.rating : '無'}</p>
        </div>
        `
    });

    marker.addListener('click', function() {
        infowindow.open(map, marker);
    });
    infowindow.open(map, marker);

    addToSidebar(name, place);
}

function addToSidebar(name, place) {
    var sidebar = document.getElementById('sidebar');
    var item = document.createElement('div');
    item.setAttribute('class', 'sidebar-list');
    item.setAttribute('data-spot-id', place.place_id);
    item.innerHTML = `
        <span>${name}</span>
        <button onclick="submitPlaceDetails('${place.place_id}')" style="background-color: lightblue; color: white; border: none; padding: 5px 10px; cursor: pointer;">save</button>
        <button onclick="deleteLocation('${place.place_id}')" style="background-color: lightblue; color: white; border: none; padding: 5px 10px; cursor: pointer;">Delete</button>
    `;
    sidebar.appendChild(item);
}

function addLocationToSidebar() {
    if (selectedPlace) {
        addToSidebar(selectedPlace.name, selectedPlace);
    } else {
        alert('請先搜尋一個地點');
    }
}

function submitPlaceDetails(placeId) {
    var place = selectedPlace;
    if (place.place_id !== placeId) {
        alert('地點ID不匹配');
        return;
    }

    place.address_components.forEach((element)=>{
        if (element.types[0] === 'administrative_area_level_1') {
            console.log(element.long_name);
            city = element.long_name;
        }
    })
    

    var formData = new FormData();
    formData.append('csrfmiddlewaretoken', getCookie('csrftoken'));
    formData.append('name', place.name);
    formData.append('address', place.formatted_address);
    formData.append('city', city || 'N/A'); 
    formData.append('latitude', place.geometry.location.lat());
    formData.append('longitude', place.geometry.location.lng());
    formData.append('phone', place.formatted_phone_number || 'N/A');
    formData.append('url', place.website || 'N/A');
    formData.append('rating', place.rating || 'N/A');
    formData.append('place_id', place.place_id);

    fetch('/spots/save_spot/', {
        method: 'POST',
        body: formData,
        headers: {
            'X-CSRFToken': getCookie('csrftoken')
        }
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then(data => {
        alert('Place saved successfully!');
        // removeMarkerAndSidebarItem(placeId);
    })
}

function deleteLocation(place_id) {
    fetch(`/spots/delete/${place_id}/`, {
        method: 'DELETE',
        headers: {
            'X-CSRFToken': getCookie('csrftoken')
        }
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then(data => {
        if (data.status === 'success') {
            alert(data.message);
            removeLocationFromUI(place_id);  // 删除成功后从UI中移除
        } else {
            alert(data.message);
        }
    })
    .catch(error => {
        console.error('There was a problem with the fetch operation:', error);
        alert('Failed to delete place, please try again.');
    });
}

function removeLocationFromUI(place_id) {
    const element = document.querySelector(`[data-spot-id="${place_id}"]`);
    if (element) {
        element.remove();
    }
}

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
