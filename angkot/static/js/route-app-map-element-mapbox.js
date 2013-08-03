(function(angkot) {

"use strict"

var app = angkot.app;

app.directive('angkotMap', function() {

  var controller = ['$scope', '$element', function($scope, $element) {

    $scope.init = function() {
      initMap();
      initEditor();
    }

    $scope.$watch('editable', function(value) {
      editor.setEditable(value);
    });

    var updateView = function() {
      var pos = $scope.center;
      var center = [pos[1], pos[0]];
      var zoom = $scope.zoom;
      map.setView(center, zoom);
    }

    $scope.$watch('center', updateView);
    $scope.$watch('zoom', updateView);

    $scope.$watch('routes', function(routes) {
      var res = [];
      var bounds;
      for (var i=0; i<routes.length; i++) {
        var route = toLatLng(routes[i]);
        res.push(route);

        var bound = new L.LatLngBounds(route);
        if (!bounds) bounds = bound;
        else bounds.extend(bound);
      }
      editor.setRoutes(res);
      editor.setEditable($scope.editable);

      if ($scope.fitToBounds && bounds) {
        map.fitBounds(bounds);
      }
    });

    $scope.$watch('viewport', function(viewport) {
      if (!viewport) return;

      var a = [viewport[0][1], viewport[0][0]];
      var b = [viewport[1][1], viewport[1][0]];
      var bounds = new L.LatLngBounds([a, b]);
      map.fitBounds(bounds);
    });

    var map, editor;

    var initMap = function() {
      var center = [$scope.center[1], $scope.center[0]];
      map = L.mapbox.map($element[0], $scope.mapboxKey, {
          boxZoom: false,
          minZoom: 12,
          maxZoom: 17,
        }).setView(center, $scope.zoom);

      // map.on('zoomend', function() {
      //   $scope.$apply(function() {
      //     $scope.zoom = map.getZoom();
      //   });
      // });

      // map.on('moveend', function() {
      //   $scope.$apply(function() {
      //     var center = map.getCenter();
      //     $scope.center = [center.lng, center.lat];
      //   });
      // });

    }

    var initEditor = function() {
      editor = new L.Angkot.Route();
      editor.setEditable($scope.editable);
      editor.addTo(map);

      editor.on('route:add', function(e) {
        var routes = editor.getRoutes();
        $scope.$apply(function() {
          $scope.routes.push(toLngLat(routes[e.index]));
        });
      });

      editor.on('route:delete', function(e) {
        $scope.$apply(function() {
          $scope.routes.splice(e.index, 1);
        });
      });

      editor.on('route:update', function(e) {
        var routes = editor.getRoutes();
        $scope.$apply(function() {
          $scope.routes[e.index] = toLngLat(routes[e.index]);
        });
      });
    }

    var toLngLat = function(path) {
      var res = [];
      for (var i=0; i<path.length; i++) {
        var p = path[i];
        res.push([p.lng, p.lat]);
      }
      return res;
    }

    var toLatLng = function(path) {
      var res = [];
      for (var i=0; i<path.length; i++) {
        var p = path[i];
        res.push([p[1], p[0]]);
      }
      return res;
    }

  }];

  return {
    restrict: 'E',
    template: '<div class="angkot-map"></div>',
    replace: true,
    controller: controller,
    scope: {
      mapboxKey: '=',
      center: '=',
      zoom: '=',
      routes: '=',
      viewport: '=',
      fitToBounds: '=',
      editable: '=',
    },
    link: function(scope, element, attrs) {
      scope.init();
    }
  };

});

})(window.angkot);

