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

        $scope.gaSendPageview();
      })
      .error(function(data, status) {
        console.error('load data error', url, status, data);
        $scope.loading--;
      });
  }

  $scope.gaSendPageview = function() {
    var id = $scope.data.id;
    var page = window.location.pathname + id + '/edit/';

    var p = $scope.data.geojson.properties;
    var province = $scope.provinceName[p.province]
    var name = (p.company || '') + ' ' + p.number;
    var title = 'Edit: ' + province + ' - ' + p.city + ' - ' + name;

    $scope.ga('send', 'pageview', {page: page, title: title});
  }

  $scope.refresh = function() {
    $scope.info.update($scope.data.geojson.properties);
    $scope.map.editable = true;
    $scope.map.fitRoutesToBounds = true;
    $scope.map.routes = $scope.data.geojson.geometry.coordinates;
    $scope.parentId = $scope.data.submission_id;
  }

  $scope.goToListCheck = function() {
    // TODO check modification state and show confirmation
    $scope.goToList();
  }

  $scope.goToList = function() {
    $scope.ga('send', 'event', 'transportation-edit', 'back');

    $scope.showPanel('transportation-list');
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

    var url = $('body').data('url-transportation-data-save').replace('0', $scope.data.id);

    var data = {geojson: JSON.stringify(geojson)};
    if ($scope.parentId) data['parent_id'] = $scope.parentId

    $scope.gaSendSubmitEditEvent();

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

  $scope.gaSubmitEditCount = {};

  $scope.gaSendSubmitEditEvent = function() {
    var id = $scope.data.id;

    if (!$scope.gaSubmitEditCount[id]) $scope.gaSubmitEditCount[id] = 0;
    $scope.gaSubmitEditCount[id]++;

    $scope.ga('send', 'event', 'transportation-edit', 'submit',
              ''+id, $scope.gaSubmitEditCount[id]);
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

