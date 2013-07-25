(function() {

//{"type":"LineString","coordinates":[[106.78092956542969,-6.128607295880528],[106.79019927978516,-6.1528433461544285],[106.78504943847656,-6.178443607362563],[106.80805206298828,-6.193803170076392],[106.8094253540039,-6.212575362017247],[106.83380126953125,-6.222473157416403],[106.86126708984375,-6.226568742378317],[106.87328338623047,-6.217012327817175],[106.87328338623047,-6.195509760592845],[106.8856430053711,-6.1811742288990965],[106.89044952392578,-6.15557409952461],[106.87397003173828,-6.1422615443784805],[106.87397003173828,-6.123145498606163],[106.85440063476562,-6.122804134421456]],"properties":{"license":{"CC BY-SA":true}}}

"use strict"

var JAKARTA = [-6.1744444, 106.8294444];
var gm = google.maps;
gm.visualRefresh = true;

var app = angular.module('AngkotRouteEditor', []);

app.controller('MainController', ['$scope', function($scope) {
  $scope.init = function() {
    $scope.center = new gm.LatLng(JAKARTA[0], JAKARTA[1]);
    $scope.zoom = 12;
    console.log('main init');

    var data = {
      type: 'Feature',
      properties: {
        city: 'Jakarta',
        company: 'Kopaja',
        number: 'S616',
        origin: 'Cipedak',
        destination: 'Blok M',
        license: {
          'CC BY-SA': true,
        }
      },
      geometry: {
        type: 'MultiLineString',
        coordinates: [
          [[106.78092956542969,-6.128607295880528],[106.79019927978516,-6.1528433461544285],[106.78504943847656,-6.178443607362563],[106.80805206298828,-6.193803170076392],[106.8094253540039,-6.212575362017247],[106.83380126953125,-6.222473157416403],[106.86126708984375,-6.226568742378317],[106.87328338623047,-6.217012327817175],[106.87328338623047,-6.195509760592845],[106.8856430053711,-6.1811742288990965],[106.89044952392578,-6.15557409952461],[106.87397003173828,-6.1422615443784805],[106.87397003173828,-6.123145498606163],[106.85440063476562,-6.122804134421456]]
        ]
      }
    }
  }
}]);

app.directive('angkotMap', function() {
  var controller = ['$scope', '$element', function($scope, $element) {

    var map,
        editor;

    var initMap = function() {
      var opts = {
        center: $scope.center,
        zoom: $scope.zoom,
        mapTypeId: gm.MapTypeId.ROADMAP,
        streetViewControl: false,
        draggableCursor: 'crosshair',
      }
      map = new gm.Map($element[0], opts);

      gm.event.addListener(map, 'drag', function() {
        $scope.$apply(function() {
          $scope.center = map.getCenter();
        });
      });
      gm.event.addListener(map, 'zoom_changed', function() {
        $scope.$apply(function() {
          $scope.zoom = map.getZoom();
        });
      });
    }

    var initEditor = function() {
      editor = new RouteEditor()
      editor.setMap(map);
    }

    $scope.init = function() {
      initMap();
      initEditor();
    }
  }];

  return {
    restrict: 'E',
    template: '<div class="angkot-map"></div>',
    replace: true,
    controller: controller,
    scope: {
      center: '=center',
      zoom: '=zoom',
      path: '=path',
    },
    link: function(scope, element, attrs) {
      scope.init();
    }
  }
});

var RouteEditor = (function() {
  var C = function() {
    this._init();
  }
  var P = C.prototype;

  P.setMap = function(map) {
    if (this._map) this._destroyEvents();
    this._map = map;
    if (this._map) this._initEvents();
  }

  P.getRoutes = function() {
    return this._routes;
  }

  P._init = function() {
    this._routes = [];
    this._events = {};
  }

  P._clear = function() {
  }

  P._reset = function() {
  }

  P._initEvents = function() {
    var self = this;
    this._events.editor = [
      gm.event.addListener(this._map, 'mousemove', function(e) { self._onMouseMove(e); }),
      gm.event.addListener(this._map, 'mouseover', function(e) { self._onMouseOver(e); }),
      gm.event.addListener(this._map, 'mouseout', function(e) { self._onMouseOut(e); }),
      gm.event.addListener(this._map, 'click', function(e) { self._onClick(e); }),
      gm.event.addListener(this._map, 'dblclick', function(e) { self._onDoubleClick(e); }),
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

  P._onMouseMove = function(e) {
    if (!this._nextLine || !this._nextPath.getLength()) return;
    this._nextPath.setAt(1, e.latLng);
  }

  P._onMouseOver = function(e) {
  }

  P._onMouseOut = function(e) {
  }

  P._onClick = function(e) {
    if (!this._nextLine) {
      var line = new gm.Polyline({
        clickable: false,
        editable: false,
        draggable: false,
        strokeColor: '#0000FF',
        strokeOpacity: 0.6,
        strokeWeight: 2,
      });
      this._nextLine = line;
      this._nextLine.setMap(this._map);
      this._nextPath = line.getPath();
    }
    if (this._nextPath.getLength() == 0) {
      this._nextPath.push(e.latLng);
      this._nextPath.push(e.latLng);
    }
    if (!this._nextLine.getMap()) {
      this._nextLine.setMap(this._map);
    }

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

      this._route = route;
      this._path = route.getPath();
      this._initRouteEvents(this._route);
      route.setMap(this._map);
    }

    this._path.push(e.latLng);
    this._nextPath.setAt(0, e.latLng);
  }

  P._onDoubleClick = function(e) {
  }

  P._onRouteClick = function(route, e) {
    if (e.vertex === undefined) {
      this._onClick(e);
      return;
    }

    if (route === this._route) {
      if (e.vertex === this._path.getLength() - 1) {
        this._route.setOptions({strokeColor:'#FF0000'});
        this._nextLine.setMap(null);
        this._nextPath.clear();
        delete this._path;
        delete this._route;
      }
      else {
        this._onClick(e);
      }
    }
    else if (this._route) {
      this._onClick(e);
    }
    else {
      var path = route.getPath();
      if (e.vertex === 0) {
        // flip vertex
        var arr = path.getArray().slice();
        for (var i=0, j=arr.length-1; j>=0; i++, j--) {
          path.setAt(i, arr[j]);
        }
      }
      if (e.vertex === 0 || e.vertex === path.getLength() - 1) {
        // continue
        this._route = route;
        this._path = route.getPath();
        route.setOptions({strokeColor: '#0000FF'});

        this._nextLine.setMap(this._map);
        this._nextPath.push(e.latLng);
        this._nextPath.push(e.latLng);
      }
    }
  }

  P._onRouteDoubleClick = function(route, e) {
    console.log('route dbl click', route, e);
  }

  P._initRouteEvents = function(route) {
    var self = this;
    var events = [
      gm.event.addListener(route, 'click', function(e) { self._onRouteClick(route, e); }),
      gm.event.addListener(route, 'dblclick', function(e) { self._onRouteDoubleClick(route, e); }),
    ];
    this._events[route] = events;
  }

  P._destroyRouteEvents = function(route) {
    if (!this._events[route]) return;
    var events = this._events[route];
    for (var i=0; i<events.length; i++) {
      gm.event.removeListener(events[i]);
    }
    delete this._events[route];
  }

  return C;
})();




})();

