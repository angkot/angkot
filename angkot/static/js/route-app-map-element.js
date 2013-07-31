(function(angkot) {

"use strict"

var gm = google.maps;
var app = angkot.app;

gm.visualRefresh = true;

app.directive('angkotMap', function() {

  var controller = ['$scope', '$element', function($scope, $element) {

    var map,
        editor;

    $scope.$watch('center', function(pos) {
      if (pos === undefined) return;
      var center = new gm.LatLng(pos[1], pos[0]);
      map.setCenter(center);
    });

    $scope.$watch('zoom', function(zoom) {
      if (zoom === undefined) return;
      map.setZoom(zoom);
    });

    $scope.$watch('routes', function(routes) {
      if (routes === undefined) return;
      var data = [];
      for (var i=0; i<routes.length; i++) {
        data.push(makeLatLng(routes[i]));
      }
      editor.setRouteArrays(data);

      if (data.length>0 && $scope.fitToBounds) {
        editor.fitToBounds();
      }
      editor.setEditable($scope.editable);
    });

    $scope.$watch('viewport', function(value) {
      if (value === undefined) return;
      var bounds = new gm.LatLngBounds(new gm.LatLng(value[0][1], value[0][0]),
                                       new gm.LatLng(value[1][1], value[1][0]));
      map.fitBounds(bounds);
    });

    $scope.$watch('editable', function(value) {
      editor.setEditable(value);
    });

    var apply = function(fn) {
      if ($scope.$$phase || $scope.$root.$$phase) {
        fn();
      }
      else {
        $scope.$apply(fn);
      }
    }

    var initMap = function() {
      var opts = {
        mapTypeId: gm.MapTypeId.ROADMAP,
        streetViewControl: false,
        draggableCursor: 'crosshair',
        styles: [{
          featureType: 'poi',
          elementType: 'labels',
          stylers: [{
            visibility: 'off'
          }]
        }],
      }
      map = new gm.Map($element[0], opts);

      gm.event.addListener(map, 'drag', function() {
        apply(function() {
          var center = map.getCenter();
          $scope.center = [center.lng(), center.lat()];
        });
      });
      gm.event.addListener(map, 'zoom_changed', function() {
        apply(function() {
            $scope.zoom = map.getZoom();
        });
      });
    }

    var extractPath = function(route) {
      var path = route.getPath().getArray().slice();
      var res = [];
      for (var i=0; i<path.length; i++) {
        var p = path[i];
        res.push([p.lng(), p.lat()]);
      }
      return res;
    }

    var makeLatLng = function(path) {
      var res = [];
      for (var i=0; i<path.length; i++) {
        var p = path[i];
        res.push(new gm.LatLng(p[1], p[0]));
      }
      return res;
    }

    var initEditor = function() {
      editor = new angkot.route.Editor()
      editor.setMap(map);
      gm.event.addListener(editor, 'route_added', function(index) {
        var routes = editor.getRoutes();
        $scope.$apply(function() {
          $scope.routes.push(extractPath(routes[index]));
        });
      });
      gm.event.addListener(editor, 'route_updated', function(index) {
        var routes = editor.getRoutes();
        $scope.$apply(function() {
          $scope.routes[index] = extractPath(routes[index]);
        });
      });
      gm.event.addListener(editor, 'route_merged', function(e) {
        var routes = editor.getRoutes();
        var route = routes[e.result];
        var a = e.first,
            b = e.second;
        if (e.second < e.first) {
          a = e.second;
          b = e.first;
        }
        $scope.$apply(function() {
          $scope.routes.splice(b, 1);
          $scope.routes.splice(a, 1);
          $scope.routes.splice(e.result, 0, extractPath(route));
        });
      });
      gm.event.addListener(editor, 'route_deleted', function(index) {
        $scope.$apply(function() {
          $scope.routes.splice(index, 1);
        });
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
      routes: '=routes',
      viewport: '=viewport',
      fitToBounds: '=fitToBounds',
      editable: '=editable',
    },
    link: function(scope, element, attrs) {
      scope.init();
    }
  }
});

})(window.angkot);

