dataiku.setAPIKey('XS897gKNfzzWBWlRfwFuZwMZKfTforJb');
dataiku.setDefaultProjectKey('ACCIDENTS');
/**
 * This template loads a DSS dataset containing geographical points and displays them on a world map.
 *
 * This is a simple "static" map: a whole dataset is shown. Each row of the dataset gets one circle on the map, with a popup.
 *
 * This template uses the 'leaflet' library.
 *
 * In this template, we assume that there are "latitude" and "longitude" columns.
 */

// Create a Map
var map = L.map('map').setView([47, 3], 5);

// Add an OpenStreetMap(c) based background
var cartodb =  new  L.tileLayer(
    'http://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}.png', {
    attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors, &copy; <a href="http://cartodb.com/attributions">CartoDB</a>'
})
map.addLayer(cartodb);

/* This is where we actually read the dataset.
 *
 * IMPORTANT NOTE
 *
 * Don't forget that you need to authorize this web app to read your dataset.
 * Go to Settings > Dataset and check at least the "Read data" permission
 */
dataiku.fetch('geocoded_by_concat_quality_check', {
        sampling : "head",
        limit : 200
    }, function (df) {

    // Add a map marker for each row on the dataset
    // Each marker is a circle. The size of the circle varies with the 'size' column values
    var nbRows = df.getNbRows();
    for (var i = 0; i < nbRows; i++) {
        var record = df.getRecord(i);

        // Replace by your own column names here
        var lat = parseFloat(record["latitude"]);
        var lon = parseFloat(record["longitude"]);
        var name = record["Num_Acc"];
        var size = parseInt(record["result_score"]);

        // Radius of the marker is in meters
        var radius = Math.log(size) * 20;

        var marker = new L.circle([lat, lon], radius, {
            color: 'red',
            fillColor: 'red',
            fillOpacity: 0.9
        }).bindPopup("Name: <strong>" + name + "</strong>");

        marker.addTo(map);
    };
});

/* Automatically added: Python interaction sample */
$.getJSON("/html-apps-backends/yroqJx8/first_api_call", function(data) {
    console.info(data);
});
