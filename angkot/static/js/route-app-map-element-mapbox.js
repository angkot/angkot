(function(angkot) {

"use strict"

var app = angkot.app;

app.directive('angkotMap', function() {

  var controller = ['$scope', '$element', function($scope, $element) {

    $scope.init = function() {
      initMap();
    }

    var map;

    var initMap = function() {
      var center = [$scope.center[1], $scope.center[0]];
      map = L.mapbox.map($element[0], $scope.mapboxKey)
        .setView(center, $scope.zoom);
    }

  }];

  return {
    restrict: 'E',
    template: '<div class="angkot-map"></div>',
    replace: true,
    controller: controller,
    scope: {
      mapboxKey: '=',
      center: '=',
      zoom: '=',
      routes: '=',
      viewport: '=',
      fitToBounds: '=',
      editable: '=',
    },
    link: function(scope, element, attrs) {
      scope.init();
    }
  };

});

})(window.angkot);

