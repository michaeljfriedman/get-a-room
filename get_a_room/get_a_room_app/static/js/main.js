/* global overlay_control */
/* global mapPos */
/* global footprints */
/* global layers */
/* global map */
/* global L */

map = L.map('map', {
    scrollWheelZoom: false,
    maxBoundsViscosity: 1.0,
});

//Holds references to different map layers
layers = {};

layers.tiles = L.tileLayer(//'https://api.mapbox.com/styles/v1/bnprks/cizxah1p6003n2rs6zu65xd7i/tiles/256/{z}/{x}/{y}?access_token={accessToken}', {
  'https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token={accessToken}', {
    attribution: 'Map data &copy; <a href="http://openstreetmap.org">OpenStreetMap</a> contributors, <a href="http://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, Imagery &copy <a href="http://mapbox.com">Mapbox</a>, Rooms app by Ben Parks \'17',
    id: 'bnprks.9754e7af',//'mapbox.streets-basic',
    accessToken: 'pk.eyJ1IjoiYm5wcmtzIiwiYSI6ImNqMHVpaHBndjA2NG0zMnFheG5kbG5wa3AifQ.Cypl8hCriRSkA4XF-4GgMQ'
});

layers.footprints = L.geoJson(footprints, {
    style: function (feature) {
        // var colors = {
        //     butler: "#0068AC",
        //     whitman : "#89CCE2",
        //     rockefeller : "#6EB43F",
        //     mathey: "#941e00",
        //     forbes: "#EF4035",
        //     wilson: "#F8981D",
        //     upperclass: "#828282"
        // }
        var colleges = buildings[feature.properties.id].college.sort()
        // var fill = colors[colleges[0]]
        if (colleges.length > 1) {
            fill = "url(#" + colleges.join('-') + ")"
        }
        return {
            fillColor: fill,
            weight: 2,
            opacity: 1,
            color: 'white',
            dashArray: '3',
            fillOpacity: 0.7
       };
    },
    onEachFeature: function(feature, layer) {
        var building = buildings[feature.properties.id]
        layer.bindPopup('<strong>' + building.name + '</strong><br/>Click to view floorplans',
                           {closeButton: false, autoPan: false});

        layer.on({
            'mouseover': setHover.bind(layer),
            'mouseout': removeHover.bind(layer),
            'popupopen': function(e) {
                  var b = layer.getBounds();
                  var lat = b.getNorth()
                  var lng = b.getCenter().lng
                  e.popup.setLatLng([lat, lng])
            },
             'click': function(e) {
                 layers.footprints.resetStyle(e.target);
                 setMapView(building.id + "-" + building.floors[0])
            }
        });
    }
});

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

function removeHover(e) {
    map.closePopup();
    layers.footprints.resetStyle(e.target);
}

overlay_control = null;
legend_control = new LegendControl();
//Store the map position in order to restore the map view after viewing floorplans
mapPos = {center: [40.345129502014764, -74.65826869010927], zoom: 17};

