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

  var groupTransportations = function(data) {
    if (!data) return [];

    var cmpNumber = function(a, b) {
      return a.number.localeCompare(b.number);
    };

    // order by cities and companies
    var items = data.slice();
    items = items.sort(function(a, b) {
      if (a.city != b.city) {
        return a.city.localeCompare(b.city);
      }
      if (!a.company) return -1;
      if (!b.company) return 1;
      return a.company.localeCompare(b.company);
    });

    // Make a tree
    var city = {name: undefined, _total: 0},
        company = {name: undefined, items: []};
    var h = [];
    angular.forEach(items, function(item) {
      if (item.city != city.name) {
        company.items = company.items.sort(cmpNumber);
        company = {
          name: item.company,
          items: [],
        };
        city = {
          name: item.city,
          companies: [company],
          _total: 0,
        };
        h.push(city);
      }
      if (item.company != company.name) {
        city._total += company.items.length;
        company.items = company.items.sort(cmpNumber);
        company = {
          name: item.company,
          items: []
        };
        city.companies.push(company);
      }
      company.items.push(item);
    });
    city._total += company.items.length;

    // Sort city by the number of transportations
    h = h.sort(function(a, b) {
      return b._total - a._total;
    });

    return h;
  };

  $scope.$watch('transportations', function(value) {
    $scope.groups = groupTransportations(value);
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

