(function(window) {

"use strict";

var app = angular.module('angkot-route-drawing', []);

app.factory('MapService', function() {
  var data = {
    map: undefined,
    routes: undefined,
    layers: {},
    visible: {},
  };

  var clearRoutes = function() {
    for (var i in data.layers) {
      var layer = data.layers[i];
      data.map.removeLayer(layer);
    }
    data.layers = {};
    data.visible = {};
  }

  var showRoute = function(index) {
    if (!data.routes[index]) return;
    if (data.visible[index]) return;

    if (!data.layers[index]) {
      var latlngs = [],
          route = data.routes[index],
          len = route.length;

      // Swap (x, y) -> (lat, lng)
      for (var i=0; i<len; i++) {
        latlngs.push(L.latLng(route[i][1], route[i][0]));
      }
      console.log(latlngs.length);
      var layer = L.polyline(latlngs, {color: '#F8F', opacity: 0.9, weight: 3});
      data.layers[index] = layer;
    }

    data.layers[index].addTo(data.map);
    data.map.fitBounds(data.layers[index].getBounds());
    data.visible[index] = true;
  }

  var hideRoute = function(index) {
    if (!data.routes[index]) return;
    if (!data.visible[index]) return;
    if (!data.layers[index]) return;

    data.map.removeLayer(data.layers[index]);
    data.visible[index] = false;
  }

  return {
    setRoutes: function(routes) {
      if (!data.map) data.map = window.map; // FIXME
      clearRoutes();
      data.routes = routes;
    },

    showRoute: function(index) {
      showRoute(index);
    },

    hideRoute: function(index) {
      hideRoute(index);
    },
  }
});

app.controller('EditorController', ['$scope', '$http', function($scope, $http) {

  $scope.data = {};

  $scope.routeList = {};

  $scope.init = function() {
    $http.get('/route/transportation-list.json')
      .success(function(data) {
        $scope.raw = data;
        $scope.provinces = data.provinces;

        var names = {};
        angular.forEach(data.provinces, function(item) {
          this[item[0]] = item[1];
        }, names);
        $scope.provinceNames = names;
      });
  }

  $scope.setActiveSubmission = function(id) {
    if (!$scope.data[id]) {
      $scope.loadSubmission(id);
    }
    else {
      $scope.showSubmission(id);
    }
  }

  $scope.loadSubmission = function(id) {
    var url = '/route/transportation/' + id + '.json';
    $http.get(url)
      .success(function(data) {
        console.log(id, data);
        $scope.data[id] = data;
        $scope.showSubmission(id);
      });
  }

  $scope.showSubmission = function(id) {
    $scope.activeSubmission = $scope.data[id];
  }

}]);

app.controller('SubmissionController', ['$scope', 'MapService', function($scope, MapService) {

  $scope.visible = {};

  $scope.$watch('activeSubmission', function() {
    if (!$scope.activeSubmission) return;

    var s = $scope.activeSubmission,
        g = s.geojson;
    $scope.geojson = g;
    $scope.meta = g.properties;
    $scope.paths = g.geometry.coordinates;
    $scope.visible = {};

    MapService.setRoutes($scope.paths);
  });

  $scope.$watch('visible', function(a, b) {
    var keys = {};
    for (var k in a) { keys[k] = k; }
    for (var k in b) { keys[k] = k; }
    for (var k in keys) {
      if (a[k] && b[k]) continue;
      if (!a[k] && !b[k]) continue;
      if (a[k] && !b[k]) MapService.showRoute(k);
      else MapService.hideRoute(k);
    }
  }, true);
}]);

app.controller('SubmissionListController', ['$scope', '$http', function($scope, $http) {

  $scope.init = function() {
  }

  $scope.$watch('raw', function() {
    if (!$scope.raw) return;

    var raw = $scope.raw,
        transportations = raw.transportations;

    // group by city and company
    var cities = {},
        data = {};
    angular.forEach(transportations, function(t) {
      var cities = this[0],
          data = this[1];

      // city group
      var company = t.company || '';
      var key = t.province + '|' + t.city;
      t._cityKey = key;

      cities[key] = cities[key] || {
        key: key,
        province: t.province,
        city: t.city,
        count: 0,
        companies: {}
      };
      cities[key].count += 1;

      // company group
      var c = cities[key].companies;
      c[company] = c[company] || {
        company: t.company,
        items: []
      }
      c[company].items.push(t.id);

      // data by id
      data[t.id] = t;

    }, [cities, data]);

    // get city keys and sort company names
    var cityList = [];
    angular.forEach(cities, function(item, cityKey) {
      this.push(cityKey);

      var companies = [];
      for (var company in item.companies) {
        companies.push(company);
      }
      companies.sort();
      item.companyNames = companies;
    }, cityList);

    // sort cities
    cityList.sort(function(a, b) {
      return cities[b].count - cities[a].count;
    });

    $scope.data = data;
    $scope.dataTree = cities;
    $scope.cityKeyList = cityList;
  });

  $scope.show = function(id) {
    $scope.setActiveSubmission(id);
  }

}]);

})(window);

