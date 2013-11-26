L.RouteDrawingLayer = L.LayerGroup.extend({
  includes: L.Mixin.Events,

  initialize: function(osm) {
    L.LayerGroup.prototype.initialize.call(this);

    this._osm = osm;
  },

  onAdd: function(map) {
    L.LayerGroup.prototype.onAdd.call(this, map);

    this._map.on({
      'click': this._onMapClick,
    }, this);
    this._osm.on({
      'osm:node:click': this._onNodeClick,
    }, this);
  },

  onRemove: function(map) {
    this._map.off({
      click: this._onMapClick,
    }, this);
    this._osm.off({
      'osm:node:click': this._onNodeClick,
    }, this);

    L.LayerGroup.prototype.onRemove.call(this, map);
  },

  // event handlers

  _onMapClick: function(e) {
    // console.log('map click', e);
    // this._addNode(e.latlng);
  },

  _onNodeClick: function(e) {
    console.log('node click', e.nodeId);
    var latlng = this._osm.nodes[e.nodeId];
    this._addNode(latlng);
    return true;
  },

  // draw

  _addNode: function(latlng) {
    if (!this._activeLine) {
      this._activeLine = new L.Polyline([], {color: '#FF0', opacity: 0.5, weight: 15});
      this._activeLine.addTo(this._map);
    }
    this._activeLine.addLatLng(latlng);
  },
});

