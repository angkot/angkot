(function(angkot) {

"use strict"

var gm = google.maps;

angkot.route.Editor = function() {
  this._init();
}

var P = angkot.route.Editor.prototype;

P.setMap = function(map) {
  if (this._map) this._destroyEvents();
  this._map = map;
  this._tooltip.setMap(map);
  for (var i=0; i<this._routes.length; i++) {
    this._routes[i].setMap(map);
  }
  if (this._map) this._initEvents();
}

P.getRoutes = function() {
  return this._routes;
}

P.setRouteArrays = function(paths) {
  this._clear();
  if (!paths) return;

  for (var i=0; i<paths.length; i++) {
    var data = paths[i];

    var route = new gm.Polyline({
      clickable: true,
      editable: true,
      draggable: false,
      strokeColor: '#FF0000',
      strokeOpacity: 0.9,
      strokeWeight: 3,
    });

    var path = route.getPath();
    for (var j=0; j<data.length; j++) {
      path.push(data[j]);
    }

    if (this._map) {
      route.setMap(this._map);
    }
    this._routes.push(route);
    this._initRouteEvents(route);
  }
}

P._init = function() {
  this._routes = [];
  this._events = {};
  this._tooltip = new angkot.route.Tooltip();
  this._createNextLine();
}

P._clear = function() {
  for (var i=0; i<this._routes.length; i++) {
    var route = this._routes[i];
    route.setMap(null);
    this._destroyRouteEvents(route);
  }
  this._routes = [];

  this._nextLine.setMap(null);
  this._nextPath.clear();

  if (this._path) {
    delete this._path;
    delete this._route;
  }

  this._tooltip.setContent(null);
}

P._initEvents = function() {
  var self = this;
  this._events.editor = [
    gm.event.addListener(this._map, 'mousemove', function(e) { self._onMouseMove(e); }),
    gm.event.addListener(this._map, 'mouseover', function(e) { self._onMouseOver(e); }),
    gm.event.addListener(this._map, 'mouseout', function(e) { self._onMouseOut(e); }),
    gm.event.addListener(this._map, 'click', function(e) { self._onClick(e); }),
    gm.event.addDomListener(document, 'keyup', function(e) { self._onKeyUp(e); }),
    gm.event.addDomListener(document, 'keydown', function(e) { self._onKeyDown(e); }),
  ]
}

P._destroyEvents = function() {
  for (var key in this._events) {
    var events = this._events[key];
    for (var i=0; i<events.length; i++) {
      gm.event.removeListener(events[i]);
    }
  }
}

P._createNextLine = function(pos) {
  var line = new gm.Polyline({
    clickable: false,
    editable: false,
    draggable: false,
    strokeColor: '#0000FF',
    strokeOpacity: 0.6,
    strokeWeight: 2,
  });
  this._nextLine = line;
  this._nextPath = line.getPath();
  this._nextPath.push(new gm.LatLng(0, 0));
  this._nextPath.push(new gm.LatLng(0, 0));
}

P._onMouseMove = function(e) {
  if (!this._nextLine || !this._nextPath.getLength()) return;
  this._nextPath.setAt(1, e.latLng);
}

P._onMouseOver = function(e) {
  if (this._routes.length === 0) {
    this._tooltip.setContent('Klik untuk membuat rute');
  }
}

P._onMouseOut = function(e) {
}

P._onClick = function(e) {
  if (!this._route) {
    // new route
    var route = new gm.Polyline({
      clickable: true,
      editable: true,
      draggable: false,
      strokeColor: '#0000FF',
      strokeOpacity: 0.9,
      strokeWeight: 3,
    });
    this._routes.push(route);

    this._isNewRoute = true;
    this._route = route;
    this._path = route.getPath();
    this._initRouteEvents(this._route);
    route.setMap(this._map);
  }

  this._path.push(e.latLng);
  this._nextPath.setAt(0, e.latLng);
  this._nextPath.setAt(1, e.latLng);
  this._nextLine.setMap(this._map);

  if (this._routes.length === 1) {
    var len = this._path.getLength();
    if (len == 1) {
      this._tooltip.setContent('Lanjutkan dengan mengklik jalur sepanjang rute');
    }
    else if (len == 2) {
      this._tooltip.setContent('Klik titik terakhir untuk mengakhiri');
    }
    else if (len == 3) {
      this._tooltip.setContent(null);
    }
  }
}

P._onKeyUp = function(e) {
  this._shiftKey = e.shiftKey;
  if (e.keyCode == 27) { // esc
    this._stopDrawing();
  }
}

P._onKeyDown = function(e) {
  this._shiftKey = e.shiftKey;
}

P._stopDrawing = function() {
  if (!this._route) return;

  this._route.setOptions({strokeColor:'#FF0000'});
  this._nextLine.setMap(null);
  this._nextPath.clear();
  this._tooltip.setContent(null);

  var index = this._routes.indexOf(this._route);
  if (this._path.getLength() === 1) {
    this._routes.splice(index, 1);
    this._route.setMap(null);
  }
  else {
    if (this._isNewRoute) {
      gm.event.trigger(this, 'route_added', index);
    }
    else {
      gm.event.trigger(this, 'route_updated', index);
    }
  }

  this._isNewRoute = false;
  delete this._path;
  delete this._route;
}

P._onRouteClick = function(route, e) {
  if (e.vertex === undefined) {
    this._onClick(e);
    return;
  }

  var path = route.getPath();
  var start = e.vertex === 0;
  var end = e.vertex === path.getLength() - 1;
  var tip = start || end;

  if (route === this._route) {
    if (e.vertex === this._path.getLength() - 1) {
      this._stopDrawing();
    }
    else {
      this._onClick(e);
    }
  }
  else if (this._route) {
    if (tip && this._shiftKey) {
      // merge

      var index = this._routes.indexOf(this._route);
      var withIndex = this._routes.indexOf(route);

      var arr = path.getArray().slice();
      if (end) {
        arr.reverse();
      }

      for (var i=0; i<arr.length; i++) {
        this._path.push(arr[i]);
      }

      route.setMap(null);
      this._routes.splice(withIndex, 1);
      var toIndex = this._routes.indexOf(this._route);

      this._route.setOptions({strokeColor:'#FF0000'});
      this._nextLine.setMap(null);
      this._nextPath.clear();
      this._tooltip.setContent(null);
      delete this._path;
      delete this._route;

      this._destroyRouteEvents(route);
      gm.event.trigger(this, 'route_merged', {first:index, second:withIndex, result:toIndex})
    }
    else {
      this._onClick(e);
    }
  }
  else {
    if (this._shiftKey) {
      var index = this._routes.indexOf(route);
      path.removeAt(e.vertex);
      if (path.getLength() == 1) {
        path.clear();
        route.setMap(null);
        this._routes.splice(index, 1);
        gm.event.trigger(this, 'route_deleted', index);
      }
      else {
        gm.event.trigger(this, 'route_updated', index);
      }
    }
    else if (tip) {
      // continue

      if (start) {
        // flip vertex
        var arr = path.getArray().slice();
        for (var i=0, j=arr.length-1; j>=0; i++, j--) {
          path.setAt(i, arr[j]);
        }
      }

      this._isNewRoute = false;
      this._route = route;
      this._path = route.getPath();
      route.setOptions({strokeColor: '#0000FF'});

      this._nextPath.setAt(0, e.latLng);
      this._nextPath.setAt(1, e.latLng);
      this._nextLine.setMap(this._map);

      this._tooltip.setContent(null);
    }
    else {
      this._onClick(e);
    }
  }
}

P._onRouteMouseOver = function(route, e) {
  if (this._routes.length === 0) return;
  if (e.vertex === undefined) return;

  if (this._nextPath.getLength() > 0 && e.vertex !== undefined) {
    // snap to vertex
    this._nextPath.setAt(1, e.latLng);
  }

  if (route === this._route) return;

  var path = route.getPath();
  var start = e.vertex === 0;
  var end = e.vertex === path.getLength() - 1;
  var tip = start || end;

  if (!this._route && tip) {
    this._tooltip.setContent('Klik untuk melanjutkan rute');
  }
  else if (!this._route) {
    this._tooltip.setContent('Untuk menghapus titik, tahan tombol <kbd>shift</kbd> lalu klik titik yang mau dihapus');
  }
  else if (tip) {
    this._tooltip.setContent('Untuk menggabung rute, tahan tombol <kbd>shift</kbd> lalu klik titik tujuan');
  }
}

P._onRouteMouseOut = function(route, e) {
  if (this._routes.length === 0) return;
  if (route === this._route) return;

  var path = route.getPath();
  var start = e.vertex === 0;
  var end = e.vertex === path.getLength() - 1;
  var tip = start || end;

  if (tip || !this._route) {
    this._tooltip.setContent(null);
  }
}

P._initRouteEvents = function(route) {
  var self = this;
  var events = [
    gm.event.addListener(route, 'click', function(e) { self._onRouteClick(route, e); }),
    gm.event.addListener(route, 'mouseover', function(e) { self._onRouteMouseOver(route, e); }),
    gm.event.addListener(route, 'mouseout', function(e) { self._onRouteMouseOut(route, e); }),
  ];
  this._events[route] = events;
}

P._destroyRouteEvents = function(route) {
  if (!route._$gr$events) return;
  var events = route._$gr$events;
  for (var i=0; i<events.length; i++) {
    gm.event.removeListener(events[i]);
  }
  delete route._$gr$events;
}

})(window.angkot);