//Call setMapView("BULIDINGID-FLOOR") to set the map to show the designated floorplan.
//Call setMapView() to reset the map to the campus map view
function setMapView(floorplan_id) {
    if (floorplan_id == null) {
        //Reset the map to the basic view
        if(map.hasLayer(layers.floorplan)) map.removeLayer(layers.floorplan);
        map.addLayer(layers.tiles).addLayer(layers.footprints);
        map.setMaxZoom(18).setMinZoom(16);
        map.setMaxBounds([[40.33761, -74.66769], [40.350697, -74.65053]]);
        map.setView(mapPos.center, mapPos.zoom, {reset: true});
        map.setZoom(mapPos.zoom, {animate: false});
        mapPos = null;


        map.addControl(legend_control);
        if (overlay_control) {
            map.removeControl(overlay_control);
        }
        $(".searchbox").show()
        $("#searchbox").val("").focus()

    } else {
        $(".searchbox").hide()
        map.removeControl(legend_control);
        var portraitOrientation = ["0030-A","0092-A","0636-00","0636-01","0636-02","0636-03","0636-04","0668-00","0668-01","0668-A","0686-04"];
        var container = document.getElementById("map")
        var mapDimensions = {width: container.clientWidth, height:container.clientHeight};

        var rawImgDimensions = {width: 3400,height: 2200};
        //Check if the image is in portrait orientation
        for (var i = 0; i < portraitOrientation.length; i++) {
            if (floorplan_id == portraitOrientation[i]) {
                rawImgDimensions = {height: 3400,width: 2200}
            }
        }
        //Fit the image dimensions to fit within the map container
        var imgDimensions;
        if (mapDimensions.width/rawImgDimensions.width > mapDimensions.height/rawImgDimensions.height) {

            imgDimensions = {width: rawImgDimensions.width/rawImgDimensions.height*mapDimensions.height,
                            height: mapDimensions.height}
        } else {

            imgDimensions = {width: mapDimensions.width,
                            height:rawImgDimensions.height/rawImgDimensions.width*mapDimensions.width}
        }

        //Set map zoom and center
        var w = imgDimensions.width,
            h = imgDimensions.height,
            url = '/static/newrooms/svgz/' + floorplan_id + ".svgz" + cache_bust;

            var southWest = map.unproject([0, h], 16);
            var northEast = map.unproject([w, 0], 16);
            var bounds = new L.LatLngBounds(southWest, northEast);

        map.removeLayer(layers.tiles).removeLayer(layers.footprints);
        if (map.hasLayer(layers.floorplan)) map.removeLayer(layers.floorplan);
        layers.floorplan = L.imageOverlay(url, bounds);
        map.addLayer(layers.floorplan);

        if (mapPos == null) {
            mapPos = {center: map.getCenter(), zoom: map.getZoom()};

            map.setMaxBounds(bounds);
            map.setMinZoom(16).setMaxZoom(18);
            map.setView(map.unproject([w/2, h/2], 16),16, {reset: true});
            map.setZoom(16);

        }

        //Set overlay
        if (overlay_control) {
            map.removeControl(overlay_control);
        }
        var building_id = floorplan_id.split("-")[0],
            floor_id = floorplan_id.split("-")[1]
        overlay_control = new OverlayControl({"building_id":building_id, "floor_id":floor_id});
        map.addControl(overlay_control)

    }
}

/** Initialize the map with the given layers **/
setMapView(); //Shouldn't have to set to basic map view first, but something floorplan doesn't show when I go straight to building floorplan
var hash = window.location.hash.slice(1);
if (hash) {
    var building_id = hash.split('-')[0];
    var floor_id = hash.split('-')[1];
    if(buildings[building_id] && buildings[building_id].floors.indexOf(floor_id) != -1)
        setMapView(hash)
}

var substringMatcher = function(strs) {
    return function findMatches(q, cb) {

        var matches, substringRegex;

        // an array that will be populated with substring matches
        matches = [];

        // regex used to determine if a string contains the substring `q`
        substrRegex = new RegExp(q, 'i');

        // iterate through the pool of strings and for any string that
        // contains the substring `q`, add it to the `matches` array
        for (var str in dorms) {
            if (substrRegex.test(str)) {
                matches.push(str);
            }
        };

        cb(matches);
    };
};
var dorms = {}
for (var i in buildings) {
    dorms[buildings[i].name] = i;
}

$("#searchbox").typeahead({
        hint: true,
        highlight: true,
        minLength: 1
        },
        {
        name: 'dorms',
        source: substringMatcher(dorms)
});

$("#searchbox").bind("typeahead:select input", function() {
    if (dorms[this.value] !== undefined) {
        building = buildings[dorms[this.value]];
        setMapView(building.id + "-" + building.floors[0]);
    }
})
