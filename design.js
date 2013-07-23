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


window.PathEditor = (function() {

var gm = google.maps,
    geom = google.maps.geometry;

function getDistance(a, b) {
  return geom.spherical.computeDistanceBetween(a, b);
}

// is p closer to a than to b?
function isCloser(p, a, b) {
  var pa = getDistance(p, a);
  var pb = getDistance(p, b);
  return pa < pb;
}

function reversePath(path) {
  // reverse
  var arr = path.getArray().slice();
  for (var i=0, j=arr.length-1; i<arr.length; i++, j--) {
    path.setAt(i, arr[j]);
  }
}

var PathEditor = function() {
  this._init();
}

var p = PathEditor.prototype;

p.setMap = function(map) {
  if (this._map) this._destroy();
  this._map = map;
  if (this._map) this._setup();
}

p.getMap = function() {
  return this._map;
}

p.reset = function() {
  this._path.clear();
  this._nextPath.clear();
}

p.getPolyline = function() {
  return this._line;
}

p.setEnabled = function(enabled) {
  this._enabled = enabled;
  this._updateEvents();
}

p.isEnabled = function() {
  return this._enabled;
}

p._init = function() {
  this._line = new gm.Polyline({
    editable: true,
    clickable: true,
    draggable: false,
    strokeColor: '#FF0000',
    strokeOpacity: 1.0,
    strokeWeight: 3,
  });
  this._path = this._line.getPath();

  this._next = new gm.Polyline({
    editable: false,
    clickable: false,
    draggable: false,
    strokeColor: '#0000FF',
    strokeOpacity: 0.75,
    strokeWeight: 3,
  });
  this._nextPath = this._next.getPath();
}

p._setup = function() {
  this._line.setMap(this._map);
  this._next.setMap(this._map);
  this._updateEvents();
}

p._destroy = function() {
  this._line.setMap(null);
  this._next.setMap(null);
  this._updateEvents();
}

p._updateEvents = function() {
  if (this._map && this._enabled) {
    this._setupEvents();
  }
  else {
    this._destroyEvents();
  }
}

p._setupEvents = function() {
  if (this._onMouseMoveListener) return;

  var self = this;
  this._onMouseMoveListener = gm.event.addListener(this._map, 'mousemove', function(e) { self._onMouseMove(e); });
  this._onClickListener = gm.event.addListener(this._map, 'click', function(e) { self._onClick(e); });
  this._onLineDblClickListener = gm.event.addListener(this._line, 'dblclick', function(e) { self._onLineDblClick(e);});
  this._onKeyUpListener = gm.event.addDomListener(document, 'keyup', function(e) { self._onKeyUp(e); });
}

p._destroyEvents = function() {
  if (!this._onMouseMoveListener) return;

  gm.event.removeListener(this._onMouseMoveListener);
  gm.event.removeListener(this._onClickListener);
  delete this._onMouseMoveListener;
  delete this._onClickListener;

  gm.event.removeListener(this._onLineDblClickListener);
  delete this._onLineDblClickListener;

  gm.event.removeListener(this._onKeyUpListener);
  delete this._onKeyUpListener;
}

p._onMouseMove = function(e) {
  if (this._nextPath.getLength() > 0) {
    this._nextPath.setAt(1, e.latLng);
  }
}

p._onClick = function(e) {
  if (this._nextPath.getLength() === 0 && this._path.getLength() > 1) {
    var a = this._path.getAt(0);
    var b = this._path.getAt(this._path.getLength()-1);
    if (isCloser(e.latLng, a, b)) {
      reversePath(this._path);
    }
  }

  this._path.push(e.latLng);
  if (this._nextPath.getLength() === 0) {
    this._nextPath.push(e.latLng);
    this._nextPath.push(e.latLng);
  }
  this._nextPath.setAt(0, e.latLng);
}

p._onLineDblClick = function(e) {
  if (this._nextPath.getLength() > 0) {
    this._nextPath.clear();
  }
  else {
    this._path.removeAt(e.vertex);
    if (this._path.getLength() == 1) {
      this._path.clear();
    }
  }
}

p._onKeyUp = function(e) {
  if (e.keyCode != 27) return;
  if (this._nextPath.getLength() > 0) {
    this._nextPath.clear();
  }
  // TODO figure out how to disable the escape key event when the map lost focus
  // else if (this._path.getLength() > 0) {
  //   this._path.removeAt(this._path.getLength()-1);
  //   if (this._path.getLength() == 1) {
  //     this._path.clear();
  //   }
  // }
}

return PathEditor;

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

  // var tooltip = new Tooltip();
  // tooltip.setMap(map);
  // tooltip.setContent('<strong>a</strong><br/>a b ca');

  var pathEditor = new PathEditor();
  pathEditor.setMap(map);
  pathEditor.setEnabled(true);
}

function setupPage() {
  setupMap();
}

$(document).ready(function() {
  setupPage();
});

})();

