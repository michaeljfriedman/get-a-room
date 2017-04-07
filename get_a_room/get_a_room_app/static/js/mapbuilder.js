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
                setMapView(building);
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
function setMapView(building) {
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
            var content = '';  // default to empty content
            if (!jQuery.isEmptyObject(buildingStats)) {
                var content =  // this is a **horrible** way to populate the view, but I don't know how else to do it!
                    `<h1>` + buildingStats.name + `</h1>
                    <div class="my-wrapper">
                    <table id="table">`;
                for (i = 0; i < buildingStats.rooms.length; i++) {
                    var room = buildingStats.rooms[i];
                    content +=
                        `<tr class="tablerow">
                        <td>` + room.number + `</td>
                        <td>` + room.occupancy + ` / ` + room.capacity + `</td>
                        </tr>`
                }
                content +=
                    `</table>
                    </div>
                    <a href="#" class="close">Click to close</a>`;
            }

            // Slide out the panel with the content
            $.slidePanel.show({
                content: content
            }, {
                direction: 'right',
                closeSelector: '.close',
                useCssTransforms3d: true,
                useCssTransforms: true,
                useCssTransitions: true,
                loading: {
                    template: function(options) {
                        return '<div class="' + options.classes.loading + '"><div class="spinner"></div></div>';
                    }
                }
            });
        }
    });
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
