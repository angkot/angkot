(function(app) {

app.controller('SubmissionListController', ['$scope', '$http', function($scope, $http) {

  $scope.submissions = undefined;
  $scope.loading = 0;

  $scope.init = function() {
  }

  $scope.$watch('panel', function(value, old) {
    if (value !== 'submission-list') return;
    if ($scope.submissions === undefined) {
      $scope.reload();
    }
    $scope.map.editable = false;
    $scope.map.routes = [];
  });

  $scope.reload = function() {
    $scope.loading++;
    var url = jQuery('body').data('url-submission-list');
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
    $scope.map.routes = route.geojson.geometry.coordinates;
    $scope.active = route;
  }

  $scope.editRoute = function(route) {
  }

}]);

})(window.angkot.app);

