L.Marker.Handle = L.Marker.extend({
  options: {
    type: 'vertex',
  },

  initialize: function(latlng, options) {
    L.Marker.prototype.initialize.call(this, latlng, options);
    L.Util.setOptions(this, options);

    this._polyline = undefined;
    this._index = 0;

    this.on('dragstart', this._onDragStart, this);
    this.on('drag', this._onDrag, this);
    this.on('dragend', this._onDragEnd, this);

    this.on('mouseover', this._onMouseEvent, this);
    this.on('mouseout', this._onMouseEvent, this);
    this.on('click', this._onMouseEvent, this);
  },

  onAdd: function() {
    L.Marker.prototype.onAdd.apply(this, arguments);
    this.fire('add');
  },

  setPolyline: function(polyline) {
    this._polyline = polyline;
  },

  onAdd: function(map) {
    L.Marker.prototype.onAdd.apply(this, arguments);

    if (!this._polyline) return;

    if (this.options.type === 'vertex') {
      var index = this._polyline._handles.indexOf(this);
      var pos = this._polyline._latlngs[index];
      this.setLatLng(pos);
    }
    else {
      var index = this._polyline._mids.indexOf(this);
      var left = this._polyline._latlngs[index];
      var right = this._polyline._latlngs[index+1];
      var mid = this._getMidLatLng(left, right);
      this.setLatLng(mid);
    }
  },

  _getMidLatLng: function(a, b) {
    var aa = this._map.latLngToLayerPoint(a);
    var bb = this._map.latLngToLayerPoint(b);
    return this._map.layerPointToLatLng(aa._add(bb)._divideBy(2));
  },

  _onDragStart: function(e) {
    if (this.options.type === 'edge') {
      var index = this._polyline._mids.indexOf(this);
      this._polyline._handles.splice(index+1, 0, this);
      this.options.type = 'vertex';
      var className = this._icon.className;
      this._icon.className = className.replace('leaflet-angkot-handle-edge', 'leaflet-angkot-handle-vertex');

      var left = L.Polyline.Editable.handle(this._polyline, 'edge');
      var right = L.Polyline.Editable.handle(this._polyline, 'edge');
      this._polyline._mids.splice(index, 1, left, right);
      this._polyline._latlngs.splice(index+1, 0, e.target._latlng);

      left.addTo(this._map);
      right.addTo(this._map);
    }

    this._index = this._polyline._handles.indexOf(this);
    this._hasLeftEdge = this._index > 0;
    this._hasRightEdge = this._index < this._polyline._handles.length-1;
  },

  _onDrag: function(e) {
    var latlng = e.target._latlng;
    this._polyline._latlngs[this._index] = latlng;
    this._polyline.redraw();

    if (this._hasLeftEdge) {
      var left = this._polyline._latlngs[this._index-1];
      var mid = this._getMidLatLng(left, latlng);
      this._polyline._mids[this._index-1].setLatLng(mid);
    }
    if (this._hasRightEdge) {
      var right = this._polyline._latlngs[this._index+1];
      var mid = this._getMidLatLng(latlng, right);
      this._polyline._mids[this._index].setLatLng(mid);
    }
  },

  _onDragEnd: function(e) {
  },

  _onMouseEvent: function(e) {
    if (!this._polyline) return;

    if (this.options.type === 'vertex') {
      e.vertex = this._polyline._handles.indexOf(this);
    }
    else if (this.options.type === 'edge') {
      e.edge = this._polyline._mids.indexOf(this);
    }

    this._polyline.fire('handle:' + e.type, e);
  },
});

L.Polyline.Editable = L.Polyline.extend({
  options: {
    editable: false,
  },

  initialize: function(path, options) {
    L.Polyline.prototype.initialize.call(this, path, options);
    L.Util.setOptions(this, options);

    this._handles = [];
    this._mids = [];
    this._resetHandles();
  },

  setEditable: function(editable) {
    this.options.editable = editable;
    this._resetHandles();
  },

  addLatLng: function(latlng) {
    L.Polyline.prototype.addLatLng.apply(this, arguments);
    this._resetHandles(); // FIXME
  },

  spliceLatLngs: function() {
    L.Polyline.prototype.spliceLatLngs.apply(this, arguments);
    this._resetHandles(); // FIXME
  },

  onAdd: function(map) {
    L.Polyline.prototype.onAdd.apply(this, arguments);
    this._resetHandles(); // FIXME
  },

  onRemove: function(map) {
    L.Polyline.prototype.onRemove.apply(this, arguments);
    this._resetHandles(); // FIXME
  },

  _resetHandles: function() {
    if (this._map) {
      for (var i=0; i<this._handles.length; i++) {
        this._map.removeLayer(this._handles[i]);
      }
      for (var i=0; i<this._mids.length; i++) {
        this._map.removeLayer(this._mids[i]);
      }
    }

    this._handles.splice(0, this._handles.length);
    this._mids.splice(0, this._mids.length);

    if (!this.options.editable) return;

    var len = this._latlngs.length;
    var prev = undefined;
    for (var i=0; i<len; i++) {
      var latlng = this._latlngs[i];

      if (prev) {
        var h = L.Polyline.Editable.handle(this, 'edge');
        this._mids.push(h);
      }

      var h = L.Polyline.Editable.handle(this, 'vertex');
      this._handles.push(h);

      prev = latlng;
    }

    if (this._map) {
      for (var i=0; i<this._handles.length; i++) {
        this._handles[i].addTo(this._map);
      }
      for (var i=0; i<this._mids.length; i++) {
        this._mids[i].addTo(this._map);
      }
    }
  },

});

L.Polyline.Editable.handle = function(polyline, type) {
  var icon = L.divIcon({
    className: 'leaflet-angkot-handle leaflet-angkot-handle-' + type,
    iconSize: new L.Point(10, 10),
  });
  var opts = {
    draggable: true,
    icon: icon,
    type: type,
  }

  var m = new L.Marker.Handle([0,0], opts);
  m.setPolyline(polyline);

  return m;
};

