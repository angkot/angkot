L.Control.TransportationInfo = L.Control.extend({
  options: {
    position: 'topleft',
  },

  onAdd: function(map) {
    var html = '<p><span class="company"></span> <span class="number"></span>';
    html += '<p><span class="origin"></span> &ndash; <span class="destination"></span>';
    html += '<p class="route"></p>';
    html += '<p class="edit"><a href="http://google.com">edit</a></p>';

    var c = L.DomUtil.create('div', 'leaflet-transportation-info');
    c.innerHTML = html;
    this._update();
    this._c = c;

    var stop = L.DomEvent.stopPropagation;

    L.DomEvent
        .on(c, 'click', stop)
        .on(c, 'mousedown', stop)
        .on(c, 'dblclick', stop)
        .on(c, 'click', L.DomEvent.preventDefault)

    jQuery(c).find('> p.edit a').click(function() {
      console.log('edit');
    });

    return c;
  },

  setData: function(data) {
    this._data = data;
    this._update();
  },

  _getDistance: function(routes) {
    var distance = 0;
    for (var i=0; i<routes.length; i++) {
      var route = routes[i];
      if (route.length < 2) continue;

      var p = route[0];
      p = new L.LatLng(p[1], p[0]);
      for (var j=1; j<route.length; j++) {
        var n = new L.LatLng(route[j][1], route[j][0]);
        distance += p.distanceTo(n);
        p = n;
      }
    }
    console.log(routes);
    return distance;
  },

  _formatDistance: function(distance) {
    var text = (Math.round(distance / 1000 * 100) / 100) + ' km';
    if (distance < 1500)
      text = (Math.round(distance * 100) / 100) + ' km';
    return text;
  },

  _update: function() {
    var data = this._data;
    var c = jQuery(this._c);

    if (!data) {
      c.hide();
      return;
    }

    var info = data.properties || {};
    var route = data.geometry || {};

    c.show();

    var labels = {
      company: 'perusahaan',
      number: 'nomor',
      origin: 'lokasi berangkat',
      destination: 'jurusan',
    }

    var set = function(n) {
      c.find('.'+n).removeClass('empty');
      c.find('.'+n).text(info[n]);
    }

    var empty = function(n) {
      c.find('.'+n).addClass('empty');
      c.find('.'+n).text(labels[n]);
    }

    var update = function(n) {
      if (info[n]) set(n);
      else empty(n);
    }

    update('company');
    update('number');
    update('origin');
    update('destination');

    if (route.coordinates && route.coordinates.length > 0) {
      var distance = this._formatDistance(this._getDistance(route.coordinates));
      var text = route.coordinates.length + ' rute &ndash; ' + distance;
      c.find('.route').removeClass('empty');
      c.find('.route').html(text);
    }
    else {
      c.find('.route').addClass('empty');
      c.find('.route').text('gambar rute');
    }
  },
});

