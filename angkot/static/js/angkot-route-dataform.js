(function(app) {

app.controller('DataFormController', ['$scope', '$http', 'transportationService', function($scope, $http, transportationService) {

  $scope.checked = false;
  $scope.valid = false;
  $scope.incomplete = false;
  $scope.saved = false;
  $scope.modified = false;

  $scope.info = transportationService;

  $scope.init = function() {
    loadProvinces();
  }

  $scope.$watch('panel', function(value, old) {
    if (old == 'data-form' && value != 'data-form') {
      $scope.stashData();
    }
    if (value != 'data-form' || value === old) return;
    $scope.unstashData();
    $scope.map.editable = true;
  });

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

    if (!$scope.info.city) {
      focus('city');
      valid = false;
    }

    if (valid && !$scope.info.number) {
      focus('number');
      valid = false;
    }

    if (valid && !$scope.licenseAgreement) {
      focus('license-agreement');
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
        license: {
          'ODbL v1.0': $scope.licenseAgreement
        }
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

  $scope.showLicense = function() {
    $scope.showModalFrom('#license-info-content');
  }

  $scope.$on('map-reset', function() {
    $scope.info.reset();
    $scope.licenseAgreement = false;
    $scope.modified = false;
    $scope.saved = false;
    $scope.checked = false;
    $scope.message = null;
    $scope.error = null;
    $scope.parentId = null;
  });

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
  $scope.$watch('licenseAgreement', updateModified);
  $scope.$watch('map.routes', updateModified, true);

  // save/restore data

  $scope.stashData = function() {
    var routes = [];
    for (var i=0; i<$scope.map.routes.length; i++) {
      routes.push($scope.map.routes[i].slice());
    }
    var map = {
      view: {
        center: $scope.map.view.center,
        zoom: $scope.map.view.zoom,
      },
      routes: routes,
      editable: $scope.map.editable,
    }

    $scope.stash = {
      province: $scope.info.province,
      city: $scope.info.city,
      company: $scope.info.company,
      number: $scope.info.number,
      origin: $scope.info.origin,
      destination: $scope.info.destination,
      licenseAgreement: $scope.licenseAgreement,
      map: map,
    }
  }

  $scope.unstashData = function() {
    var stash = $scope.stash;
    if (!stash) return;

    $scope.info.province = stash.province;
    $scope.info.city = stash.city;
    $scope.info.company = stash.company;
    $scope.info.number = stash.number;
    $scope.info.origin = stash.origin;
    $scope.info.destination = stash.destination;
    $scope.licenseAgreement = stash.licenseAgreement;
    $scope.map.update(stash.map);
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

