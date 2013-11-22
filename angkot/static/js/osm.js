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

        this._redrawDelayed = L.Util.limitExecByInterval(this._redraw, 10, this);
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

        this._data = {};

        this._tileUrl = {};

        while (this._container.lastChild) {
            this._container.removeChild(this._container.lastChild);
        }
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
        this._bounds = tileBounds;

        this._redrawDelayed();
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
        if ((tilePoint.x + ':' + tilePoint.y) in this._data) {
            return false; // already loaded
        }

        return true;
    },

    _removeOtherTiles: function(bounds) {
        var kArr, x, y, key;

        for (key in this._data) {
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
        delete this._data[key];
    },

    _addTile: function(tilePoint) {
        tilePoint.z = this._getZoomForUrl();
        var key = tilePoint.x + ':' + tilePoint.y;

        if (!this._data[key]) {
            var url = this.getTileUrl(tilePoint);
            this._tileUrl[key] = url;
            this._loadTile(tilePoint, url);
        }
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
                self._storeTile.call(self, tilePoint, data);
                self._redrawDelayed.call(self);
            });
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
        };
        xhr.open('GET', options.url);
        xhr.send();
    },

    _storeTile: function(tilePoint, data) {
        var key = tilePoint.x + ':' + tilePoint.y;
        this._data[key] = data;
    },

    _redraw: function() {
        var bounds = this._bounds,
            x1 = bounds.min.x,
            y1 = bounds.min.y,
            x2 = bounds.max.x,
            y2 = bounds.max.y;
        var key, len, id, i;

        var q = [];
        for (var x=x1; x<=x2; x++) {
            for (var y=y1; y<=y2; y++) {
                key = x + ':' + y;
                if (!this._data[key]) continue;
                q.push(key);
            }
        }

        // collect nodes and segments
        var nodes = {},
            pos = {},
            segments = {};
        for (i in q) {
            key = q[i];
            var data = this._data[key],
                ids = data.nodes.ids,
                latlngs = data.nodes.latlngs,
                segmentList = data.segments;
            len = ids.length;
            for (var j=0; j<len; j++) {
                id = ids[j];
                if (nodes[id]) continue;

                var latlng = latlngs[j];
                nodes[id] = L.latLng(latlng[0], latlng[1]);
                pos[id] = this._map.latLngToLayerPoint(nodes[id]);
            }

            for (id in segmentList) {
                if (segments[id]) continue;
                segments[id] = segmentList[id];
            }
        }

        // get existing segments
        var paths = {},
            used = {};
        for (i=0; i<this._container.childElementCount; i++) {
            var ch = this._container.childNodes[i];
            var segmentId = ch.getAttribute('data-segment-id');
            if (segmentId !== null) {
                paths[segmentId] = ch;
                used[segmentId] = false;
            }
        }

        // add new segments
        for (id in segments) {
            if (paths[id]) {
                used[id] = true;
                continue;
            }

            var segment = segments[id];
            len = segment.length;

            var str = '';
            for (i=0; i<len; i++) {
                var nodeId = segment[i],
                    p = pos[nodeId];
                str += (i ? 'L' : 'M') + p.x + ' '  + p.y + ' ';
            }

            var path = this._createElement('path');
            path.setAttribute('d', str);
            path.setAttribute('class', 'way segment');
            path.setAttribute('data-segment-id', id);
            this._container.appendChild(path);
        }

        // remove unused segments
        for (id in used) {
            if (used[id]) continue;
            paths[id].remove();
        }
    },
});
