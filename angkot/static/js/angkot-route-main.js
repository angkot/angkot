(function(app) {

var JAKARTA = [106.8294444, -6.1744444];
var INDONESIA = [[143.0419921875, 8.189742344383703], [93.8671875, -11.867350911459308]];

app.factory('transportationService', function() {
  return {
    province: undefined,
    city: undefined,
    company: undefined,
    number: undefined,
    origin: undefined,
    destination: undefined,

    reset: function() {
      this.province = undefined;
      this.city = undefined;
      this.company = undefined;
      this.number = undefined;
      this.origin = undefined;
      this.destination = undefined;
    },

    update: function(data) {
      if (data.province !== undefined) this.province = data.province;
      if (data.city !== undefined) this.city = data.city;
      if (data.company !== undefined) this.company = data.company;
      if (data.number !== undefined) this.number = data.number;
      if (data.origin !== undefined) this.origin = data.origin;
      if (data.destination !== undefined) this.destination = data.destination;
    }
  }
});

app.controller('MainController', ['$scope', '$http', 'modalService', 'mapService', 'transportationService', function($scope, $http, modalService, mapService, transportationService) {

  $scope.panel = undefined;
  $scope.modal = modalService;
  $scope.map = mapService;
  $scope.info = transportationService;

  $scope.init = function() {
    $scope.map.view = {
      center: JAKARTA,
      zoom: 13,
    }
    $scope.map.maxBounds = INDONESIA;
    $scope.map.fitRoutesToBounds = true;
    $scope.map.editable = false;
    $scope.showPanel('transportation-list');
    $scope.mapboxKey = jQuery('body').data('mapbox-key');
    loadProvinces();
  }

  $scope.onRouteChanged = function() {
  }

  $scope.onRouteEditClicked = function() {
    $scope.$broadcast('route-edit-click');
  }

  $scope.search = function() {
    var q = jQuery.trim($scope.searchQuery);
    if (!q) return;

    var query = {
      format: 'json',
      json_callback: 'JSON_CALLBACK',
      q: q,
      countrycodes: 'ID',
    }

    var url = 'http://open.mapquestapi.com/nominatim/v1/search.php?' + jQuery.param(query);

    $http.jsonp(url)
      .success(function(data) {
        if (data.length == 0) {
          console.error('search not found');
        }
        else {
          var res = data[0];
          var bbox = [[res.boundingbox[2], res.boundingbox[0]],
                      [res.boundingbox[3], res.boundingbox[1]]];
          $scope.map.viewport = bbox;
        }
      });
  }

  $scope.resetMapCheck = function() {
    var msg = 'Apakah Anda yakin untuk menghapus semua data yang sudah ' +
              'Anda masukkan dan mengulangi dari awal?';
    if (confirm(msg)) {
      $scope.resetMap();
    }
  }

  $scope.resetMap = function() {
    $scope.$broadcast('map-reset');
  }

  $scope.$on('map-reset', function() {
    $scope.map.reset();
  });

  $scope.newTransport = function() {
    $scope.modal.useSelector('#new-transportation-modal');
  }

  // panel

  $scope.showPanel = function(name) {
    $scope.panel = name;
  }

  // provinces

  var loadProvinces = function() {
    var url = jQuery('body').data('url-province-list');
    $http.get(url)
      .success(function(data) {
        $scope.provinces = data.provinces;
      });
  }

}]);

})(window.angkot.app);

