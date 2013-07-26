(function(app) {

var JAKARTA = [-6.1744444, 106.8294444];

app.controller('MainController', ['$scope', function($scope) {

  $scope.init = function() {
    $scope.center = JAKARTA;
    $scope.zoom = 12;
    $scope.routes = [];
  }

  $scope.$watch('zoom', function(value) {
    console.log('main: zoom', value);
  });
  $scope.$watch('center', function(value) {
    console.log('main: center', value);
  });

  $scope.$watch('routes', function(value) {
    console.log('routes updated');
  }, true);

}]);

})(window.angkot.route.app);

