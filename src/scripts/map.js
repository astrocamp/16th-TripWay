let map;
let currentPosition;
let directionsService;
let directionsRenderer;

function initMap() {
    map = new google.maps.Map(document.getElementById("map"), {
        center: currentPosition,
        zoom: 16,
    });

    directionsService = new google.maps.DirectionsService();
    directionsRenderer = new google.maps.DirectionsRenderer();
    directionsRenderer.setMap(map);

    // 獲取搜索輸入框
    const input = document.getElementById("pac-input");


    console.log('test');

    // 指定需要的地點數據字段
    const autocomplete = new google.maps.places.Autocomplete(input, {
        fields: ["place_id", "geometry", "formatted_address", "name"],
    });

    // 創建一個圓形區域，半徑為100公尺
    const circle = new google.maps.Circle({
        center: currentPosition,
        radius: 100, // 100 公尺
    });

    // 設置 Autocomplete 的搜索範圍為圓形區域
    autocomplete.setBounds(circle.getBounds());

    // 添加搜索輸入框到地圖上方左側
    map.controls[google.maps.ControlPosition.TOP_LEFT].push(input);

    const infowindow = new google.maps.InfoWindow();
    const infowindowContent = document.getElementById("infowindow-content");

    infowindow.setContent(infowindowContent);

    const marker = new google.maps.Marker({ map: map });

    marker.addListener("click", () => {
        infowindow.open(map, marker);
    });

    autocomplete.addListener("place_changed", () => {
        infowindow.close();

        const place = autocomplete.getPlace();

        if (!place.geometry || !place.geometry.location) {
            return;
        }

        if (place.geometry.viewport) {
            map.fitBounds(place.geometry.viewport);
        } else {
            map.setCenter(place.geometry.location);
            map.setZoom(7);
        }

        marker.setPlace({
            placeId: place.place_id,
            location: place.geometry.location,
        });
        marker.setVisible(true);
        infowindowContent.children.namedItem("place-name").textContent = place.name;
        // infowindowContent.children.namedItem("place-id").textContent =
            // place.place_id;
        infowindowContent.children.namedItem("place-address").textContent =
            place.formatted_address;
        infowindow.open(map, marker);

        // 計算並顯示路線
        calculateAndDisplayRoute(currentPosition, place.geometry.location);
    });
}


function calculateAndDisplayRoute(origin, destination) {
    directionsService.route(
        {
            origin: origin,
            destination: destination,
            travelMode: 'DRIVING', // 這裡可以是 'DRIVING', 'WALKING', 'BICYCLING', 或 'TRANSIT'
        },
        (response, status) => {
            if (status === 'OK') {
                directionsRenderer.setDirections(response);
                const route = response.routes[0];
                // 计算总距离和预计行驶时间
                const distance = route.legs[0].distance.text;
                const duration = route.legs[0].duration.text;

                document.getElementById("distance").textContent = distance;
                document.getElementById("duration").textContent = duration;
                // console.log('Distance: ' + distance);
                // console.log('Duration: ' + duration);
            } else {
                window.alert('Directions request failed due to ' + status);
            }
        }
    );
}

// 獲取用戶位置
navigator.geolocation.getCurrentPosition(function (position) {
    currentPosition = {
        lat: position.coords.latitude,
        lng: position.coords.longitude,
    };

    // 初始化地圖
    initMap();
});


export default initMap
