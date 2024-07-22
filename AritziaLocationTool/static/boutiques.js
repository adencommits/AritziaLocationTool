// boutiques.js

// Get the checkboxes and the page label
var checkboxes = document.querySelectorAll('.collapsible input');
var pageLabel = document.querySelector('.page-label');

// Function to check the state of the checkboxes
function checkCheckboxes() {
    // Check if both checkboxes are checked
    if (Array.from(checkboxes).every(c => c.checked)) {
        // If both checkboxes are checked, reduce the padding-top of the page label
        pageLabel.style.paddingTop = '30px';
    } else {
        // If not, reset the padding-top of the page label
        pageLabel.style.paddingTop = '150px';
    }
}

// Add an event listener to each checkbox
checkboxes.forEach(function(checkbox) {
    checkbox.addEventListener('change', checkCheckboxes);
});

// Call the function initially to set the correct padding-top
checkCheckboxes();

function initMap() {
    // Clean white style with black contrast
    var map = new google.maps.Map(document.getElementById('map'), {
        center: {lat: 43.6532, lng: -79.3832}, // Coordinates for Toronto
        zoom: 8,
        styles: [
            {
                "featureType": "all",
                "elementType": "all",
                "stylers": [
                    {
                        "saturation": -100
                    },
                    {
                        "lightness": 45
                    }
                ]
            },
            {
                "featureType": "road",
                "elementType": "geometry.fill",
                "stylers": [
                    {
                        "color": "#eeeeee"
                    }
                ]
            },
            {
                "featureType": "road",
                "elementType": "geometry.stroke",
                "stylers": [
                    {
                        "color": "#eeeeee"
                    }
                ]
            },
            {
                "featureType": "road",
                "elementType": "labels.text.fill",
                "stylers": [
                    {
                        "color": "#000000"
                    }
                ]
            },
            {
                "featureType": "road",
                "elementType": "labels.text.stroke",
                "stylers": [
                    {
                        "color": "#ffffff"
                    }
                ]
            },
            {
                "featureType": "road.highway",
                "elementType": "geometry.fill",
                "stylers": [
                    {
                        "color": "#ffffff"
                    }
                ]
            },
            {
                "featureType": "road.highway",
                "elementType": "geometry.stroke",
                "stylers": [
                    {
                        "color": "#ffffff"
                    }
                ]
            },
            {
                "featureType": "road.highway",
                "elementType": "labels.text.fill",
                "stylers": [
                    {
                        "color": "#000000"
                    }
                ]
            },
            {
                "featureType": "road.highway",
                "elementType": "labels.text.stroke",
                "stylers": [
                    {
                        "color": "#ffffff"
                    }
                ]
            },
            // ... more style rules as needed ...
        ],
        streetViewControl: false,
        mapTypeControl: false,
        mapTypeId: 'roadmap',
        disableDoubleClickZoom: true,
    });

    // Create the search box and link it to the UI element.
    var input = document.getElementById('searchInput');
    var searchBox = new google.maps.places.SearchBox(input);
    map.controls[google.maps.ControlPosition.TOP_LEFT].push(input);

    // Bias the SearchBox results towards current map's viewport.
    map.addListener('bounds_changed', function() {
        searchBox.setBounds(map.getBounds());
    });

    var markers = [];
    // Listen for the event fired when the user selects a prediction and retrieve
    // more details for that place.
    searchBox.addListener('places_changed', function() {
        var places = searchBox.getPlaces();

        if (places.length == 0) {
            return;
        }

        markers.forEach(function(marker) {
            marker.setMap(null);
        });
        markers = [];

        var bounds = new google.maps.LatLngBounds();
        places.forEach(function(place) {
            if (!place.geometry) {
                console.log("Returned place contains no geometry");
                return;
            }

            markers.push(new google.maps.Marker({
                map: map,
                title: place.name,
                position: place.geometry.location
            }));

            var lat = place.geometry.location.lat();
            var lng = place.geometry.location.lng();

            document.getElementById('savedLocation').textContent = 'Location Saved: Latitude ' + lat + ', Longitude ' + lng;

            $.ajax({
                url: '/save_coordinates',
                type: 'POST',
                data: { lat: lat, lng: lng },
                success: function(response) {
                    console.log('Coordinates saved successfully.');
                },
                error: function(error) {
                    console.log(error);
                }
            });

            if (place.geometry.viewport) {
                bounds.union(place.geometry.viewport);
            } else {
                bounds.extend(place.geometry.location);
            }
        });
        map.fitBounds(bounds);
    });

    // Add a dblclick event listener to the map
    google.maps.event.addListener(map, 'dblclick', function(event) {
        // Get the latitude and longitude of the double clicked point
        var lat = event.latLng.lat();
        var lng = event.latLng.lng();

        // Update the coordinates text with the latitude and longitude of the double clicked point
        document.getElementById('savedLocation').textContent = 'Location Saved: Latitude ' + lat + ', Longitude ' + lng;

        // Send an AJAX request to the Python Flask server
        $.ajax({
            url: '/save_coordinates',  // the endpoint, a route to handle the request in your Python script
            type: 'POST',  // http method
            data: { lat: lat, lng: lng },  // Corrected data keys to 'lat' and 'lng'

            // handle a successful response
            success: function(response) {
                console.log('Coordinates saved successfully.');
            },

            // handle a non-successful response
            error: function(error) {
                console.log(error);
            }
        });
    });
}

// Add an event listener to the "Begin Assessment" button
$('#get-started-retail').click(function() {
    // Send an AJAX request to the Flask server
    $.ajax({
        url: '/run_retail_scripts',  // the endpoint to run the scripts
        type: 'GET',  // http method

        // handle a successful response
        success: function(response) {
            console.log('Scripts executed successfully.');
        },

        // handle a non-successful response
        error: function(error) {
            console.log(error);
        }
    });
});
