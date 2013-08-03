L.Angkot.Route = L.LayerGroup.extend({
  options: {
    editable: false,
  },

  includes: L.Mixin.Events,

  initialize: function(layers, options) {
    L.LayerGroup.prototype.initialize.call(this, layers);
    L.Util.setOptions(this, options);

    this._polylines = [];
    this._active = null;
    this._guide = new L.Polyline.Color([], {
      color: 'blue',
      weight: 2,
      opacity: 0.5,
    });
    this._shiftKey = false;

    this._tooltip = new L.Tooltip();
    this._distance = 0;
  },

  onAdd: function(map) {
    L.LayerGroup.prototype.onAdd.apply(this, arguments);

    if (this.options.editable) {
      this._setupEvents();
      this._guide.addTo(map);
    }

    this._tooltip.addTo(map);
  },

  onRemove: function(map) {
    map.removeLayer(this._tooltip);
    L.LayerGroup.prototype.onRemove.apply(this, arguments);
  },

  setEditable: function(editable) {
    this.options.editable = editable;
    if (editable) this._setupEvents();
    else this._removeEvents();

    // FIXME restructure
    if (this._map) {
      if (editable) this._guide.addTo(this._map);
      else this._map.removeLayer(this._guide);
    }
  },

  getRoutes: function() {
    var routes = [];
    for (var i=0; i<this._polylines.length; i++) {
      routes.push(this._polylines[i].getLatLngs());
    }
    return routes;
  },

  setRoutes: function(routes) {
    this.clear();
    for (var i=0; i<routes.length; i++) {
      var route = routes[i];
      var p = this._addPolyline({color:'red'});
      p.addLatLngs(route);
    }
  },

  clear: function() {
    while (this._polylines.length > 0) {
      this._removePolyline(this._polylines[0]);
    }
  },

  _setupEvents: function() {
    if (!this._map) return;

    this._map.on('click', this._onMapClick, this);
    this._map.on('mousemove', this._onMapMouseMove, this);
    this._map.on('mouseover', this._onMapMouseOver, this);
    this._map.on('mouseout', this._onMapMouseOut, this);

    L.DomEvent.addListener(document, 'keydown', function(e) {
      this._shiftKey = e.shiftKey;
    }, this);
    L.DomEvent.addListener(document, 'keyup', function(e) {
      this._shiftKey = e.shiftKey;
    }, this);
  },

  _removeEvents: function() {
    if (!this._map) return;

    this._map.off('click', this._onMapClick, this);
    this._map.off('mouseout', this._onMapMouseOut, this);
    this._map.off('mousemove', this._onMapMouseMove, this);
    this._map.off('mouseover', this._onMapMouseOver, this);
  },

  _onMapClick: function(e) {
    if (this._active) {
      this._addNextPoint(e);
    }
    else {
      this._startRoute(e);
    }
  },

  _startRoute: function(e) {
    var p = this._addPolyline({color:'blue'});
    p.addLatLng(e.latlng);
    this._active = p;

    this._guide.spliceLatLngs(0, this._guide._latlngs.length);
    this._guide.addLatLng(e.latlng);
    this._guide.addLatLng(e.latlng);

    this._distance = 0;
    this._drawMode = 'new';

    if (this._polylines.length == 1) {
      this._tooltip.setContent('Lanjutkan dengan mengklik titik-titik di sepanjang rute');
    }
  },

  _addNextPoint: function(e) {
    this._active.addLatLng(e.latlng);
    this._guide.spliceLatLngs(0, 1, e.latlng);

    if (this._active._latlngs.length > 1) {
      var last = this._active._latlngs.length-1;
      this._distance += this._active._latlngs[last-1].distanceTo(this._active._latlngs[last]);
    }

    if (this._polylines.length == 1) {
      var len = this._polylines[0]._latlngs.length;
      if (len == 2) {
        this._tooltip.setContent('Klik titik terakhir untuk mengakhiri');
      }
      else if (len == 3) {
        this._tooltip.setContent(null);
      }
    }
  },

  _onMapMouseOver: function(e) {
    if (this._polylines.length == 0) {
      this._tooltip.setContent('Klik untuk membuat rute');
    }
  },

  _onMapMouseOut: function(e) {
    this._tooltip.clear();
  },

  _onMapMouseMove: function(e) {
    if (this._active) {
      this._guide.spliceLatLngs(1, 1, e.latlng);

      var last = this._active._latlngs.length-1;
      var distance = this._active._latlngs[last].distanceTo(e.latlng);
      distance += this._distance;
      this._showDistance(distance);
    }

    this._tooltip.setLatLng(e.latlng);
  },

  _showDistance: function(distance) {
    var text = (Math.round(distance/1000*100)/100) + ' km';
    if (distance < 1500) text = (Math.round(distance*100)/100) + ' m';
    this._tooltip.setTitle(text);
  },

  _createPolyline: function(options) {
    var opts = {
      editable: this.options.editable,
      color: 'red',
      weight: 3,
      opacity: 0.8,
    };
    for (k in options) {
      opts[k] = options[k];
    }

    var p = new L.Polyline.Editable([], opts);
    return p;
  },

  _addPolyline: function(options) {
    var p = this._createPolyline(options);
    p.addTo(this._map);
    p.on('handle:click', this._onHandleClick, this);
    p.on('handle:mouseover', this._onHandleMouseOver, this);
    p.on('handle:mouseout', this._onHandleMouseOut, this);
    p.on('handle:dragend', this._onHandleDragEnd, this);
    this._polylines.push(p);
    return p;
  },

  _removePolyline: function(p) {
    var index = this._polylines.indexOf(p);
    if (index >= 0) this._polylines.splice(index, 1);

    p.off('handle:mouseover', this._onHandleMouseOver, this);
    p.off('handle:mouseout', this._onHandleMouseOut, this);
    p.off('handle:click', this._onHandleClick, this);
    p.off('handle:dragend', this._onHandleDragEnd, this);
    if (this._map) this._map.removeLayer(p);
  },

  _stopDrawing: function() {
    var index = this._polylines.indexOf(this._active);

    this._active.setColor('red');
    this._active = null;
    this._guide.spliceLatLngs(0, this._guide._latlngs.length);

    this._distance = 0;

    this._tooltip.clear();

    if (index >= 0) {
      if (this._drawMode == 'new') {
        this.fire('route:add', {index:index});
      }
      else if (this._drawMode == 'continue') {
        this.fire('route:update', {index:index});
      }
    }

    this._drawMode = null;
  },

  _continueRoute: function(e) {
    var p = e.target;
    if (e.vertex === 0) {
      p.reverseLatLngs();
    }
    this._active = p;
    this._active.setColor('blue');
    this._guide.addLatLng(e.latlng);
    this._guide.addLatLng(e.latlng);

    var latlngs = this._active._latlngs;
    var distance = 0;
    for (var i=1; i<latlngs.length; i++) {
      distance += latlngs[i-1].distanceTo(latlngs[i]);
    }
    this._distance = distance;

    this._drawMode = 'continue';

    this._showDistance(distance);
    this._tooltip.setContent(null);
  },

  _mergeRoute: function(e) {
    var p = e.target;
    if (e.vertex !== 0) {
      p.reverseLatLngs();
    }
    this._active.addLatLngs(p._latlngs);

    var index = this._polylines.indexOf(p);
    this.fire('route:delete', {index:index});

    this._removePolyline(p);
  },

  _removeVertex: function(e) {
    var p = e.target;
    p.spliceLatLngs(e.vertex, 1);

    var index = this._polylines.indexOf(p);

    if (p._latlngs.length === 1) {
      this._removePolyline(p);
      this.fire('route:delete', {index:index});
    }
    else {
      this.fire('route:update', {index:index});
    }
  },

  _onHandleMouseOver: function(e) {
    var p = e.target;
    var length = p._latlngs.length;
    var head = e.vertex === 0;
    var tail = e.vertex === length - 1;
    var tip = head || tail;
    var onVertex = e.vertex !== undefined;

    if (!this._active) {
      if (tip) {
        this._tooltip.setContent('Klik untuk melanjutkan rute');
      }
      else if (onVertex) {
        this._tooltip.setContent('Untuk menghapus titik, tahan tombol <kbd>shift</kbd> lalu klik titik yang mau dihapus');
      }
    }
    else if (p !== this._active) {
      if (tip) {
        this._tooltip.setContent('Untuk menggabung rute, tahan tombol <kbd>shift</kbd> lalu klik titik tujuan');
      }
    }
  },

  _onHandleMouseOut: function(e) {
    if (!this._active || this._polylines.length > 1) {
      this._tooltip.setContent(null);
    }
  },

  _onHandleClick: function(e) {
    var p = e.target;
    var length = p._latlngs.length;
    var head = e.vertex === 0;
    var tail = e.vertex === length - 1;
    var tip = head || tail;

    if (e.target == this._active) {
      if (tail) {
        if (length === 1) {
          this._removePolyline(p);
        }
        this._stopDrawing();
      }
      else {
        this._addNextPoint(e);
      }
    }
    else if (!this._active && this._shiftKey && e.vertex !== undefined) {
      this._removeVertex(e);
    }
    else if (tip) {
      if (!this._active) {
        this._continueRoute(e);
      }
      else if (this._active && this._shiftKey) {
        this._mergeRoute(e);
        this._stopDrawing();
      }
      else if (this._active) {
        this._addNextPoint(e);
      }
    }
    else if (!this._active) {
      this._startRoute(e);
    }
    else {
      this._addNextPoint(e);
    }
  },

  _onHandleDragEnd: function(e) {
    var p = e.target;
    if (p == this._active) return;
    var index = this._polylines.indexOf(p);
    this.fire('route:update', {index:index});
  },

});

