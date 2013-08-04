(function(app) {

var JAKARTA = [106.8294444, -6.1744444];
var INDONESIA = [[143.0419921875, 8.189742344383703], [93.8671875, -11.867350911459308]];

app.controller('MainController', ['$scope', '$http', function($scope, $http) {

  $scope.panel = undefined;

  $scope.init = function() {
    $scope.map = {
      center: JAKARTA,
      maxBounds: INDONESIA,
      zoom: 13,
      routes: [],
    }
    $scope.showPanel('transportation');
    $scope.mapboxKey = jQuery('body').data('mapbox-key');
  }

  $scope.$watch('map.zoom', function(value) {
    // console.log('main: zoom', value);
  });
  $scope.$watch('map.center', function(value) {
    // console.log('main: center', value);
  });

  $scope.$watch('map.routes', function(value, old) {
    // console.log('routes updated');
    // console.log(old);
    // console.log(value);
  }, true);

  $scope.setMapData = function(data) {
    if (data.center) $scope.map.center = data.center;
    if (data.zoom) $scope.map.zoom = data.zoom;
    if (data.routes) $scope.map.routes = data.routes;
  }

  $scope.setMapGeoJSON = function(data) {
    $scope.showRoute(data.geometry.coordinates);
    $scope.showInfo(data);
  }

  $scope.setMapEditable = function(editable) {
    $scope.map.editable = editable;
  }

  $scope.showRoute = function(routes) {
    $scope.map.fitToBounds = true;
    $scope.map.routes = routes;
  }

  $scope.showInfo = function(data) {
    $scope.map.info = data;
  }

  $scope.showModal = function(data) {
    $scope.modal = $scope.modal || {};
    if (data === false) {
      $scope.modal.show = false;
    }
    else {
      if (data.show !== undefined) $scope.modal.show = data.show;
      if (data.title !== undefined) $scope.modal.title = data.title;
      if (data.content !== undefined) $scope.modal.content = data.content;
    }
  }

  $scope.showModalFrom = function(selector) {
    var title = jQuery(selector).find('> h2').text();
    var content = jQuery(selector).find('> .content').html();
    $scope.showModal({
      show: true,
      title: title,
      content: content,
    });
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
        console.log(data);
        if (data.length == 0) {
          console.log('not found');
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

  $scope.newRoute = function() {
    $scope.resetMap();
    $scope.showPanel('editor');
  }

  $scope.$on('map-reset', function() {
    $scope.map.routes = [];
  });

  $scope.editMap = function() {
    console.log('main edit map');
  }

  // panel

  $scope.showPanel = function(name) {
    $scope.panel = name;
  }

}]);

})(window.angkot.app);

