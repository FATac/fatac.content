
// http://www.extjs.com/forum/showthread.php?t=78424
// adds caret Functionalety to an Ext.Element
Ext.override(Ext.Element, {
    _iCaretNative: undefined,
    _isSupported: undefined,
    /**
     * @private
     */
    isCaretNative: function () {
        if (typeof this._isCaretNative == 'undefined') {
            var d = document,
            o = d.createElement("input");
            this._isCaretNative = "selectionStart" in o;
            this._isCaretSupported = this._isCaretNative || (o = d.selection) && !!o.createRange;
        }
        return this._isCaretNative
    },
    /**
     * @private
     */
    isSupported: function () {
        if (typeof this._isCaretSupported == 'undefined') {
            this.isCaretNative();
        }
        return this._isCaretSupported
    },
    /**
     * selects the text of the Element
     * @param {Mixed} start Start position of the selection 
     * @param {Number} end End position of the selection
     * @return {}
     */
    setCaret: function (start, end) {
        if (! (this.dom.nodeName.toLowerCase() == "textarea" || this.dom.nodeName.toLowerCase() == "input")) {
            return;
        }
        if (typeof start.start != 'undefined') {
            end = start.end;
            start = start.start;
        }
        if (this.isCaretNative()) {
            return this.dom.setSelectionRange(start, end)
        } else {
            var o = this.dom;
            var t = o.createTextRange();
            end -= start + o.value.slice(start + 1, end).split("\n").length - 1;
            start -= o.value.slice(0, start).split("\n").length - 1;
            t.move("character", start),
            t.moveEnd("character", end),
            t.select();
        }
    },
    /**
     * returns the current Selection of the Element
     * @return {Object} {start: startposition, end: endposition} of the selection
     */
    getCaret: function () {
        var o = this.dom;
        if (this.isCaretNative()) {
            return {
                start: o.selectionStart,
                end: o.selectionEnd
            }
        } else {
            var s = (this.dom.focus(), document.selection.createRange()),
            r,
            start,
            end,
            value; // the current selection range is not part of the controll asking for the caret...
            if (s.parentElement() != o) return {
                start: 0,
                end: 0
            };
            var isTA = o.nodeName.toLowerCase() == "textarea";
            if (isTA ? (r = s.duplicate()).moveToElementText(o) : r = o.createTextRange(), !isTA) return r.setEndPoint("EndToStart", s),
            {
                start: r.text.length,
                end: r.text.length + s.text.length
            };
            for (var $ = "[###]";
            (value = o.value).indexOf($) + 1; $ += $);
            r.setEndPoint("StartToEnd", s),
            r.text = $ + r.text,
            end = o.value.indexOf($);
            s.text = $,
            start = o.value.indexOf($);
            if (document.execCommand && document.queryCommandSupported("Undo")) for (r in {
                0: 0,
                0: 0
            }) document.execCommand("Undo");
            return o.value = value,
            this.setCaret(start, end),
            {
                start: start,
                end: end
            };
        }
    },
    /**
     * Returns the caret Plus the Line, Column nummer and the position Number
     * @return {}
     */
    getCaretPosition: function () {
        if (! (this.dom.nodeName.toLowerCase() == "textarea" || this.dom.nodeName.toLowerCase() == "input")) {
            return;
        }
        var c = this.getCaret(),
        o = this.dom;
        if (c) {
            var lines; // = (typeof o.value != 'undefined') ? o.value.split("\n") : o.innerText.split("\n");
            if (typeof o.value != 'undefined') {
                lines = o.value.split("\n");
            } else {
                lines = o.innerText.split("\n");
            }
            c.lines = lines.length;
            var p = c.start,
            ll = c.lines,
            len = 0,
            line = 0;
            for (; line < ll; line++) {
                len = lines[line].length + 1;
                if (p < len) break;
                p -= len;
            }
            line++;
            c.line = line;
            c.column = p;
            c.position = c.start;
        }
        return c;
    },
    /**
     * sets the CaretPosition 
     * @param {Number} start the beginnig of the selection
     * @param {Number} end the end of the selection
     */
    setCaretPosition: function (start, end) { // FIX start.start ? 
        if (typeof start.start != 'undefined') {
            end = start.end;
            start = start.start;
        }
        if (typeof start != 'undefined') {
            this.setCaret(start, end || start);
        }
    },
    /**
     * gets the current selected text
     * @return {}
     */
    getCaretText: function () {
        var o = this.getCaret();
        return (typeof this.dom.value != 'undefined') ? this.dom.value.slice(o.start, o.end) : '';
    },
    /**
     * overrides the currently selected Text with an other text
     * @param {String} text
     */
    setCaretText: function (text) {
        var o = this.getCaret(),
        i = this.dom,
        s = i.value;
        if (typeof s == 'undefined') {
            return;
        }
        i.value = s.slice(0, o.start) + text + s.slice(o.end);
        this.setCaret(o.start += text.length, o.start);
    }
}); 
