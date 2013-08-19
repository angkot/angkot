(function(app) {

"use strict";

app.controller('MenuController', ['$scope', function($scope) {

  $scope.showAbout = function() {
    $scope.ga('send', 'event', 'menu', 'click-about');

    $scope.modal.showFromSelector('#about-content');
  };

  $scope.showContact = function() {
    $scope.ga('send', 'event', 'menu', 'click-contact');

    $scope.modal.showFromSelector('#contact-content');
  };

  $scope.showLogin = function() {
    $scope.ga('send', 'event', 'menu', 'click-login');

    $scope.$parent.showLogin(undefined, 'menu');
  };

}]);

})(window.angkot.app);

