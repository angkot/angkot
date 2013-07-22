(function() {

"use strict"

var JAKARTA = [-6.1744444, 106.8294444];

var map = undefined;

function setupMap() {
  map = L.map('map', {
    center: JAKARTA,
    zoom: 13,
    zoomControl: false,
  })

  L.tileLayer('http://a.tiles.mapbox.com/v3/'+MAPBOX_KEY+'/{z}/{x}/{y}.png', {
    attribution: 'Map data &copy; <a href="http://openstreetmap.org">OpenStreetMap</a> contributors, <a href="http://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, Imagery &copy; <a href="http://www.mapbox.com">MapBox</a>',
    maxZoom: 18
  }).addTo(map);

  new L.Control.Zoom({position: 'bottomright'}).addTo(map);
}

function setupPage() {
  setupMap();
}

$(document).ready(function() {
  setupPage();
});

})();

