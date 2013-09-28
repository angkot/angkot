(function(angkot) {

"use strict";

var app = angular.module('AngkotRoute', ['modal', 'angkotMap', 'angkotFilter']);

app.config(['$interpolateProvider', '$httpProvider', function($interpolateProvider, $httpProvider) {
  $interpolateProvider.startSymbol('((');
  $interpolateProvider.endSymbol('))');

  function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
  }

  // From: http://thomas.rabaix.net/blog/2013/05/csrf-token-security-with-angularjs
  $httpProvider.defaults.headers.common['X-CSRFToken'] = getCookie('csrftoken');
  $httpProvider.defaults.headers.post["Content-Type"] = "application/x-www-form-urlencoded";

}]);

angkot.app = app;

})(window.angkot);

