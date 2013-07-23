window.Tooltip = (function() {

var gm = google.maps;

var Tooltip = function() {
  this._init();
}

var p = Tooltip.prototype;

p.setMap = function(map) {
  if (this._map) this._destroy();
  this._map = map;
  if (map) this._setup();
}
p.getMap = function() {
  return this._map;
}

p.setContent = function(html) {
  this._content = html;
  this._$c.html(html);
}
p.getContent = function() {
  return this._content;
}

p._init = function() {
  this._$c = $('<div class="angkot-map-tooltip"></div>');
  this._$c.hide();
}

p._setup = function() {
  var self = this;
  this._onMouseOverListener = gm.event.addListener(this._map, 'mouseover', function(e) { self._onMouseOver(e); });
  this._onMouseOutListener = gm.event.addListener(this._map, 'mouseout', function(e) { self._onMouseOut(e); });
  this._onMouseMoveListener = gm.event.addListener(this._map, 'mousemove', function(e) { self._onMouseMove(e); });
  this._div = this._map.getDiv();
  $(this._div).append(this._$c);
}

p._destroy = function() {
  this._$c.remove();
  gm.event.removeListener(this._onMouseOverListener);
  gm.event.removeListener(this._onMouseOutListener);
  gm.event.removeListener(this._onMouseMoveListener);
  delete this._onMouseOverListener;
  delete this._onMouseOutListener;
  delete this._onMouseMoveListener;
  delete this._div;
}

p._onMouseOver = function(e) {
  var p = e.pixel;
  this._pos = {x: p.x, y:p.y};
  this._$c.css({left: this._pos.x+'px', top: this._pos.y+'px'});
  this._$c.show();
}

p._onMouseOut = function(e) {
  this._$c.hide();
}

p._onMouseMove = function(e) {
  var p = e.pixel;
  var dx = p.x - this._pos.x + 10;
  var dy = p.y - this._pos.y;
  this._$c.css('transform', 'translate('+dx+'px, '+dy+'px)');
}

return Tooltip;

})();

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

  var tooltip = new Tooltip();
  tooltip.setMap(map);
  tooltip.setContent('<strong>a</strong><br/>a b ca');
}

function setupPage() {
  setupMap();
}

$(document).ready(function() {
  setupPage();
});

})();

