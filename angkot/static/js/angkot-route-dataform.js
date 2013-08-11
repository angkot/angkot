(function(app) {

app.controller('DataFormController', ['$scope', '$http', '$location', function($scope, $http, $location) {

  $scope.checked = false;
  $scope.valid = false;
  $scope.incomplete = false;
  $scope.saved = false;
  $scope.modified = false;
  $scope.loading = 0;

  $scope.init = function() {
  }

  $scope.$watch('panel', function(value, old) {
    if (value != 'data-form' || value === old) return;
    $scope.reset();
    $scope.map.editable = true;
    $scope.map.info = undefined;
    $scope.load();
  });

  $scope.load = function() {
    var tid = parseInt($location.path().replace(/\//g, ''));
    $scope.loading++;

    var url = jQuery('body').data('url-transportation-data').replace('0', tid);
    $http.get(url)
      .success(function(data) {
        $scope.data = data;
        $scope.refresh();
        $scope.loading--;
      })
      .error(function(data, status) {
        console.error('load data error', url, status, data);
        $scope.loading--;
      });
  }

  $scope.refresh = function() {
    $scope.info.update($scope.data.geojson.properties);
    $scope.map.editable = true;
    $scope.map.fitRoutesToBounds = true;
    $scope.map.routes = $scope.data.geojson.geometry.coordinates;
  }

  $scope.saveRouteCheck = function() {
    $scope.error = null;
    $scope.message = null;
    $scope.errorIncomplete = false;

    var valid = true;

    var focus = function(name) {
      jQuery('#new-route input[name="'+name+'"]').focus();
    }

    if (!$scope.info.province) {
      focus('province');
      valid = false;
    }

    if (valid && !$scope.info.city) {
      focus('city');
      valid = false;
    }

    if (valid && !$scope.info.number) {
      focus('number');
      valid = false;
    }

    if (valid && !$scope.termAgreement) {
      focus('term-agreement');
      valid = false;
    }

    $scope.incomplete = !valid;
    $scope.checked = true;

    if (valid) {
      $scope.saveRoute();
    }
  }

  $scope.saveRoute = function() {
    $scope.error = null;
    $scope.message = 'mengirim data..';

    var geojson = {
      type: 'Feature',
      properties: {
        province: $scope.info.province,
        city: $scope.info.city,
        company: $scope.info.company,
        number: $scope.info.number,
        origin: $scope.info.origin,
        destination: $scope.info.destination,
        accept: ['ContributorTerms'],
      },
      geometry: {
        type: 'MultiLineString',
        coordinates: $scope.map.routes,
      },
    }

    var url = $('body').data('url-save');

    var data = {geojson: JSON.stringify(geojson)};
    if ($scope.parentId) data['parent_id'] = $scope.parentId

    $http.post(url, jQuery.param(data))
      .success(function(data) {
        $scope.message = 'Terima kasih atas partisipasi Anda!';
        $scope.parentId = data.submission_id;
        $scope.checked = false;
        $scope.saved = true;
      })
      .error(function(msg, status) {
        $scope.message = null;
        $scope.error = 'Gagal! code='+status;
      });
  }

  $scope.$on('map-reset', function() {
    $scope.reset();
  });

  $scope.reset = function() {
    $scope.info.reset();
    $scope.map.reset();
    $scope.termAgreement = false;
    $scope.modified = false;
    $scope.saved = false;
    $scope.checked = false;
    $scope.message = null;
    $scope.error = null;
    $scope.parentId = null;
  }

  function updateModified() {
    $scope.modified = $scope.info.province !== '' ||
                      $scope.info.city !== '' ||
                      $scope.info.company !== '' ||
                      $scope.info.number !== '' ||
                      $scope.info.origin !== '' ||
                      $scope.info.destination !== '' ||
                      $scope.map.routes.length > 0;
  }

  $scope.$watch('info.province', updateModified);
  $scope.$watch('info.city', updateModified);
  $scope.$watch('info.company', updateModified);
  $scope.$watch('info.number', updateModified);
  $scope.$watch('info.origin', updateModified);
  $scope.$watch('info.destination', updateModified);
  $scope.$watch('termAgreement', updateModified);
  $scope.$watch('map.routes', updateModified, true);

}]);

})(window.angkot.app);

