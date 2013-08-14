(function(app) {

app.controller('MenuController', ['$scope', function($scope) {

  $scope.showAbout = function() {
    $scope.modal.showFromSelector('#about-content');
  }

  $scope.showContact = function() {
    $scope.modal.showFromSelector('#contact-content');
  }

}]);

})(window.angkot.app);

