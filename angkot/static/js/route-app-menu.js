(function(app) {

app.controller('MenuController', ['$scope', function($scope) {

  $scope.showAbout = function() {
    $scope.showModal({
      show: true,
      title: 'Apa ini?',
      content: '<p>Situs ini memiliki misi untuk mengumpulkan seluruh rute/trayek ' +
               'angkuan umum yang ada di Indonesia dan menjadi tempat rujukan ' +
               'alternatif pencarian rute.</p> ' +
               '<p>Situs ini dibuat seperti <a href="http://www.wikipedia.org" target="_blank">Wikipedia</a> ' +
               'sehingga siapapun dapat ikut serta memasukkan dan menyempurnakan data ' +
               'yang ada. Data rute yang dikumpulkan bersifat publik dan dapat digunakan ' +
               'untuk kepentingan apa saja, selama sesuai dengan ' +
               '<a href="http://creativecommons.org/licenses/by-sa/3.0/deed.id">ketentuan penggunaan data</a>.</p>',
    });
  }

}]);

})(window.angkot.app);

