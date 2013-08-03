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
      for (var i=0; i<routes.length; i++) {
        res.push(toLatLng(routes[i]));
      }
      editor.setRoutes(res);
    });

    var map, editor;

    var initMap = function() {
      var center = [$scope.center[1], $scope.center[0]];
      map = L.mapbox.map($element[0], $scope.mapboxKey, {
          boxZoom: false,
        }).setView(center, $scope.zoom);
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

