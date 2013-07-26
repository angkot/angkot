(function(app) {

app.filter('lengthUnit', function() {
  return function(value) {
    if (value < 1500) {
      return Math.round(value) + ' m';
    }
    return Math.round(value / 10) / 100 + ' km';
  }
});

})(window.angkot.route.app);

