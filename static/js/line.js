(function() {

"use strict";

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
    .when('/', {
      templateUrl: '/static/partial/line/index.html',
      controller: 'LineIndexController',
    })
    .when('/:lineId/', {
      templateUrl: '/static/partial/line/info.html',
      controller: 'LineInfoController',
    })
    .when('/:lineId/edit/', {
      templateUrl: '/static/partial/line/edit.html',
      controller: 'LineEditController',
    });

});

app.factory('api', function($http) {
  var BASE = '/_/wapi/';
  return {
    line: {
      loadList: function() {
        var url = BASE + 'line/list.json';
        return $http.get(url);
      },
      loadLine: function(lineId) {
        var url = BASE + 'line/' + lineId + '.json';
        return $http.get(url);
      }
    },
  };
});

app.factory('lineData', function(api) {
  var lineData = {
    data: {},

    load: function(lineId, onLoaded) {
      var future = {
        onSuccess: function() {},
        onError: function() {},
        success: function(func) { this.onSuccess = func; },
        error: function(func) { this.onError = func; },
      };

      api.line.loadLine(lineId)
        .success(function(data) {
          angular.copy(data, lineData.data);
          future.onSuccess();
        })
        .error(function() {
          future.onError();
        });

      return future;
    },
  };

  return lineData;
});

app.factory('lineList', function(api) {
  var lineList = {
    lines: [],

    loaded: false,

    load: function() {
      api.line.loadList()
        .success(function(data) {
          angular.copy(data.lines, lineList.lines);
          lineList.loaded = true;
        });
    }
  };

  return lineList;
});

app.controller('LineIndexController', function($scope, $location, lineList) {
  $scope.lines = lineList.lines;

  $scope.$on('$routeChangeSuccess', function() {
    if (!lineList.loaded) {
      lineList.load();
    }
  });
});

app.controller('LineInfoController', function($scope, $routeParams, lineData) {
  $scope.data = lineData.data;

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
    lineData.load(lineId);
  };

  $scope.showLine = function(data) {
    $scope.data = data;
  };

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


})();

