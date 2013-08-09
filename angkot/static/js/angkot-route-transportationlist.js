(function(app) {

app.controller('TransportationListController', ['$scope', '$http', function($scope, $http) {

  $scope.provinces = undefined;
  $scope.transportations = undefined;
  $scope.loading = 0;

  $scope.init = function() {
  }

  $scope.$watch('panel', function(value, old) {
    if (value !== 'transportation-list') return;
    if ($scope.transportations === undefined) {
      $scope.reload();
    }
    $scope.map.editable = false;
  });

  $scope.reload = function() {
    $scope.loading++;
    var url = jQuery('body').data('url-transportation-list');
    $http.get(url)
      .success(function(data) {
        $scope.provinces = data.provinces;
        $scope.transportations = data.transportations;
        $scope.loading--;
      });
  };

  var groupByProvince = function(data) {
    var groups = {};
    angular.forEach(data, function(item) {
      if (!groups[item.province]) {
        groups[item.province] = {
          province: item.province,
          transportations: []
        }
      }

      item._label = (item.company ? item.company + ' ' : '') + item.number;
      groups[item.province].transportations.push(item);
    });

    var res = [];
    angular.forEach(groups, function(item, province) {
      res.push(item);
    });

    res = res.sort(function(a, b) {
      return b.transportations.length - a.transportations.length;
    });

    return res;
  }

  $scope.$watch('provinces', function(value) {
    var names = {};
    angular.forEach(value, function(item) {
      names[item[0]] = item[1];
    })
    $scope.provinceName = names;
  });

  $scope.$watch('transportations', function(value) {
    $scope.groups = groupByProvince(value);
  });

  $scope.showTransportation = function(t) {
    // TODO show loading
    var url = jQuery('body').data('url-transportation-data').replace('0', t.id);
    $http.get(url)
      .success(function(data) {
        $scope.data = data;
        $scope.map.info = data.geojson;
        $scope.map.editable = false;
        $scope.map.fitRoutesToBounds = true;
        $scope.map.routes = data.geojson.geometry.coordinates;
      });
  }

  $scope.$on('route-edit-click', function() {
    if ($scope.panel !== 'transportation-list') return;
    $scope.info.reset();
    $scope.map.info = undefined;
    $scope.info.update($scope.data.geojson.properties);
    $scope.$apply(function() {
      $scope.showPanel('data-form');
    });
  });

}]);

})(window.angkot.app);

