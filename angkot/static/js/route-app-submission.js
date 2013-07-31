(function(app) {

app.controller('SubmissionController', ['$scope', '$http', function($scope, $http) {

  $scope.submissions = undefined;
  $scope.loading = 0;

  $scope.init = function() {
  }

  $scope.$watch('panel', function(value, old) {
    if (value !== 'submission') return;
    if ($scope.submissions === undefined) {
      $scope.reload();
    }
    $scope.map.routes = [];
    $scope.map.editable = false;
  });

  $scope.reload = function() {
    $scope.loading++;
    var url = jQuery('#submissions').data('url-submissions');
    $http.get(url)
      .success(function(data) {
        data.submissions.sort(function(a, b) {
          return b.created - a.created;
        });
        $scope.submissions = data.submissions;
        $scope.loading--;
      });
  }

  $scope.showRoute = function(route) {
    $scope.$parent.showRoute(route.geojson.geometry.coordinates);
    $scope.active = route;
  }

  $scope.editRoute = function(route) {
  }

}]);

})(window.angkot.app);

