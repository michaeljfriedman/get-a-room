// initialize the map
var map = L.map('map').setView([40.345129502014764, -74.65826869010927], 17);
map.setMaxZoom(17).setMinZoom(16);
//map.setMaxBounds([[40.33761, -74.67769], [40.350697, -74.64053]]);

L.control.locate({options:{
    setView: 'untilPan',
    icon: 'icon-location',
    }}).addTo(map);
// L.Control.extend();

layers = {}
// load a tile layer
layers.tiles = L.tileLayer('https://api.mapbox.com/styles/v1/bnprks/cizxah1p6003n2rs6zu65xd7i/tiles/256/{z}/{x}/{y}?access_token={accessToken}',
{
  accessToken:'pk.eyJ1IjoiYm5wcmtzIiwiYSI6ImNqMHVpaHBndjA2NG0zMnFheG5kbG5wa3AifQ.Cypl8hCriRSkA4XF-4GgMQ',
  attribution: 'Tiles by <a href="http://mapc.org">MAPC</a>, Data by <a href="http://mass.gov/mgis">MassGIS</a>',
  id: 'bnprks.9754e7af',
  maxZoom: 17,
  minZoom: 9
}).addTo(map);

function onEachFeature(feature, layer) {
    var popupContent = "<p>Click for stats on rooms in this building!</p> <strong>" + feature.properties.popupContent + "</strong>";


    layer.bindPopup(popupContent,{closeButton: false, autoPan: false});
    layer.on({
            'mouseover': setHover.bind(layer),
            'mouseout': removeHover.bind(layer),
             'click': function(e) {
                map.closePopup();
                var building = feature.properties.popupContent;
                openSidePanel(building);
                // map.addLayer(layers.tiles).addLayer(layers.places);
            }
    });
}

function setHover(e) {
    this.openPopup()
    var layer = e.target;
    layer.setStyle({
        weight: 5,
        color: '#666',
        dashArray: '',
        fillOpacity: 0.7
    });
}

// Loads stats for 'building', and opens the side panel with those stats
function openSidePanel(building) {
    // Helper function for replacing all occurrences of spaces with hyphens
    // in building name
    String.prototype.replaceAll = function(search, replacement) {
        var target = this;
        return target.split(search).join(replacement);
    };
    // map.removeLayer(layers.tiles).removeLayer(layers.places);

    // Make AJAX request to get building stats
    $.ajax({
        url: 'http://localhost:8000/stats/building/' + building.replaceAll(' ', '-').toLowerCase(),
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

function removeHover(e) {
    map.closePopup();
    layers.places.resetStyle(e.target);
}

layers.places = L.geoJSON(places, {
    style: function (feature) {
        return feature.properties && feature.properties.style;
    },

    onEachFeature: onEachFeature,

    pointToLayer: function (feature, latlng) {
        return L.circleMarker(latlng, {
            radius: 8,
            fillColor: "#ff7800",
            color: "#000",
            weight: 0.2,
            opacity: 0.5,
            fillOpacity: 0.2
        });
    }
}).addTo(map);

/*----------------------------------------------------------------------------*/

$(document).ready(function() {
    // Set click listener on 'close' button of the side panel
    $('#close-side-panel').click(closeSidePanel);
});
