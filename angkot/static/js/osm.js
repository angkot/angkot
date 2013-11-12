L.OSMDataLayer = L.Class.extend({
	includes: L.Mixin.Events,

	options: {
		minZoom: 16,
		maxZoom: 19,
		tileSize: 256,
		zoomOffset: 0,
	},

	initialize: function(url, options) {
		options = L.setOptions(this, options);
		this._url = url;
		this._osmNodes = {};

		this._data = {};
		this._nodeUsage = {};
		this._nodeLatLng = {};
		this._wayUsage = {};
		this._wayNodes = {};
		this._wayHighway = {};
		this._visible = {};
		this._visibleWayUsage = {};
	},

	onAdd: function(map) {
		this._map = map;

		this._initContainer();
		if (this._container) {
			this._map._pathRoot.appendChild(this._container);
		}

		map.on({
			'viewreset': this._reset,
			'moveend': this._update
		}, this);

		this._reset();
		this._update();
	},

	addTo: function(map) {
		map.addLayer(this);
		return this;
	},

	onRemove: function(map) {
		this._container.parentNode.removeChild(this._container);

		map.off({
			'viewreset': this._reset,
			'moveend': this._update
		}, this);

		map._pathRoot.removeChild(this._container);
		this._map = null;
	},

	_createElement: function(name) {
		return document.createElementNS(L.Path.SVG_NS, name);
	},

	_initContainer: function() {
		if (!this._container) {
			this._map._initPathRoot();
			this._container = this._createElement('g');
		}
	},

	_reset: function(e) {
		this._tiles = {};
		this._tilesToLoad = 0;
	},

	_update: function() {
		if (!this._map) return;

		var bounds = this._map.getPixelBounds(),
		    zoom = this._map.getZoom(),
		    tileSize = this.options.tileSize;

		if (zoom > this.options.maxZoom || zoom < this.options.minZoom) {
			return;
		}

		var tileBounds = L.bounds(
		        bounds.min.divideBy(tileSize)._floor(),
		        bounds.max.divideBy(tileSize)._floor());

		this._addTilesFromCenterOut(tileBounds);
		this._removeOtherTiles(tileBounds);
	},

	_addTilesFromCenterOut: function(bounds) {
		var queue = [],
		    center = bounds.getCenter();

		var j, i, point;

		for (j=bounds.min.y; j<=bounds.max.y; j++) {
			for (i=bounds.min.x; i<=bounds.max.x; i++) {
				point = new L.Point(i, j);
				if (this._tileShouldBeLoaded(point)) {
					queue.push(point);
				}
			}
		}

		var tilesToLoad = queue.length;
		if (tilesToLoad === 0) return;

		queue.sort(function(a, b) {
			return a.distanceTo(center) - b.distanceTo(center);
		});

		this.t_tilesToLoad += tilesToLoad;

		for (i=0; i<tilesToLoad; i++) {
			this._addTile(queue[i]);
		}
	},

	_tileShouldBeLoaded: function(tilePoint) {
		if ((tilePoint.x + ':' + tilePoint.y) in this._tiles) {
			return false; // already loaded
		}

		return true;
	},

	_removeOtherTiles: function(bounds) {
		var kArr, x, y, key;

		for (key in this._tiles) {
			kArr = key.split(':');
			x = parseInt(kArr[0], 10);
			y = parseInt(kArr[1], 10);

			// remove tile if it's out of bounds
			if (x < bounds.min.x || x > bounds.max.x || y < bounds.min.y || y > bounds.max.y) {
				this._removeTile(key);
			}
		}
	},

	_removeTile: function(key) {

	},

	_addTile: function(tilePoint) {
		tilePoint.z = this._getZoomForUrl();
		var url = this.getTileUrl(tilePoint);
		this._tiles[tilePoint.x + ':' + tilePoint.y] = url;
		this._loadTile(tilePoint, url);
	},

	_getTilePos: function (tilePoint) {
		var origin = this._map.getPixelOrigin(),
		    tileSize = this.options.tileSize;

		return tilePoint.multiplyBy(tileSize).subtract(origin);
	},

	getTileUrl: function (tilePoint) {
		return L.Util.template(this._url, L.extend({
			z: tilePoint.z,
			x: tilePoint.x,
			y: tilePoint.y
		}, this.options));
	},

	_getZoomForUrl: function () {
		var options = this.options,
		    zoom = this._map.getZoom();

		if (options.zoomReverse) {
			zoom = options.maxZoom - zoom;
		}

		return zoom + options.zoomOffset;
	},

	_loadTile: function(tilePoint, url) {
		var key = tilePoint.x + ':' + tilePoint.y;

		var self = this;
		this._ajax({url: url, dataType: 'json'},
			function(data, status) {
				self._storeOSMData.call(self, tilePoint, data);
				self._showOSMData.call(self, tilePoint);
			})
	},

	_ajax: function(options, success, error) {
		success = success || function() {};
		error = error || function() {};

		var xhr = new XMLHttpRequest();
		xhr.onreadystatechange = function() {
			if (xhr.readyState === 4) {
				if (xhr.status === 200) {
					var response = xhr.responseText;
					if (options.dataType && options.dataType === 'json') {
						response = JSON.parse(response);
					}
					success(response, xhr.status);
				}
				else {
					error(xhr.responseText, xhr.status);
				}
			}
		}
		xhr.open('GET', options.url);
		xhr.send();
	},

	_storeOSMData: function(tilePoint, data) {
		var key = tilePoint.x + ':' + tilePoint.y;
		this._data[key] = data;

		var ids = data.nodes.ids,
		    latlngs = data.nodes.latlngs,
		    len = ids.length;
		for (var i=0; i<len; i++) {
			var id = ids[i];
			this._nodeUsage[id] = this._nodeUsage[id] || {};
			if (!this._nodeLatLng[id]) {
				this._nodeLatLng[id] = L.latLng(latlngs[i][0], latlngs[i][1]);
			}
			this._nodeUsage[id][key] = true;
		}

		for (sid in data.segments) {
			var nodes = data.segments[sid];
			this._wayUsage[sid] = this._wayUsage[sid] || {};
			if (!this._wayNodes[sid]) {
				this._wayNodes[sid] = nodes;
				this._wayHighway[sid] = data.segments_highway[sid];
			}
			this._wayUsage[sid][key] = true;
		}
	},

	_showOSMData: function(tilePoint) {
		var key = tilePoint.x + ':' + tilePoint.y;
		if (this._visible[key]) return;

		this._showOSMSegment(tilePoint);

		this._visible[key] = true;
	},

	_showOSMSegment: function(tilePoint) {
		var key = tilePoint.x + ':' + tilePoint.y;
		var data = this._data[key],
		    segments = data.segments;
		for (sid in segments) {
			if (this._visibleWayUsage[sid]) continue;

			var nodes = segments[sid],
			    len = nodes.length;

			var str = '';
			for (var i=0; i<len; i++) {
				var node = nodes[i];
				var latlng = this._nodeLatLng[node];
				var p = this._map.latLngToLayerPoint(latlng);
				str += (i ? 'L' : 'M') + p.x + ' ' + p.y + ' ';
			}

			var path = this._createElement('path');
			path.setAttribute('d', str);
			path.setAttribute('fill', 'none');
			path.setAttribute('stroke-width', '2');
			path.setAttribute('stroke', 'red');
			this._container.appendChild(path);

			this._visibleWayUsage[sid] = (this._visibleWayUsage[sid] || 0) + 1;
		}
	},

	_loadOSMNodes: function(data) {
		var ids = data.nodes.ids,
		    latlngs = data.nodes.latlngs,
		    len = ids.length;

		for (var i=0; i<len; i++) {
			var id = ids[i],
			    latlng = latlngs[i];

			if (this._osmNodes[id]) continue;
			this._osmNodes[id] = (this._osmNodes[id] || 0) + 1;

			var circle = this._createCircle(latlng);
			circle.setAttribute('class', 'osm-nodes project');
			circle.setAttribute('r', '2');
			circle.setAttribute('id', 'osm-nodes-' + id);
			this._container.appendChild(circle);
		}

		this._updateProjections();
	},

	_createCircle: function(latlng) {
		var el = this._createElement('circle');
		el.setAttribute('data-lat', latlng[0]);
		el.setAttribute('data-lng', latlng[1]);
		return el;
	},

	_updateProjections: function() {
		var els = this._container.querySelectorAll('circle.project'),
		    len = els.length;

		var p = [];
		for (var i=0; i<els.length; i++) {
			var el = els[i];
			var latlng = L.latLng(parseFloat(el.getAttribute('data-lat')),
			                      parseFloat(el.getAttribute('data-lng')));
			var point = this._map.latLngToLayerPoint(latlng);
			p.push(point);
		}

		for (var i=0; i<els.length; i++) {
			var el = els[i],
			    point = p[i];
			el.setAttribute('cx', point.x);
			el.setAttribute('cy', point.y);
		}
	}
});

