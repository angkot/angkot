(function(app) {

var JAKARTA = [106.8294444, -6.1744444];

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

}]);

})(window.angkot.app);

