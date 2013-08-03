(function(app) {

var JAKARTA = [106.8294444, -6.1744444];

// var geocoder = new google.maps.Geocoder();

app.controller('MainController', ['$scope', function($scope) {

  $scope.panel = undefined;

  $scope.init = function() {
    $scope.map = {
      center: JAKARTA,
      zoom: 12,
      routes: [],
    }
    $scope.showPanel('editor');
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

  $scope.setMapEditable = function(editable) {
    $scope.map.editable = editable;
  }

  $scope.showRoute = function(routes) {
    $scope.map.fitToBounds = true;
    $scope.map.routes = routes;
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

  /*
  $scope.search = function() {
    var q = jQuery.trim($scope.searchQuery);
    if (!q) return;

    var query = {
      address: q,
      region: 'ID',
    }
    geocoder.geocode(query,
      function(results, status) {
        console.log(results);
        var pos = results[0].geometry.location;
        var center = [pos.lng(), pos.lat()];

        var v = results[0].geometry.viewport;
        var sw = v.getSouthWest();
        var ne = v.getNorthEast();
        var viewport = [[sw.lng(), sw.lat()], [ne.lng(), ne.lat()]];
        console.log('center', center, 'viewport', viewport);
        $scope.$apply(function() {
          $scope.map.viewport = viewport;
          //$scope.map.center = center;
        });
      });
  }
  */

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
    $scope.map.routes = [];
  });

  // panel

  $scope.showPanel = function(name) {
    $scope.panel = name;
  }

}]);

})(window.angkot.app);

