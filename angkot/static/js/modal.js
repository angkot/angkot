(function() {

var mod = angular.module('modal', ['ngSanitize']);

mod.factory('modalService', function() {
  return {
    visible: false,
    title: undefined,
    content: undefined,
    selector: undefined,
    name: undefined,
    copy: true,

    show: function(content, title, name) {
      this.name = name || title;
      this.content = content;
      this.title = title;
      this.copy = true;
      this.visible = true;
    },

    showFromSelector: function(selector, name) {
      var c = jQuery(selector);
      if (c.length === 0) {
        console.error('Modal content not found: ' + selector);
        return;
      }
      var title = c.find('> h2').text();
      var content = c.find('> .content').html();
      this.show(content, title, name);
    },

    useSelector: function(selector, name) {
      var c = jQuery(selector);
      if (c.length === 0) {
        console.error('Modal content not found: ' + selector);
        return;
      }
      this.title = c.find('> h2').text();
      this.name = name || this.title;
      this.selector = selector;
      this.copy = false;
      this.visible = true;
    },

    hide: function() {
      this.visible = false;
    },
  }
});

mod.directive('modal', ['modalService', '$compile', function(modalService, $compile) {

  return {
    restrict: 'E',
    scope: {
      data: '=data',
      fireModalClosed: '&?onmodalclosed',
    },
    replace: true,
    templateUrl: '/static/partial/modal.html',
    controller: ['$scope', '$element', function($scope, $element) {
      $scope.close = function() {
        $scope.data.visible = false;
        if ($scope.fireModalClosed) {
          $scope.fireModalClosed();
        }
      }

      $scope.$watch('data.visible', function(value, old) {
        if (value === old) return;
        $scope.clear();
        if (value) {
          $scope.reload();
        }
      });

      $scope.clear = function() {
        if ($scope.selector) {
          var content = jQuery($element).find('> .c > .content').children();
          var c = jQuery($scope.selector);
          content.detach();
          c.find('> .content').append(content);
        }
        else {
          var c = jQuery($element).find('.c');
          c.find('> .title').html('');
          c.find('> .content').html('');
        }
        $scope.selector = undefined;
      }

      $scope.reload = function() {
        $scope.title = $scope.data.title;
        if ($scope.data.copy) {
          var html = $($scope.data.content);
          if (html.hasClass('compile')) {
            html = $compile(html)($scope);
          }
          jQuery($element).find('> .c > .content').html(html);
        }
        else {
          $scope.selector = $scope.data.selector;
          var c = jQuery($scope.selector);
          var content = c.find('> .content').children();
          content.detach();
          var e = jQuery($element).find('> .c > .content').append(content);
          e.show();
        }
      };
    }]
  }

}]);

})();

