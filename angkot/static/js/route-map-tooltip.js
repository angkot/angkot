(function(angkot) {

"use strict"

var gm = google.maps;

angkot.route.Tooltip = function() {
  this._init();
}

var P = angkot.route.Tooltip.prototype;

P.setMap = function(map) {
  if (this._map) this._destroy();
  this._map = map;
  this._updateVisibility();
  if (map) this._setup();
}
P.getMap = function() {
  return this._map;
}

P.setContent = function(html) {
  this._content = html;
  this._$c.html(html);
  this._updateVisibility();
}
P.getContent = function() {
  return this._content;
}

P._init = function() {
  this._events = [];
  this._$c = $('<div class="angkot-map-tooltip"></div>');
  this._$c.hide();
}

P._setup = function() {
  var self = this;
  this._events = [
    gm.event.addListener(this._map, 'mouseover', function(e) { self._onMouseOver(e); }),
    gm.event.addListener(this._map, 'mouseout', function(e) { self._onMouseOut(e); }),
    gm.event.addListener(this._map, 'mousemove', function(e) { self._onMouseMove(e); }),
  ]
  this._div = this._map.getDiv();
  $(this._div).append(this._$c);
}

P._destroy = function() {
  this._$c.remove();
  for (var i=0; i<this._events.length; i++) {
    gm.event.removeListener(this._events[i]);
  }
  delete this._div;
}

P._onMouseOver = function(e) {
  var p = e.pixel;
  this._pos = {x: p.x, y:p.y};
  this._$c.css({left: this._pos.x+'px', top: this._pos.y+'px'});
  this._inMap = true;
  this._updateVisibility();
}

P._onMouseOut = function(e) {
  this._inMap = false;
  this._updateVisibility();
}

P._onMouseMove = function(e) {
  var p = e.pixel;
  var dx = p.x - this._pos.x + 20;
  var dy = p.y - this._pos.y + 10;
  this._$c.css('transform', 'translate('+dx+'px, '+dy+'px)');
}

P._updateVisibility = function() {
  if (!this._content || !this._inMap) this._$c.hide();
  else this._$c.show();
}

})(window.angkot);

