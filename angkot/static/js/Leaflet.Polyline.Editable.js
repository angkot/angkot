L.Marker.Handle = L.Marker.extend({
  options: {
    color: 'red',
    draggable: true,
    type: 'vector',
  },

  initialize: function(pos, options) {
    L.Marker.prototype.initialize.call(this, pos, options);
    L.Util.setOptions(this, options);

    var type = options.type;
    var icon = L.divIcon({
      className: 'leaflet-polyline-editable-handle leaflet-polyline-editable-handle-' + type,
      iconSize: new L.Point(10, 10),
    });
    this.options.icon = icon;
  },

  onAdd: function(map) {
    L.Marker.prototype.onAdd.apply(this, arguments);
    this._icon.style.borderColor = this.options.color;
  },

  setColor: function(color) {
    this.options.color = color;
    if (this._icon) {
      this._icon.style.borderColor = this.options.color;
    }
  },
});

L.Polyline.Color = L.Polyline.extend({
  setColor: function(color) {
    this.options.color = color;
    this._updateStyle();
  },
});

L.Polyline.Editable = L.Polyline.Color.extend({
  options: {
    editable: false,
  },

  initialize: function(path, options) {
    L.Polyline.Color.prototype.initialize.call(this, path, options);
    L.Util.setOptions(this, options);

    this._handles = [];
    this._handleGroup = new L.LayerGroup();

    var opacity = Math.max(this.options.opacity/2.0, 0.4);
    this._shadow = new L.Polyline.Color([], {
      opacity: opacity,
      weight: this.options.weight,
      color: this.options.color,
    });

    this._resetHandles();
  },

  onAdd: function(map) {
    L.Polyline.Color.prototype.onAdd.apply(this, arguments);

    this._updateHandlePositions(map);
    if (this.options.editable) {
      this._shadow.addTo(map);
      this._handleGroup.addTo(map);
    }
  },

  onRemove: function(map) {
    L.Polyline.Color.prototype.onRemove.apply(this, arguments);

    map.removeLayer(this._handleGroup);
    map.removeLayer(this._shadow);
  },

  setColor: function(color) {
    L.Polyline.Color.prototype.setColor.apply(this, arguments);
    for (var i=0; i<this._handles.length; i++) {
      this._handles[i].setColor(color);
    }
    this._shadow.setColor(color);
  },

  addLatLng: function(latlng) {
    L.Polyline.Color.prototype.addLatLng.apply(this, arguments);
    if (this.options.editable) this._addHandle(latlng);
  },

  addLatLngs: function(latlngs) {
    for (var i=0; i<latlngs.length; i++) {
      this._latlngs.push(latlngs[i]);
    }
    this.redraw();
    this._resetHandles();
  },

  spliceLatLngs: function() {
    L.Polyline.Color.prototype.spliceLatLngs.apply(this, arguments);
    this._resetHandles();
  },

  reverseLatLngs: function() {
    this._latlngs.reverse();
    this._resetHandles();
  },

  setEditable: function(editable) {
    this.options.editable = editable;
    if (this._map) {
      if (editable) {
        this._shadow.addTo(this._map);
        this._handleGroup.addTo(this._map);
      }
      else {
        this._map.removeLayer(this._shadow);
        this._map.removeLayer(this._handleGroup);
      }
    }
    this._resetHandles();
  },

  _resetHandles: function() {
    for (var i=0; i<this._handles.length; i++) {
      this._handleGroup.removeLayer(this._handles[i]);
    }
    this._handles.splice(0, this._handles.length);

    if (!this.options.editable) return;

    for (var i=0; i<this._latlngs.length; i++) {
      this._addHandle(this._latlngs[i]);
    }
  },

  _addHandle: function(latlng) {
    var edge, vertex;
    if (this._handles.length > 0) {
      var edge = this._createHandle('edge');
      edge.addTo(this._handleGroup);
      this._handles.push(edge);
    }

    var vertex = this._createHandle('vertex');
    vertex.addTo(this._handleGroup);
    this._handles.push(vertex);

    if (this._map) {
      if (edge) {
        this._updateEdgeHandlePosition(edge);
      }
      vertex.setLatLng(latlng);
    }
  },

  _updateEdgeHandlePosition: function(h) {
    var index = this._handles.indexOf(h);
    if (!this._map || index<0) return;

    var prev = this._latlngs[parseInt(index/2)];
    var next = this._latlngs[parseInt(index/2)+1];
    var mid = this._getMidLatLng(this._map, prev, next);
    h.setLatLng(mid);
  },

  _createHandle: function(type) {
    var opts = {
      type: type,
      color: this.options.color,
    }

    var handle = new L.Marker.Handle([0,0], opts);

    handle.on('dragstart', this._onHandleDragStart, this);
    handle.on('drag', this._onHandleDrag, this);
    handle.on('dragend', this._onHandleDragEnd, this);

    handle.on('mouseover', this._onHandleMouseEvent, this);
    handle.on('mouseout', this._onHandleMouseEvent, this);
    handle.on('click', this._onHandleMouseEvent, this);

    return handle;
  },

  _updateHandlePositions: function(map) {
    for (var i=0; i<this._handles.length; i++) {
      var h = this._handles[i];
      if (h.options.type === 'vertex') {
        h.setLatLng(this._latlngs[parseInt(i/2)]);
      }
      else {
        var prev = this._latlngs[parseInt(i/2)];
        var next = this._latlngs[parseInt(i/2)+1];
        var mid = this._getMidLatLng(map, prev, next);
        h.setLatLng(mid);
      }
    }
  },

  _getMidLatLng: function(map, a, b) {
    var aa = map.latLngToLayerPoint(a);
    var bb = map.latLngToLayerPoint(b);
    return map.layerPointToLatLng(aa._add(bb)._divideBy(2));
  },

  _onHandleDragStart: function(e) {
    var h = e.target;

    var d = 2;
    if (h.options.type === 'edge') d = 1;

    var p = [];
    var index = this._handles.indexOf(h);
    if (index > 0) {
      p.push(this._handles[index-d]._latlng);
    }
    if (index < this._handles.length-1) {
      p.push(this._handles[index+d]._latlng);
    }
    p.splice(1, 0, h._latlng);

    this._shadow.setLatLngs(p);
  },

  _onHandleDrag: function(e) {
    this._shadow.spliceLatLngs(1, 1, e.target._latlng);
  },

  _onHandleDragEnd: function(e) {
    this._shadow.setLatLngs([]);

    var h = e.target;
    var index = this._handles.indexOf(h);

    if (h.options.type === 'vertex') {
      this._latlngs.splice(parseInt(index/2), 1, h._latlng);
      this._updateEdgeHandlePosition(this._handles[index-1]);
      this._updateEdgeHandlePosition(this._handles[index+1]);
      this.redraw();
    }
    else {
      this._latlngs.splice(parseInt(index/2)+1, 0, h._latlng);
      h.options.type = 'vertex';
      h._icon.className = h._icon.className.replace('leaflet-polyline-editable-handle-edge', 'leaflet-polyline-editable-handle-vertex');

      var left = this._createHandle('edge');
      var right = this._createHandle('edge');

      this._handles.splice(index+1, 0, right);
      this._handles.splice(index, 0, left);

      if (this._map) {
        left.addTo(this._handleGroup);
        right.addTo(this._handleGroup);
        this._updateEdgeHandlePosition(left);
        this._updateEdgeHandlePosition(right);
      }
      this.redraw();
    }
  },

  _onHandleMouseEvent: function(e) {
    var h = e.target;

    var index = parseInt(this._handles.indexOf(h)/2);
    if (h.options.type === 'vertex') {
      e.vertex = index;
    }
    else {
      e.edge = index;
    }

    this.fire('handle:' + e.type, e);
  },

});

