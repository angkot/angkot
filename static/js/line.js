(function() {

"use strict";

var app = angular.module('AngkotApp', ['ui.bootstrap', 'ui.router']);

app.controller('TopNavController', function($scope) {
});

app.controller('MapController', function($scope, $element, $attrs) {

  var CENTER = [-6.1744444, 106.8294444];
  var ZOOM = 13;

  $scope.map = null;
  $scope.layers = {};

  $scope.init = function() {
    initMap();
  };

  //
  // Initialization functions
  //

  function initMap() {
    var map = L.map($element[0].id, {
      boxZoom: false,
      minZoom: 7,
      maxZoom: 19,
      zoomControl: false,
    });
    map.setView(CENTER, ZOOM);
    map.addControl(new L.Control.Zoom({position: 'topright'}));

    var mapbox = L.mapbox.tileLayer($attrs.mapboxKey);
    mapbox.addTo(map);

    $scope.map = map;
  }
});

app.directive('angkotMap', function() {
  var CENTER = [-6.1744444, 106.8294444];
  var ZOOM = 13;
  var map;

  return {
    restrict: 'E',
    transclude: false,
    scope: {
    },
    link: {
      pre: function(scope, element, attrs, ctrl) {
        var map = L.map(element[0], {
          boxZoom: false,
          minZoom: 7,
          maxZoom: 19,
          zoomControl: false,
          layers: scope.layers,
        });
        map.setView(CENTER, ZOOM);
        map.addControl(new L.Control.Zoom({position: 'topright'}));
        scope.map = map;
      }
    },
    controller: function($scope) {
      $scope.layers = [];

      this.addLayer = function(layer) {
        layer.addTo($scope.map);
      }
    },
  }
});

app.directive('mapboxLayer', function() {
  return {
    restrict: 'E',
    require: '^angkotMap',
    scope: {
      key: '@',
    },
    link: function(scope, element, attrs, mapCtrl) {
      var layer = L.mapbox.tileLayer(scope.key);
      mapCtrl.addLayer(layer);
    },
  };
});

app.directive('editorLayer', function() {

  var LineEditor = L.Angkot.Route.extend({
    options: {
      minZoomEdit: 16,
    },

    initialize: function(layers, options) {
      L.Angkot.Route.prototype.initialize.call(this, layers, options);
      L.Util.setOptions(this, options);
    },

    onAdd: function(map) {
      L.Angkot.Route.prototype.onAdd.apply(this, arguments);
      map.on('zoomend', this._updateEditable, this);
    },

    onRemove: function(map) {
      map.off('zoomend', this._updateEditable, this);
      L.Angkot.Route.prototype.onRemove.apply(this, arguments);
    },

    _updateEditable: function(e) {
      var zoom = this._map.getZoom();
      this.setEditable(zoom >= this.options.minZoomEdit);
    },
  });

  return {
    restrict: 'E',
    require: '^angkotMap',
    link: function(scope, element, attrs, mapCtrl) {
      var layer = new LineEditor([], {
        maxRoutes: 1,
      });
      mapCtrl.addLayer(layer);
    }
  };
});


})();

