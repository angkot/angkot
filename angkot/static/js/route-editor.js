window.RouteEditor = (function() {

"use strict"

var gm = google.maps,
    geocoder = undefined;

function getDistance(p1, p2) {
  return gm.geometry.spherical.computeDistanceBetween(p1, p2);
}

var RouteEditor = function(target, opts) {
  this.target = target;
  this.opts = opts;
  this.pathUpdatedHandlers = [];

  this.path = {
    layer: undefined,
    data: undefined,
    next: undefined,
    nextLayer: undefined
  }

  this.map = new gm.Map(target, opts);
  if (geocoder === undefined) {
    geocoder = new gm.Geocoder();
  }

  this.editable = false;
};

RouteEditor.prototype = {}

RouteEditor.prototype.search = function(address) {
  var self = this;
  geocoder.geocode({address: address},
    function(results, status) {
      if (status == gm.GeocoderStatus.OK) {
        var g = results[0].geometry;
        if (g.viewport) {
          self.map.fitBounds(g.viewport);
        }
        else if (g.bounds) {
          self.map.fitBounds(g.bounds);
        }
        else {
          self.map.setCenter(g.location);
        }
      }
    }
  );
}

RouteEditor.prototype.setEditable = function(editable) {
  if (editable === true) {
    this.initEditor();
  }

  if (!editable) {
    if (this.path.nextLayer.getMap() === this.map) {
      this.map.nextLayer.setMap(null);
    }
  }

  this.editable = editable;
  this.path.layer.setEditable(editable);
}

RouteEditor.prototype.initEditor = function() {
  if (this.path.layer !== undefined) return;

  var self = this;
  var cancelClick = false;
  var path = this.path,
      map = this.map;

  // path
  var opts = {
    editable: false,
    draggable: false,
    strokeColor: '#ff0000',
    strokeOpacity: 0.9
  };
  path.layer = new gm.Polyline(opts);
  path.layer.setMap(map);

  path.data = path.layer.getPath();

  // next path: last point to the mouse position
  opts = {
    editable: false,
    draggable: false,
    strokeColor: '#0000ff',
    strokeOpacity: 0.5
  }
  path.nextLayer = new gm.Polyline(opts);

  path.next = path.nextLayer.getPath();
  path.next.push(map.getCenter());
  path.next.push(map.getCenter());

  // click on the map
  var startNewPoint = function(e) {
    if (path.data.getLength() >= 2) {
      var d1 = getDistance(e.latLng, path.data.getAt(0));
      var d2 = getDistance(e.latLng, path.data.getAt(path.data.getLength()-1));
      if (d2 > d1) {
        // reverse path
        var p = path.data.getArray().slice();
        for (var i=0, j=p.length-1; i<p.length; i++, j--) {
          path.data.setAt(i, p[j]);
        }
      }
    }

    path.data.push(e.latLng);

    path.next.setAt(0, e.latLng);
    path.next.setAt(1, e.latLng);

    if (path.nextLayer.getMap() !== map) {
      path.nextLayer.setMap(map);
    }
  }
  gm.event.addListener(map, 'click', function(e) {
    if (!self.editable) return;
    setTimeout(function() {
      if (!cancelClick)
        startNewPoint(e);
      cancelClick = false;
    }, 250);
  });

  gm.event.addListener(map, 'dblclick', function(e) {
    cancelClick = true;
  });

  // click on the next path
  gm.event.addListener(path.nextLayer, 'click', function(e) {
    path.next.setAt(0, e.latLng);
    path.data.push(e.latLng);
  });

  // double click to end path or remove data point
  gm.event.addListener(path.layer, 'dblclick', function(e) {
    if (!self.editable) return;
    if (path.nextLayer.getMap() === map) {
      if (e.vertex === path.data.getLength()-1) {
        path.nextLayer.setMap(null);
      }
    }
    else {
      path.data.removeAt(e.vertex);
    }
  });

  // mouse hovering the map
  gm.event.addListener(map, 'mousemove', function(e) {
    if (!self.editable) return;
    if (path.nextLayer.getMap() === map) {
      path.next.setAt(1, e.latLng);
    }
  });

  // if the latest point in the path is moved, update path.next[0] as well
  gm.event.addListener(path.data, 'set_at', function(pos) {
    if (pos === path.data.getLength()-1) {
      path.next.setAt(0, path.data.getAt(pos));
      path.next.setAt(1, path.data.getAt(pos));
    }
  });

  // escape button
  var removeLast = function() {
    if (path.nextLayer.getMap() === map) {
      path.nextLayer.setMap(null);
    }
    else {
      if (path.data.getLength() > 0) {
        path.data.removeAt(path.data.getLength() - 1);
      }
    }
  }
  $(document).keyup(function(e) {
    if (!self.editable) return;
    if (e.keyCode === 27) {
      removeLast();
    }
  });

  // path info
  var triggerPathUpdated = function() {
    self.triggerPathUpdated();
  }
  gm.event.addListener(path.data, 'insert_at', triggerPathUpdated);
  gm.event.addListener(path.data, 'set_at', triggerPathUpdated);
  gm.event.addListener(path.data, 'remove_at', triggerPathUpdated);
}

RouteEditor.prototype.triggerPathUpdated = function() {
  var handlers = this.pathUpdatedHandlers;
  var len = handlers.length;
  for (var i=0; i<len; i++) {
    var handler = handlers[i];
    handler();
  }
}

RouteEditor.prototype.pathUpdated = function(handler) {
  this.pathUpdatedHandlers.push(handler);
}

RouteEditor.prototype.getPathLength = function() {
  return gm.geometry.spherical.computeLength(this.path.data);
}

RouteEditor.prototype.setPath = function(path) {
  this.initEditor();

  var len = path.length;
  this.path.data.clear();
  for (var i=0; i<len; i++) {
    this.path.data.push(path[i]);
  }
}

return RouteEditor;

})();

