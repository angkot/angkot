L.Angkot = {};

// Taken and modified from Leaflet 0.6.4
L.Draggable.include({
  _onDown: function(e) {
    // The following is commented for Angkot
    // if (e.shiftKey || ((e.which !== 1) && (e.button !== 1) && !e.touches)) { return; }

    L.DomEvent
      .stopPropagation(e);

    if (L.Draggable._disabled) { return; }

    L.DomUtil.disableImageDrag();
    L.DomUtil.disableTextSelection();

    var first = e.touches ? e.touches[0] : e,
        el = first.target;

    // if touching a link, highlight it
    if (L.Browser.touch && el.tagName.toLowerCase() === 'a') {
      L.DomUtil.addClass(el, 'leaflet-active');
    }

    this._moved = false;

    if (this._moving) { return; }

    this._startPoint = new L.Point(first.clientX, first.clientY);
    this._startPos = this._newPos = L.DomUtil.getPosition(this._element);

    L.DomEvent
        .on(document, L.Draggable.MOVE[e.type], this._onMove, this)
        .on(document, L.Draggable.END[e.type], this._onUp, this);
  },
});

