(function(app) {

var JAKARTA = [-6.1744444, 106.8294444];

app.controller('MainController', ['$scope', function($scope) {

  $scope.init = function() {
    $scope.center = JAKARTA;
    $scope.zoom = 12;
    $scope.routes = [];
  }

  $scope.$watch('zoom', function(value) {
    // console.log('main: zoom', value);
  });
  $scope.$watch('center', function(value) {
    // console.log('main: center', value);
  });

  $scope.$watch('routes', function(value, old) {
    // console.log('routes updated');
    // console.log(old);
    // console.log(value);
  }, true);

}]);

})(window.angkot.route.app);

