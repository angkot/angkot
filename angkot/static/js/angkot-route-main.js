(function(app) {

var JAKARTA = [106.8294444, -6.1744444];
var INDONESIA = [[143.0419921875, 8.189742344383703], [93.8671875, -11.867350911459308]];

app.factory('transportationService', function() {
  return {
    province: undefined,
    city: undefined,
    company: undefined,
    number: undefined,
    origin: undefined,
    destination: undefined,

    reset: function() {
      this.province = undefined;
      this.city = undefined;
      this.company = undefined;
      this.number = undefined;
      this.origin = undefined;
      this.destination = undefined;
    },

    update: function(data) {
      if (data.province !== undefined) this.province = data.province;
      if (data.city !== undefined) this.city = data.city;
      if (data.company !== undefined) this.company = data.company;
      if (data.number !== undefined) this.number = data.number;
      if (data.origin !== undefined) this.origin = data.origin;
      if (data.destination !== undefined) this.destination = data.destination;
    }
  }
});

app.controller('MainController', ['$scope', '$http', '$location', '$timeout', 'modalService', 'mapService', 'transportationService', function($scope, $http, $location, $timeout, modalService, mapService, transportationService) {

  $scope.panel = undefined;
  $scope.modal = modalService;
  $scope.map = mapService;
  $scope.info = transportationService;
  $scope.loggingIn = false;

  $scope.init = function() {
    $scope.map.view = {
      center: JAKARTA,
      zoom: 13,
    }
    $scope.map.maxBounds = INDONESIA;
    $scope.map.fitRoutesToBounds = true;
    $scope.map.editable = false;
    $scope.showPanel('transportation-list');
    $scope.mapboxKey = jQuery('body').data('mapbox-key');
    $scope.contributorTermsUrl = jQuery('body').data('url-contributor-terms');
    loadProvinces();
    loadUserData();
  }

  $scope.onRouteChanged = function() {
  }

  $scope.search = function() {
    var q = jQuery.trim($scope.searchQuery);
    if (!q) return;

    var query = {
      format: 'json',
      json_callback: 'JSON_CALLBACK',
      q: q,
      countrycodes: 'ID',
    }

    var url = 'http://open.mapquestapi.com/nominatim/v1/search.php?' + jQuery.param(query);

    $http.jsonp(url)
      .success(function(data) {
        if (data.length == 0) {
          console.error('search not found');
        }
        else {
          var res = data[0];
          var bbox = [[res.boundingbox[2], res.boundingbox[0]],
                      [res.boundingbox[3], res.boundingbox[1]]];
          $scope.map.viewport = bbox;
        }
      });
  }

  $scope.resetMapCheck = function() {
    var msg = 'Apakah Anda yakin untuk menghapus semua data yang sudah ' +
              'Anda masukkan dan mengulangi dari awal?';
    if (confirm(msg)) {
      $scope.resetMap();
    }
  }

  $scope.resetMap = function() {
    $scope.$broadcast('map-reset');
  }

  $scope.$on('map-reset', function() {
    $scope.map.reset();
  });

  // transportation

  $scope.newTransportion = function() {
    $scope.showLogin(function() {
      $scope.modal.useSelector('#new-transportation-modal');
    }, 'new-transportation');
  }

  $scope.editTransportation = function(tid) {
    $scope.info.reset();
    $scope.map.info = undefined;
    $location.path('/'+tid);
    $scope.showPanel('data-form');
  }

  $scope.onRouteEditClicked = function(e) {
    $scope.$broadcast('route-edit-click');
  }

  // panel

  $scope.showPanel = function(name) {
    $scope.panel = name;
  }

  // provinces

  var loadProvinces = function() {
    var url = jQuery('body').data('url-province-list');
    $http.get(url)
      .success(function(data) {
        $scope.provinces = data.provinces;
      });
  }

  // account and login

  $scope.loginCallback = undefined;

  $scope.showLogin = function(callback, source) {
    var callback = callback || function() {}

    if ($scope.user) {
      callback();
      return;
    }

    $scope.loginCallback = function() {
      if ($scope.user) {
        callback();
      }
    }

    source = source || 'other';
    $scope.loginSource = source;
    $scope.modal.useSelector('#login-content', 'login');
  }

  $scope.popupLoginWindow = function(e, source) {
    // if ($scope.loggingIn) return; // FIXME!
    $scope.loggingIn = true;
    source = source || 'other';

    var url = e.currentTarget.href + '&aos=' + source;

    var opts = 'width=500,height=500,menubar=no,toolbar=no,alwaysRaised';
    var popup = window.open(url, 'angkot-account-auth', opts);

    popup.onbeforeunload = function(e) {
      $scope.$apply(function() {
        $scope.loggingIn = false;
      });
    }
  }

  var loadUserData = function(cb) {
    var url = jQuery('body').data('url-account-info');
    $timeout(function() {
      $http.get(url)
        .success(function(data) {
          if (data.authenticated === true) {
            $scope.user = data;
          }
          else {
            $scope.user = undefined;
          }

          if (cb) cb();
        });
      });
  }

  $scope.loginSuccess = function() {
    loadUserData(function() {
      var cb = $scope.loginCallback;
      $scope.loginCallback = undefined;
      $scope.modal.hide();

      if (cb) $timeout(cb, 0);
    });
  };

}]);

})(window.angkot.app);

(function(window) {

window.login_success = function() {
  var body = jQuery('body')[0];
  angular.element(body).scope().loginSuccess();
}

})(window);

