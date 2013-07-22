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
    minZoom: 11,
    maxZoom: 18,
    mapTypeId: gm.MapTypeId.ROADMAP,
    streetViewControl: false,
  }

  map = new gm.Map(target, opts);
}

function setupPage() {
  setupMap();
}

$(document).ready(function() {
  setupPage();
});

})();

