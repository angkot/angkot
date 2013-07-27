(function(app) {

app.controller('MenuController', ['$scope', function($scope) {

  $scope.showAbout = function() {
    $scope.showModalFrom('#about-content');
  }

  $scope.showContact = function() {
    $scope.showModalFrom('#contact-content');
  }

}]);

})(window.angkot.app);

