/*
* playlist.addcontent.js
* jQuery Plugin for adding content to playlists
* 2012.6.12 lpmayos
*
* @version 1.0
*
*/

$(document).ready(function() {
    // quan ha carregat el document, executa addPlaylistsMenu

    addPlaylistMenu();
});

function addPlaylistMenu() {
    // afegeix el menú per afegir a playlists a tots els elements amb classe addPlaylist

    var menu;

    $('.addPlaylist').each(function (i, element) {
        afageixPlaylistsMenu(element);
    });
}

function afageixPlaylistsMenu(element) {
    // Afegeix a l'element donat el menú per afegir a playlist

    var titol;
    var idPlaylist;
    //var menuDict = new Object();
    var llistaPlaylists;
    var idObjecte;
    // faig les vistes retornaPlaylists i actualitzaPlaylist disponibles per Interface,
    // i per tant no cal pasar path xq les podem executar des d'on estem
    //var pathname = "http://localhost:8084/fatac/";
    var pathname = "";
    var menu = [
                {"Escull playlist":{onclick:function(){},disabled:true}},
                $.contextMenu.separator,
    ];

    // Assign handlers immediately after making the request,
    // and remember the jqxhr object for this request
    $.getJSON(pathname + "retornaPlaylists", function() {
    })
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
