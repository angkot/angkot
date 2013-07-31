(function(app) {

app.filter('lengthUnit', function() {
  return function(value) {
    if (value < 1500) {
      return Math.round(value) + ' m';
    }
    return Math.round(value / 10) / 100 + ' km';
  }
});

// From http://stackoverflow.com/a/17364716/252384
app.directive('ngEnter', function() {
  return function(scope, element, attrs) {
    element.bind("keydown keypress", function(event) {
      if(event.which === 13) {
        scope.$apply(function(){
          scope.$eval(attrs.ngEnter);
        });

        event.preventDefault();
      }
    });
  };
});

app.directive('eatClick', function() {
  return function(scope, element, attrs) {
    $(element).click(function(event) {
      event.stopPropagation();
    });
  }
})

})(window.angkot.app);

