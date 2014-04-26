L.Tooltip = L.Class.extend({
  initialize: function() {
  },

  onAdd: function(map) {
    this._map = map;
    this._popupPane = map._panes.popupPane;
    this._container = L.DomUtil.create('div', 'leaflet-tooltip', this._popupPane);
    this._container.style.display = 'none';
    this._updateContent();
  },

  onRemove: function(map) {
    this._popupPane.removeChild(this._container);
    delete this._container;
    delete this._popupPane;
    delete this._map;
  },

  addTo: function(map) {
    map.addLayer(this);
  },

  setTitle: function(title) {
    this._title = title;
    this._updateContent();
    this.redraw();
  },

  setContent: function(content) {
    this._content = content;
    this._updateContent();
    this.redraw();
  },

  clear: function() {
    this._title = null;
    this._content = null;
    this._updateContent();
    this.redraw();
  },

  _updateContent: function() {
    if (!this._container) return;

    var html = '';
    if (this._title) html += '<div class="title">' + this._title + '</div>';
    if (this._content) html += '<div class="content">' + this._content + '</div>';
    this._container.innerHTML = html;
  },

  setLatLng: function(latlng) {
    this._latlng = latlng;
    this.redraw();
  },

  redraw: function() {
    if (!this._container || !this._map || this._container.innerHTML === '' || !this._latlng) {
      this._container.style.display = 'none';
      return;
    }

    this._container.style.display = 'block';
    var pos = this._map.latLngToLayerPoint(this._latlng);
    L.DomUtil.setPosition(this._container, pos);
  },
});

