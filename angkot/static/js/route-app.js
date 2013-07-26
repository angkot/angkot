(function(angkot) {

var app = angular.module('AngkotRouteEditor', []);

app.config(function($interpolateProvider, $httpProvider) {
  $interpolateProvider.startSymbol('((');
  $interpolateProvider.endSymbol('))');

  // From: http://thomas.rabaix.net/blog/2013/05/csrf-token-security-with-angularjs
  $httpProvider.defaults.headers.common['X-CSRFToken'] = jQuery('input[name=csrfmiddlewaretoken]').attr('value');
  $httpProvider.defaults.headers.post["Content-Type"] = "application/x-www-form-urlencoded";
});

angkot.route.app = app;

})(angkot);

