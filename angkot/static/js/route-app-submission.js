(function(app) {

var JAKARTA = [-6.1744444, 106.8294444];

app.controller('SubmissionController', ['$scope', '$http', function($scope, $http) {

  $scope.init = function() {
  }

  $scope.saveRouteCheck = function() {
    $scope.error = null;
    $scope.message = null;

    if (!$scope.licenseAgreement) {
      $scope.error = 'Demi kepentingan pengayaan data, rute yang Anda kirim perlu dilisensikan di bawah CC BY-SA. Silakan beri tanda centang jika Anda setuju.';
      return;
    }
    $scope.saveRoute();
  }

  $scope.saveRoute = function() {
    $scope.error = null;
    $scope.message = 'mengirim data..';

    var geojson = {
      type: 'Feature',
      properties: {
        kota: $scope.city,
        perusahaan: $scope.company,
        nomor: $scope.number,
        berangkat: $scope.origin,
        jurusan: $scope.destination,
        license: {
          'ODbL v1.0': $scope.licenseAgreement
        }
      },
      geometry: {
        type: 'MultiLineString',
        coordinates: $scope.routes,
      },
    }

    var url = $('body').data('url-save');

    var data = {geojson: JSON.stringify(geojson)};
    if ($scope.parentId) data['parent_id'] = $scope.parentId

    $http.post(url, jQuery.param(data))
      .success(function(data) {
        $scope.message = 'Terima kasih atas partisipasi Anda!';
        $scope.parentId = data.submission_id;
      })
      .error(function(msg, status) {
        $scope.message = null;
        $scope.error = 'Gagal! code='+status;
      });
  }

  $scope.showLicense = function() {
    $scope.showModalFrom('#license-info-content');
  }

}]);

})(window.angkot.app);

