(function() {

"use strict"

var app = angular.module('AngkotApp', ['ngRoute']);

app.config(function($httpProvider) {

  $httpProvider.defaults.headers.post["Content-Type"] = "application/x-www-form-urlencoded";

  $httpProvider.defaults.xsrfCookieName = 'csrftoken';
  $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';

});

app.config(function($locationProvider, $routeProvider) {

  $locationProvider.html5Mode(true);
  $locationProvider.hashPrefix('!');

  $routeProvider
    .when('/:lineId', {});

});

app.factory('api', function($http) {
  var BASE = '/_/wapi/';
  return {
    line: {
      load: function(lineId) {
        var url = BASE + 'line/' + lineId + '.json';
        return $http.get(url);
      }
    },
  }
});

app.controller('InfoController', function($scope, $route, $routeParams, $location, api) {
  $scope.data = {};

  //
  // Routing
  //

  $scope.$on('$routeChangeSuccess', function() {
    if ($routeParams.lineId) {
      $scope.loadLine($routeParams.lineId);
    }
  });

  //
  // Show transportation line
  //

  $scope.loadLine = function(lineId) {
    api.line.load(lineId)
      .success(function(data) {
        $scope.showLine(data);
      });
  }

  $scope.showLine = function(data) {
    $scope.data = data;
  }

});

app.controller('MapController', function($scope, $element, $attrs) {

  var CENTER = [-6.1744444, 106.8294444];
  var ZOOM = 13;

  $scope.map = null;
  $scope.layers = {};

  $scope.init = function() {
    initMap();
  }

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


})();

