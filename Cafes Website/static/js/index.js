// GOOGLE MAP //
function initMap() {
    var map;
    var bounds = new google.maps.LatLngBounds();
    var mapOptions = {
        mapTypeId: 'roadmap'};


    // Display a map on the web page
    map = new google.maps.Map(document.getElementById("map"), mapOptions);
    map.setTilt(50);
    var redIcon = "/static/images/pin.png";
    var blueIcon = "/static/images/location.png";
    var infoWindow = new google.maps.InfoWindow();
    var tableRows = document.querySelectorAll(".table-row");
    var markers = [];

    tableRows.forEach(function (row) {
        var markerName = row.getAttribute('data-marker-name');
        var markerLat = parseFloat(row.getAttribute('data-lat'));
        var markerLng = parseFloat(row.getAttribute('data-lng'));
        var position = new google.maps.LatLng(markerLat, markerLng);

        var marker = new google.maps.Marker({position: position, map: map, title: markerName, icon: {url: blueIcon, scaledSize: new google.maps.Size(40, 40),}});

        // Inserisco i markers in una lista
        markers.push(marker);

        // Evento click per mostrare un'InfoWindow quando si fa clic sul marker
        marker.addListener('click', function() {
            infoWindow.setContent(markerName);
            infoWindow.open(map, marker); });

        // Aggiungi eventi mouseenter e mouseleave alla riga della tabella
        row.addEventListener('mouseenter', function() {
            var markerIndex = parseInt(row.getAttribute('data-marker-index'));
            if (markerIndex >= 0 && markerIndex < markers.length) {
                infoWindow.setContent(markerName);
                infoWindow.open(map, marker);

            var icon = {
                url: redIcon,
                scaledSize: new google.maps.Size(80, 80),
            };

            markers[markerIndex].setIcon(icon)
            } });


        row.addEventListener('mouseleave', function() {
            var markerIndex = parseInt(row.getAttribute('data-marker-index'));
            var icon = {
                url: blueIcon,
                scaledSize: new google.maps.Size(40, 40),
                };
            markers[markerIndex].setIcon(icon);
        });


        // Aggiungi il marker alla lista dei bounds
        bounds.extend(position);
    });

    // Centra la mappa per adattarla a tutti i marker
    map.fitBounds(bounds);

    // Imposta il livello di zoom in modo che i marker siano visibili completamente
    var boundsListener = google.maps.event.addListener(map, 'bounds_changed', function() {
        if (this.getZoom() > 14) {
            this.setZoom(14);
        }
        google.maps.event.removeListener(boundsListener);
    });
}

// inizializzo la mappa
window.initMap = initMap;

// CAFE EXTERNAL LINKS //
document.addEventListener("DOMContentLoaded", function () {
// Get all the table rows with the class "table-row"
    const tableRows = document.querySelectorAll(".table-row");

    // Add a click event listener to each table row
    tableRows.forEach(function (row) {
        row.addEventListener("click", function () {
        // Get the URL from the "data-url" attribute of the clicked row
        const url = row.getAttribute("data-url");

        // Redirect to the specified URL
        window.open(url, "_blank");
        });
    });
});