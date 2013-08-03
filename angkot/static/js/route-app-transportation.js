(function(app) {

"use strict"

app.controller('TransportationController', ['$scope', '$http', function($scope, $http) {

  $scope.data = undefined;
  $scope.loading = 0;

  $scope.init = function() {
  }

  $scope.$watch('panel', function(value, old) {
    if (value !== 'transportation') return;
    if ($scope.data === undefined) {
      $scope.reload();
    }
  });

  var loadData = function(data) {
    $scope.provinces = data.provinces;

    $scope.province_name = {};
    $scope.province_count = {};
    $scope.city_count = {};
    $scope.cities = {};
    $scope.transportations = {};
    $scope.count = 0;

    angular.forEach(data.provinces, function(value) {
      var prov = value[0];
      $scope.province_name[prov] = value[1];
      $scope.province_count[prov] = 0;
      $scope.city_count[prov] = {};
      $scope.cities[prov] = [];
      $scope.transportations[prov] = {};
    });

    angular.forEach(data.transportations, function(item) {
      var prov = item.province,
          city = item.city;

      // first/default selection
      if (!$scope.count) {
        $scope.province = prov;
        $scope.city = city;
      }

      $scope.count += 1;
      $scope.province_count[prov] += 1;

      if (!$scope.city_count[prov][city]) {
        $scope.city_count[prov][city] = 0;
        $scope.transportations[prov][city] = [];
      }
      $scope.city_count[prov][city] += 1;
      $scope.transportations[prov][city].push(item);
    });

    angular.forEach($scope.city_count, function(cities, prov) {
      for (var city in cities) {
        $scope.cities[prov].push(city);
      }
      $scope.cities[prov].sort();
    });
  }

  $scope.reload = function() {
    $scope.loading++;
    var url = jQuery('#transportations').data('url-transportation-list');
    $http.get(url)
      .success(function(data) {
        loadData(data);
        $scope.data = data;
        $scope.loading--;
      });
  }

  $scope.provinceListLabel = function(prov) {
    var count = $scope.province_count[prov[0]];
    return prov[1] + ' (' + count + ')';
  };

  $scope.cityListLabel = function(city) {
    var count = $scope.city_count[$scope.province][city];
    return city + ' (' + count + ')';
  }

  $scope.provHasTransportation = function(prov) {
    if (!prov) return false;
    return $scope.province_count[prov[0]];
  }

  $scope.cityHasTransportation = function(city) {
    if (!city) return false;
    return $scope.city_count[$scope.province][city];
  }

  $scope.showTransportation = function(t) {
    console.log('show', t);
  }

}]);

})(window.angkot.app);

