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

  $httpProvider.defaults.headers.post["Content-Type"] = "application/x-www-form-urlencoded";
  // Source: http://stackoverflow.com/a/18156756
  $httpProvider.defaults.xsrfCookieName = 'csrftoken';
  $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';

}]);

angkot.app = app;

})(window.angkot);

