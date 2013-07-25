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
      gm.event.addListener(editor, 'route_added', function(e) {
        console.log('route_added', e);
      });
      gm.event.addListener(editor, 'route_updated', function(e) {
        console.log('route_updated', e);
      });
      gm.event.addListener(editor, 'route_merged', function(e) {
        console.log('route_merged', e);
      });
      gm.event.addListener(editor, 'route_deleted', function(e) {
        console.log('route_deleted', e);
      });
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
    this._tooltip.setMap(map);
    if (this._map) this._initEvents();
  }

  P.getRoutes = function() {
    return this._routes;
  }

  P._init = function() {
    this._routes = [];
    this._events = {};
    this._tooltip = new Tooltip();
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
      gm.event.addDomListener(document, 'keyup', function(e) { self._onKeyUp(e); }),
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
    if (this._routes.length === 0) {
      this._tooltip.setContent('Klik untuk membuat rute');
    }
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

      this._isNewRoute = true;
      this._route = route;
      this._path = route.getPath();
      this._initRouteEvents(this._route);
      route.setMap(this._map);
    }

    this._path.push(e.latLng);
    this._nextPath.setAt(0, e.latLng);

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
    if (e.keyCode == 27) { // esc
      this._stopDrawing();
    }
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
      if (tip && window.event.shiftKey) {
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
      if (window.event.shiftKey) {
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

        this._nextLine.setMap(this._map);
        this._nextPath.push(e.latLng);
        this._nextPath.push(e.latLng);

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

  return C;
})();

var Tooltip = (function() {

  var C = function() {
    this._init();
  }

  var P = C.prototype;

  P.setMap = function(map) {
    if (this._map) this._destroy();
    this._map = map;
    this._updateVisibility();
    if (map) this._setup();
  }
  P.getMap = function() {
    return this._map;
  }

  P.setContent = function(html) {
    this._content = html;
    this._$c.html(html);
    this._updateVisibility();
  }
  P.getContent = function() {
    return this._content;
  }

  P._init = function() {
    this._events = [];
    this._$c = $('<div class="angkot-map-tooltip"></div>');
    this._$c.hide();
  }

  P._setup = function() {
    var self = this;
    this._events = [
      gm.event.addListener(this._map, 'mouseover', function(e) { self._onMouseOver(e); }),
      gm.event.addListener(this._map, 'mouseout', function(e) { self._onMouseOut(e); }),
      gm.event.addListener(this._map, 'mousemove', function(e) { self._onMouseMove(e); }),
    ]
    this._div = this._map.getDiv();
    $(this._div).append(this._$c);
  }

  P._destroy = function() {
    this._$c.remove();
    for (var i=0; i<this._events.length; i++) {
      gm.event.removeListener(this._events[i]);
    }
    delete this._div;
  }

  P._onMouseOver = function(e) {
    var p = e.pixel;
    this._pos = {x: p.x, y:p.y};
    this._$c.css({left: this._pos.x+'px', top: this._pos.y+'px'});
    this._inMap = true;
    this._updateVisibility();
  }

  P._onMouseOut = function(e) {
    this._inMap = false;
    this._updateVisibility();
  }

  P._onMouseMove = function(e) {
    var p = e.pixel;
    var dx = p.x - this._pos.x + 20;
    var dy = p.y - this._pos.y + 10;
    this._$c.css('transform', 'translate('+dx+'px, '+dy+'px)');
  }

  P._updateVisibility = function() {
    if (!this._content || !this._inMap) this._$c.hide();
    else this._$c.show();
  }

  return C;
})();



})();

