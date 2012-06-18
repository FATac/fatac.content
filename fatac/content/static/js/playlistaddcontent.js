/*
* playlist.addcontent.js
* jQuery Plugin for adding content to playlists
* 2012.6.12 lpmayos
*
* @version 1.0
*
* Per fer servir aquest pluggin, cal:
*     - al .pt carregar una imatge amb classe 'addPlaylist' i rel = id de l'objecte
*       que s'afegirà a la playlist
*     - executar la funció addPlaylistMenu(); en un punt on s'hagi carregat el codi
*       del pt
* Si es vol que la imatge estigui amagada i es mostri quan fem hover cal:
*     - afegir la classe addPlaylistParent a la caixa en la que volem fer hover, i
*       afegir la classe hidden a la imatge
*/

function addPlaylistMenu() {
    // afegeix el menú contextual per afegir a playlists a tots els elements amb
    // classe addPlaylist i activa la funcionalitat per mostrar i amagar botó quan
    // fem hover.

    $('.addPlaylist').each(function (i, element) {
        afageixPlaylistsMenu(element);
    });

    mostra_amaga_addPlaylistImage();
}

function afageixPlaylistsMenu(element) {
    // Afegeix a l'element donat el menú per afegir a playlist

    var titol;
    var idPlaylist;
    var llistaPlaylists;
    var idObjecte;
    var pathname = "";
    var menu = [
        {"Escull playlist":{onclick:function(){},disabled:true}},
        $.contextMenu.separator,
    ];

    // Assign handlers immediately after making the request,
    // and remember the jqxhr object for this request
    $.getJSON(pathname + "retornaPlaylists", function() {})
        .error(function() { alert("No s'ha pogut carregar el menu contextual"); })
        .complete(function( data ) {
            llistaPlaylists = jQuery.parseJSON( data.responseText );

            idObjecte = $(element).attr('rel');

            // variable global on guardarem un array amb els ids de les playlist en l'ordre
            // en que es pinten al desplegable, per construïr url_actualitzar en funció del
            // que guardem aquí i tenir-ho disponible en el moment que es cridi la funció
            if (!window._FATAC) {window._FATAC = {}; }
            _FATAC['playlists'] = []

            for (i=0; i<llistaPlaylists['titols'].length; i++) {
                var menuDict = new Object();
                titol = llistaPlaylists['titols'][i];
                idPlaylist = llistaPlaylists['ids'][i];

                // acualitzem variable global per poder consultar l'id quan cridem la funció
                _FATAC['playlists'].push(idPlaylist)

                menuDict[titol] = function(menuItem,menu) {
                    // quan cliquem la opció del menú, idPlaylist tindrà l'últim valor assignat,
                    // i la crida es farà malament. Per solucionar-ho, busquem idPlayist a
                    // variable global (index - 2 xq hi ha el títol i el separador)
                    var idPlaylist_aux = _FATAC['playlists'][$(menuItem).index() - 2]
                    var url_actualitzar = pathname + "actualitzaPlaylist?idPlaylist=" + idPlaylist_aux + "&idObjecte=" + idObjecte;;
                    $.ajax({url: url_actualitzar, type: "post", error: function(){alert("S'ha produït un error en afegir a la playlist. No s'han guardat els canvis");}
                });};
                menu.push(menuDict);
            }

            if (llistaPlaylists['titols'].length == 0) {
                menuDict['No hi ha playlist disponibles'] = {onclick:function(){},disabled:true};
            }

            $(element).contextMenu(menu, {theme:'default'});

        });

}

function mostra_amaga_addPlaylistImage() {
    // activa la funcionalitat de mostrar i amagar la imatge que, quan es clica,
    // desplega el menú contextual.
    // Per cada element amb classe addPlaylistParent:
    //  - onmousehover: mostrem imatge
    //  - onmouseout: si no hi ha menú desplegat, amaguem la imatge; si hi ha
    //    menú depslegat, fem que quan fem mouseout amagui imatge i amagui menú.

    // variable global per saber a quin addPlaylistParent estem fem hover
    _ADDPLAYLISTPARENT = '';

    $('.addPlaylistParent').hover(
        function () {
            $(this).find('.addPlaylist').removeClass("hidden");
            $(this).addClass("hover");
            _ADDPLAYLISTPARENT = $(this).attr('id');
        },
        function () {
            // si sortim del parent i no hi ha cap menú desplegat, amaguem
            // si sortim del parent i hi ha un menú desplegat, amaguem quan
            // tanquem el menú
            var menu_visible = $('.context-menu:visible');
            if($('.context-menu:visible').length != 0) {
                $(menu_visible).hover(
                    function () {},
                    function () {
                        $('#' + _ADDPLAYLISTPARENT).find('.addPlaylist:visible').addClass("hidden");
                        $($('.context-menu:visible').parents()[3]).attr('style', 'display:none;');
                        $('#' + _ADDPLAYLISTPARENT).removeClass("hover");
                        _ADDPLAYLISTPARENT = '';
                    }
                );
            } else {
               $(this).find('.addPlaylist').addClass("hidden");
               $(this).removeClass("hover");
                $('#' + _ADDPLAYLISTPARENT).removeClass("hover");
                _ADDPLAYLISTPARENT = '';

            }
        }
    );
}
