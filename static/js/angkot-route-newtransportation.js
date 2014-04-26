(function(app) {

"use strict";

app.controller('NewTransportationController', ['$scope', '$http', function($scope, $http) {

  $scope.loading = 0;

  $scope.saveCheck = function() {
    $scope.error = null;
    $scope.incomplete = null;

    var valid = true;

    var focus = function(name) {
      jQuery('.new-transportation-form input[name="'+name+'"]').focus();
    };

    if (!$scope.province) {
      focus('province');
      valid = false;
    }

    if (valid && !$scope.city) {
      focus('city');
      valid = false;
    }

    if (valid && !$scope.number) {
      focus('number');
      valid = false;
    }

    if (valid && !$scope.termAgreement) {
      focus('term-agreement');
      valid = false;
    }

    $scope.incomplete = !valid;
    $scope.checked = true;

    if (valid) {
      $scope.save();
    }
  };

  $scope.save = function() {
    $scope.loading++;

    var data = {
      province: $scope.province,
      city: $scope.city,
      number: $scope.number,
      company: $scope.company,
      agreeToContributorTerms: $scope.termAgreement,
    };
    var url = jQuery('body').data('url-new-transportation');

    $scope.gaSendSubmitNewEvent();

    $http.post(url, jQuery.param(data))
      .success(function(data, status) {
        $scope.loading--;

        $scope.company = undefined;
        $scope.number= undefined;
        $scope.termAgreement = false;
        $scope.error = null;
        $scope.incomplete = null;
        $scope.checked = false;

        $scope.edit(data.id);
      })
      .error(function(data, status) {
        console.error('fail', status, data);
        $scope.loading--;
      });
  };

  $scope.gaSubmitNewCount = 0;

  $scope.gaSendSubmitNewEvent = function() {
    $scope.gaSubmitNewCount++;
    $scope.ga('send', 'event', 'transportation-new', 'submit',
              {eventValue: $scope.gaSubmitNewCount});
  };

  $scope.edit = function(tid) {
    $scope.modal.hide();
    $scope.editTransportation(tid);
  };

  $scope.$watch('loading', function(value, old) {
    var btn = jQuery('.new-transportation-form button.btn.save');
    if (old === 0 && value > 0) {
      jQuery('.new-transportation-form input').attr('disabled', 'disabled');
      jQuery('.new-transportation-form select').attr('disabled', 'disabled');
      jQuery('.new-transportation-form button').attr('disabled', 'disabled');
      btn.text('mengecek data..');
    }
    else if (value === 0 && old > 0) {
      jQuery('.new-transportation-form input').removeAttr('disabled');
      jQuery('.new-transportation-form select').removeAttr('disabled');
      jQuery('.new-transportation-form button').removeAttr('disabled');
      btn.text('Simpan');
    }
  });

}]);

})(window.angkot.app);

