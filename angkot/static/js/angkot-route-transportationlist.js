(function(app) {

"use strict";

app.controller('TransportationListController', ['$scope', '$http', '$location', function($scope, $http, $location) {

  $scope.transportations = undefined;
  $scope.loading = 0;

  $scope.init = function() {
  };

  $scope.$watch('panel', function(value, old) {
    if (value !== 'transportation-list') return;
    $scope.reload();
    $scope.map.editable = false;
    $scope.map.reset();
    $location.path('/');

    if (value !== old) {
      $scope.gaSendListPageview();
    }
  });

  $scope.reload = function() {
    $scope.loading++;
    var url = jQuery('body').data('url-transportation-list');
    $http.get(url)
      .success(function(data) {
        $scope.transportations = data.transportations;
        $scope.loading--;
      });
  };

  var groupByCity = function(data) {
    var groups = {};
    angular.forEach(data, function(item) {
      if (!groups[item.city]) {
        groups[item.city] = {
          city: item.city,
          transportations: []
        };
      }

      item._label = (item.company ? item.company + ' ' : '') + item.number;
      groups[item.city].transportations.push(item);
    });

    var res = [];
    angular.forEach(groups, function(item, city) {
      res.push(item);
    });

    res = res.sort(function(a, b) {
      return b.transportations.length - a.transportations.length;
    });

    return res;
  };

  $scope.$watch('transportations', function(value) {
    $scope.groups = groupByCity(value);
  });

  $scope.showTransportation = function(t) {
    // TODO show loading
    $location.path('/'+t.id+'/');
    var url = jQuery('body').data('url-transportation-data').replace('0', t.id);
    $http.get(url)
      .success(function(data) {
        $scope.data = data;
        $scope.map.info = data.geojson;
        $scope.map.editable = false;
        $scope.map.fitRoutesToBounds = true;
        $scope.map.routes = data.geojson.geometry.coordinates;

        $scope.gaSendTransportationPageview();
      });
  };

  $scope.gaSendListPageview = function() {
    var page = window.location.pathname;
    $scope.ga('send', 'pageview', {page: page});
  };

  $scope.gaSendTransportationPageview = function() {
    var id = $scope.data.id;
    var page = window.location.pathname + id + '/';

    var p = $scope.data.geojson.properties;
    var province = $scope.provinceName[p.province];
    var name = (p.company || '') + ' ' + p.number;
    var title = province + ' - ' + p.city + ' - ' + name;

    $scope.ga('send', 'pageview', {page: page, title: title});
  };

  $scope.$on('route-edit-click', function() {
    $scope.ga('send', 'event', 'transportation', 'click-edit');

    if ($scope.panel !== 'transportation-list') return;
    $scope.$apply(function() {
      $scope.showLogin(function() {
        $scope.editTransportation($scope.data.id);
      }, 'map-info');
    });
  });

}]);

})(window.angkot.app);

