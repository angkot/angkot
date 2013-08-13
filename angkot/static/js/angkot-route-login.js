(function(app) {

app.controller('LoginController', ['$scope', function($scope) {

  $scope.active = false;

  var popup = undefined;

  $scope.popupLoginWindow = function(e) {
    if ($scope.active) return;
    $scope.active = true;

    var url = e.currentTarget.href;

    var opts = 'width=500,height=500,menubar=no,toolbar=no,alwaysRaised';
    popup = window.open(url, 'angkot-account-auth', opts);

    popup.onbeforeunload = function(e) {
      $scope.$apply(function() {
        $scope.active = false;
      });
    }
  }

  $scope.$on('login-success', function() {
    if ($scope.modal.name !== 'login') return;

    $scope.modal.hide();
  });

}]);

})(window.angkot.app);

(function(window) {

window.login_success = function() {
  console.log('login success');
  var body = jQuery('body')[0];
  angular.element(body).scope().loginSuccess();
}

})(window);