L.Polyline.Styled = L.Polyline.extend({
  _initEvents: function () {
    L.Polyline.prototype._initEvents.apply(this, arguments);

    if (this._path) {
      var classes = this.options.styleClass || [];
      if (typeof classes === "string") {
        classes = [classes];
      }
      for (var i=0; i<classes.length; i++) {
        this._path.classList.add(classes[i]);
      }
    }
  },
});

L.OSMDataLayer = L.Class.extend({
    includes: L.Mixin.Events,

    options: {
        minZoom: 17,
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
            this._map._pathRoot.appendChild(this._nodeContainer);
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
        this._container.parentNode.removeChild(this._nodeContainer);
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
            this._nodeContainer = this._createElement('g');
        }
    },

    _reset: function(e) {
        this._tiles = {};
        this._tilesToLoad = 0;

        this._data = {};

        this.nodes = {};
        this.pos = {};
        this.ways = {};
        this.wayTypes = {};

        this._tileUrl = {};

        while (this._container.lastChild) {
            this._container.removeChild(this._container.lastChild);
        }
        while (this._nodeContainer.lastChild) {
            this._nodeContainer.removeChild(this._nodeContainer.lastChild);
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
        var key, len, id, i, j, p, ch;

        var q = [];
        for (var x=x1; x<=x2; x++) {
            for (var y=y1; y<=y2; y++) {
                key = x + ':' + y;
                if (!this._data[key]) continue;
                q.push(key);
            }
        }

        // collect nodes and ways
        var nodes = {},
            pos = {},
            ways = {},
            wayTypes = {},
            sidList = {};
        for (i in q) {
            key = q[i];
            var data = this._data[key],
                ids = data.nodes.ids,
                latlngs = data.nodes.latlngs,
                wayList = data.ways,
                wayType = data.ways_highway;
            len = ids.length;
            for (var j=0; j<len; j++) {
                id = ids[j];
                if (nodes[id]) continue;
                if (this.nodes[id]) {
                    nodes[id] = this.nodes[id];
                    pos[id] = this.pos[id];
                    continue;
                }

                var latlng = latlngs[j];
                nodes[id] = L.latLng(latlng[0], latlng[1]);
                pos[id] = this._map.latLngToLayerPoint(nodes[id]);
                this.nodes[id] = nodes[id];
                this.pos[id] = pos[id];
            }

            for (id in wayList) {
                if (ways[id]) continue;
                ways[id] = wayList[id];
                wayTypes[id] = wayType[id];

                if (!this.ways[id]) {
                    this.ways[id] = ways[id];
                    this.wayTypes[id] = wayTypes[id];
                }

                var way = ways[id];
                for (j in way) {
                    var nid = way[j];
                    sidList[nid] = sidList[nid] || [];
                    sidList[nid].push(id);
                }
            }
        }

        // get existing ways
        var paths = {},
            used = {};
        for (i=0; i<this._container.childElementCount; i++) {
            ch = this._container.childNodes[i];
            var wayId = ch.getAttribute('data-way-id');
            if (wayId !== null) {
                paths[wayId] = ch;
                used[wayId] = false;
            }
        }

        // add new ways
        for (id in ways) {
            if (paths[id]) {
                used[id] = true;
                continue;
            }

            var way = ways[id];
            len = way.length;

            var str = '';
            for (i=0; i<len; i++) {
                var nodeId = way[i];
                p = pos[nodeId];
                str += (i ? 'L' : 'M') + p.x + ' '  + p.y + ' ';
            }

            var path = this._createElement('path');
            path.setAttribute('d', str);
            path.setAttribute('class', 'osm way way-' + wayTypes[id]);
            path.dataset.wayId = id;
            this._container.appendChild(path);

            L.DomEvent.addListener(path, 'mouseenter', this._onWayMouseEnter, this);
            L.DomEvent.addListener(path, 'mouseout', this._onWayMouseOut, this);
            L.DomEvent.addListener(path, 'click', this._onWayClick, this);
        }

        // remove unused ways
        for (id in used) {
            if (used[id]) continue;
            paths[id].remove();
        }

        // get existing nodes
        var dots = {};
        used = {};
        for (i=0; i<this._nodeContainer.childElementCount; i++) {
            ch = this._nodeContainer.childNodes[i];
            id = ch.getAttribute('data-node-id');
            if (id !== null) {
                dots[id] = ch;
                used[id] = false;
            }
        }

        // add new nodes
        for (id in pos) {
            if (dots[id]) {
                used[id] = true;
                continue;
            }

            p = pos[id];
            var circle = this._createElement('circle');
            circle.setAttribute('cx', p.x);
            circle.setAttribute('cy', p.y);
            circle.setAttribute('r', 3);
            circle.setAttribute('class', 'osm node');
            circle.dataset.nodeId = id;
            circle.dataset.wayIdList = sidList[id];
            this._nodeContainer.appendChild(circle);

            L.DomEvent.addListener(circle, 'mouseenter', this._onNodeMouseEnter, this);
            L.DomEvent.addListener(circle, 'mouseout', this._onNodeMouseOut, this);
            L.DomEvent.addListener(circle, 'click', this._onNodeClick, this);
        }

        // remove unused nodes
        for (id in used) {
            if (used[id]) continue;
            dots[id].remove();
        }
    },

    _onWayMouseEnter: function(e) {
        var t = e.target,
            sid = t.dataset.wayId;

        this.fire('osm:way:mouseenter', {wayId: sid, e: e});
        L.DomEvent.stopPropagation(e);
    },

    _onWayMouseOut: function(e) {
        var t = e.target,
            sid = t.dataset.wayId;

        this.fire('osm:way:mouseout', {wayId: sid, e: e});
        L.DomEvent.stopPropagation(e);
    },

    _onWayClick: function(e) {
        var t = e.target,
            sid = t.dataset.wayId;

        this.fire('osm:way:click', {wayId: sid, e: e});
        L.DomEvent.stopPropagation(e);
    },

    _onNodeMouseEnter: function(e) {
        var t = e.target,
            nid = t.dataset.nodeId;

        this.fire('osm:node:mouseenter', {nodeId: nid, e: e});
        L.DomEvent.stopPropagation(e);
    },

    _onNodeMouseOut: function(e) {
        var t = e.target,
            nid = t.dataset.nodeId;

        this.fire('osm:node:mouseout', {nodeId: nid, e: e});
        L.DomEvent.stopPropagation(e);
    },

    _onNodeClick: function(e) {
        var t = e.target,
            nid = t.dataset.nodeId;

        this.fire('osm:node:click', {nodeId: nid, e: e});
        L.DomEvent.stopPropagation(e);
    },
});
