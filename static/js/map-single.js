
const lat = document.getElementById("lat").value;
const lon = document.getElementById("lon").value;
// if ($('#map-contact').length) {
// 		var map = L.map('map-contact', {
// 			zoom: 5,
// 			maxZoom: 20,
// 			tap: false,
// 			gestureHandling: true,
// 			center: [lat, lon]
// 		});

// 		map.scrollWheelZoom.disable();

// 		var Hydda_Full = L.tileLayer('https://{s}.tile.openstreetmap.de/tiles/osmde/{z}/{x}/{y}.png', {
// 			scrollWheelZoom: false,
// 			attribution: '&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors'
// 		}).addTo(map);

// 		var icon = L.divIcon({
// 			html: '<i class="fa fa-building"></i>',
// 			iconSize: [50, 50],
// 			iconAnchor: [50, 50],
// 			popupAnchor: [-20, -42]
// 		});

// 		var marker = L.marker([lat, lon], {
// 			icon: icon
// 		}).addTo(map);
	// }


    var map;
    var geocoder;
    function InitializeMap() {

        var latlng = new google.maps.LatLng(lat, lon);
        var myOptions =
        {
            zoom: 8,
            center: latlng,
            mapTypeId: google.maps.MapTypeId.ROADMAP,
            disableDefaultUI: true
        };
        map = new google.maps.Map(document.getElementById("map"), myOptions);
    }

    function FindLocaiton() {
        geocoder = new google.maps.Geocoder();
        InitializeMap();

        var address = document.getElementById("addressinput").value;
        geocoder.geocode({ 'address': address }, function (results, status) {
            if (status == google.maps.GeocoderStatus.OK) {
                map.setCenter(results[0].geometry.location);
                var marker = new google.maps.Marker({
                    map: map,
                    position: results[0].geometry.location
                });

            }
            else {
                alert("Geocode was not successful for the following reason: " + status);
            }
        });

    }


    function Button1_onclick() {
        FindLocaiton();
    }

    window.onload = InitializeMap;