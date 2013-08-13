(function(app) {

app.controller('MenuController', ['$scope', function($scope) {

  $scope.showAbout = function() {
    $scope.modal.showFromSelector('#about-content');
  }

  $scope.showContact = function() {
    $scope.modal.showFromSelector('#contact-content');
  }

  $scope.showLogin = function() {
    $scope.modal.useSelector('#login-content', 'login');
  }

}]);

})(window.angkot.app);

