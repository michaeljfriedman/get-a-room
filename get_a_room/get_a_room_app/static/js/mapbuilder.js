/*
 * mapbuilder.js
 *
 * This script loads, populates, and defines the behavior of the map
 * interface.
 */

$(document).ready(function() {

    // Domain name for AJAX requests
    var DOMAIN = 'http://localhost:8000/';

    // Helper function for replacing all occurrences of spaces with hyphens
    // in building name
    String.prototype.replaceAll = function(search, replacement) {
        var target = this;
        return target.split(search).join(replacement);
    };

    // Initialize the map
    var map = L.map('map').setView([40.345129502014764, -74.65826869010927], 17);
    map.setMaxZoom(17).setMinZoom(16);
    //map.setMaxBounds([[40.33761, -74.67769], [40.350697, -74.64053]]);

    L.control.locate({options:{
        setView: 'untilPan',
        icon: 'icon-location',
        }}).addTo(map);
    // L.Control.extend();

    // Load a tile layer
    layers = {}
    layers.tiles = L.tileLayer('https://api.mapbox.com/styles/v1/bnprks/cizxah1p6003n2rs6zu65xd7i/tiles/256/{z}/{x}/{y}?access_token={accessToken}',
    {
      accessToken:'pk.eyJ1IjoiYm5wcmtzIiwiYSI6ImNqMHVpaHBndjA2NG0zMnFheG5kbG5wa3AifQ.Cypl8hCriRSkA4XF-4GgMQ',
      attribution: 'Tiles by <a href="http://mapc.org">MAPC</a>, Data by <a href="http://mass.gov/mgis">MassGIS</a>',
      id: 'bnprks.9754e7af',
      maxZoom: 17,
      minZoom: 9
    }).addTo(map);

    /*------------------------------------------------------------------------*/

    // Pull locations and their GPS coordinates from the database, store in 'places'

    var places = {
        "type": "FeatureCollection",
        "features": []
    };

    $.ajax({
        url: DOMAIN + 'stats/most-recent',
        async: false,
        success: function(result) {
            // Parse JSON response and fill in places.features with building names,
            // GPS coordinates, and room occupancy stats.
            var buildingStats = JSON.parse(result);
            for (i = 0; i < buildingStats.length; i++) {
                // Each feature has mostly standard parameters. We set 'coordinates'
                // (GPS coordinates), 'popupContent' (text that appears in a
                // popup window), 'extra' (extra parameters that we can customize),
                // and 'id' (which just needs to be a unique integer).
               places.features.push({
                "type": "Feature",
                "geometry": {
                    "type": "Point",
                    "coordinates": [
                        // NOTE: The format for the coordinates is LONGITUDE, LATITUDE
                        // (backwards from the norm). This is DUMB! But ugh such is life.
                        parseFloat(buildingStats[i].lng), parseFloat(buildingStats[i].lat)
                    ]
                },
                "properties": {
                    "popupContent": buildingStats[i].name,
                    "extra": {
                        "rooms": buildingStats[i].rooms // list of rooms with occupancy stats
                    }
                },
                "id": i
            });
           }
       }
   });

    /*------------------------------------------------------------------------*/

    // Create and define behavior of markers

    // On mouse hover
    function onSetHover(e) {
        var marker = e.target;
        marker.setStyle({
            weight: 5,
            color: '#666',
            dashArray: '',
            fillOpacity: 0.7
        });
        this.openPopup();
    }

    // On removing mouse hover
    function onRemoveHover(e) {
        var marker = e.target;
        layers.places.resetStyle(marker);
        this.closePopup();
    }

    // Loads stats for 'building', and opens the side panel with those stats
    function openSidePanel(building) {
        // map.removeLayer(layers.tiles).removeLayer(layers.places);

        // Make AJAX request to get building stats
        $.ajax({
            url: DOMAIN + 'stats/building/' + building.replaceAll(' ', '-').toLowerCase(),
            success: function(result) {
                // Parse JSON response and populate view
                var buildingStats = JSON.parse(result);
                if (!jQuery.isEmptyObject(buildingStats)) {
                    $('#building-name').text(buildingStats.name);
                    for (i = 0; i < buildingStats.rooms.length; i++) {
                        // Make row for this room's stats
                        var room = buildingStats.rooms[i];
                        $('table#building-stats').append('<tr id="building-stats-row' + i + '"></tr>');
                        $('tr#building-stats-row' + i).append('<td id="building-stats-room-number' + i + '"></td>');
                        $('tr#building-stats-row' + i).append('<td id="building-stats-room-occupancy' + i + '"></td>');

                        // Populate row with data
                        $('td#building-stats-room-number' + i).text(room.number);
                        $('td#building-stats-room-occupancy' + i).text(room.occupancy + ' / ' + room.capacity);
                    }
                } else {
                    // Show error message in side panel instead of room data
                    $('#building-name').text('Oops!');
                    $('#building-stats-error-message').text('We couldn\'t find stats for this room!');
                }

                // Slide out the panel with the content
                $('#side-panel').slideDown(250);
            }
        });
    }

    // Closes the side panel
    function closeSidePanel() {
        $('#side-panel').slideUp(250);

        // Clear contents
        $('table#building-stats').html('');
        $('#building-stats-error-message').text('');
    }

    // Place markers on map
    layers.places = L.geoJSON(places, {
        style: function (feature) {
            return feature.properties && feature.properties.style;
        },

        onEachFeature: function (feature, layer) {
            // Adds mouse hover/click listeners and sets the marker's popup
            // window content. The parameter 'feature' passed in is one of the
            // feature objects in 'places', defined in the last section.
            var popupContent = "<p>Click for stats on rooms in this building!</p> <strong>" + feature.properties.popupContent + "</strong>";
            layer.bindPopup(popupContent,{closeButton: false, autoPan: false});
            layer.on({
                'mouseover': onSetHover.bind(layer),
                'mouseout': onRemoveHover.bind(layer),
                'click': function(e) {
                    this.closePopup();
                    var building = feature.properties.popupContent;
                    openSidePanel(building);
                    // map.addLayer(layers.tiles).addLayer(layers.places);
                }
            });
        },

        pointToLayer: function (feature, latlng) {
            // Set this marker fill color based on occupancy of the rooms.
            // Again, 'feature' is one of the feature objects in 'places'.
            var rooms = feature.properties.extra.rooms;
            var FILLCOLOR;
            var numRoomsOpen = 0;
            var totalRooms = rooms.length;
            for (i = 0; i < totalRooms; i++) {
                if (rooms[i].occupancy / rooms[i].capacity < 0.8) {
                    numRoomsOpen++;
                }
            }
            var ratio = numRoomsOpen / totalRooms;
            if (ratio >= 0.5)
                FILLCOLOR = '#36ce4c'; // green
            else if (0.0 < ratio && ratio < 0.5)
                FILLCOLOR = '#fec041'; // yellow
            else
                FILLCOLOR = '#fc635d'; // red

            return L.circleMarker(latlng, {
                radius: 8,
                fillColor: FILLCOLOR,
                color: '#000',
                weight: 0.2,
                opacity: 0.5,
                fillOpacity: 0.3
            });
        }
    }).addTo(map);

    /*------------------------------------------------------------------------*/

    // Set click listener on 'close' button of the side panel
    $('#close-side-panel').click(closeSidePanel);
});
