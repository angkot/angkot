(function() {

"use strict"

var JAKARTA = [-6.1744444, 106.8294444];

var gm = google.maps,
    map = undefined;

function setupMap() {
  var target = document.getElementById('map');
  var opts = {
    center: new gm.LatLng(JAKARTA[0], JAKARTA[1]),
    zoom: 12,
    mapTypeId: gm.MapTypeId.ROADMAP,
    streetViewControl: false,
    mapTypeControl: false,
    panControl: false,
    zoomControl: true,
    zoomControlOptions: {
      position: gm.ControlPosition.RIGHT_TOP,
    },
  }

  map = new gm.Map(target, opts);

  // move the controls a bit lower
  var spacer = $('<div class="map-control-spacer"/>')[0];
  spacer.index = -1
  map.controls[gm.ControlPosition.RIGHT_TOP].push(spacer);
}

function setupPage() {
  setupMap();
}

$(document).ready(function() {
  setupPage();
});

})();

