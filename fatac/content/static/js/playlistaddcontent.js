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
*
* TODO: lpmayos (traduïr comentaris!)
* TODO: lpmayos (quan no estàs identificat, peta xq intentem cridar una funció que no existeix des dels pt)
*
*/

function addPlaylistMenu() {
    // afegeix el menú contextual per afegir a playlists a tots els elements amb
    // classe addPlaylist i activa la funcionalitat per mostrar i amagar botó quan
    // fem hover.

    initPlaylistMenu();

    mostra_amaga_addPlaylistImage();
}

function recarregaPlaylistsMenu() {
    // esborra els menús per afegir a playlists i els torna a calcular

    esborrarPlaylistMenu();
    initPlaylistMenu();
}

function esborrarPlaylistMenu() {
    // esborrar tots els menús per afegir a playlists

    $('.context-menu-shadow').remove();
    $('table').each(function (i, element) {
        if($(element).find('.context-menu').length > 0) {
            $(element).remove();
        }
    });
}

function initPlaylistMenu() {
    // crida la vista retornaPlaylists per obtenir un llistat de les
    // playlists disponibles, i afegeix el menú per cada element amb
    // classe addPlaylist

    var llistaPlaylists;
    var pathname = "";

    $.getJSON(pathname + "retornaPlaylists", function() {})
    .error(function() { alert("No s'ha pogut carregar el menu contextual"); })
    .complete(function( data ) {
        llistaPlaylists = jQuery.parseJSON( data.responseText );

        $('.addPlaylist').each(function (i, element) {
            afageixPlaylistsMenu(element, llistaPlaylists);
        });

        //afegeixSlidersMenus();

    });
}

// TODO: lpmayos (arreglar funció, xq no funciona, i cridar des de initPlaylistMenu)
function afegeixSlidersMenus() {
    // afegeix slider vertical a les opcions del menú desplegable
    // per afegir els elements a les playlist

    $('.context-menu').each(function(i, element) {
        if($(element).find('.slider_vertical').length == 0) {
            var identificador = 'menu_playlist_' + (i);
            $(element).find('.context-menu-item').wrapAll('<div class="div_interior" />');
            $(element).find('.div_interior').wrap('<div class="laura" id="' + identificador + '" />');
            $(element).find('.laura').wrap('<div class="slider_vertical" style="height:150px;" />');
        }
    });

    $('.laura').each(function(i, element) {
        var identificador = $(element).attr('id');
        crea_scroll_vertical(identificador);
    });

}

function afageixPlaylistsMenu(element, llistaPlaylists) {
    // Afegeix a l'element donat el menú per afegir a playlist, generat
    // a partir de llistaPlaylist

    // _ és una funció definida a fatac.js que retorna l'entrada del
    // diccionari corresponent a l'idioma actual.
    text_afegir_a = _({'ca': 'Afegir a:',
                     'en': 'Add to:',
                     'es': 'Añadir a:'});
    text_error_afegir = _({'ca': "S'ha produït un error. No s'han guardat els canvis",
                           'en': 'An error occurred. No changes have been saved.',
                           'es': 'Se ha producido un error. No se han guardado los cambios.'});
    text_element_afegit = _({'ca': 'element afegit correctament',
                             'en': 'element added',
                             'es': 'elemento añadido correctamente'});
    text_error_playlist = _({'ca': "S'ha produït un error. No s'ha pogut recuperar l'identificador de la nova playlist",
                             'en': 'An error occurred. Unable to retrieve the new playlist identifier.',
                             'es': 'Se ha producido un error. No se ha podido recuperar el identificador de la nueva playlist.'});
    text_nou_album = _({'ca': 'Crear Playlist',
                        'en': 'Crear Playlist',
                        'es': 'Add Playlist'});

    var titol;
    var idPlaylist;
    var idObjecte;
    var pathname = "";

    var menu = []
    var menuDict = new Object();
    menuDict[text_afegir_a] = {onclick:function(){},disabled:true}
    menu.push(menuDict);

    idObjecte = $(element).attr('rel');

    // variable global on guardarem un array amb els ids de les playlist en l'ordre
    // en que es pinten al desplegable, per construïr url_actualitzar en funció del
    // que guardem aquí i tenir-ho disponible en el moment que es cridi la funció
    if (!window._FATAC) {window._FATAC = {}; }
    _FATAC['playlists'] = []

    // afegim al menú el llistat de playlist
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
            var idPlaylist_aux = _FATAC['playlists'][$(menuItem).index() - 1]
            console.error(idPlaylist_aux);
            var url_actualitzar = pathname + "actualitzaPlaylist?idPlaylist=" + idPlaylist_aux + "&idObjecte=" + idObjecte;;
            $.ajax({url: url_actualitzar, type: "post",
            error: function(){alert(text_error_afegir);},
            complete: function(){
                $('<div class="purr"><div class="info"><span>'+text_element_afegit+'</span></div></div>').purr({
                    fadeInSpeed: 200,
                    fadeOutSpeed: 200,
                    removeTimer: 2000,
                });
            }
        });};
        menu.push(menuDict);
    }


    // afegim al menú opció per afegir a una nova playlist)
    var menuDict2 = new Object();
    menuDict2[text_nou_album] = function(menuItem,menu) {

        // quan cliquem la opció del menú, idPlaylist tindrà l'últim valor assignat,
        // i la crida es farà malament. Per solucionar-ho, busquem idPlayist a
        // variable global (index - 2 xq hi ha el títol i el separador)
        var idPlaylist_aux = _FATAC['playlists'][$(menuItem).index() - 2]

        // creem link per executar l'overlay (el cridarem programaticament)
        var id_link = 'link_' + idObjecte;
        if($('.' + id_link).length == 0) {
            //$('body').append('<a class="' + id_link + ' link-overlay hidden" href="/fatac/Members/admin/++add++fatac.playlist">add</a>')
            $('body').append('<a class="' + id_link + ' link-overlay hidden" href="afegirPlaylist">add</a>')
        }

        // fem que l'overlay carregui el formulari per crear nova playlist,
        // sense redirigir a la pàgina de 'playlist creat correctament' quan
        // enviem el form; un cop creada la nova playlist afegim l'element a
        // la nova playlist, tanquem overlay, mostrem avís i actualitzem
        // llistats playlist
        $('.' + id_link).prepOverlay({
            subtype: 'ajax',
            filter: common_content_filter,
            formselector: 'form#form',
            closeselector: '#form-buttons-cancel',
            redirect: function () {
                var href = location.href;
                return href;
            },
            noform: function (el) {
                $.getJSON(pathname + "retornaIdUltimaPlaylist", function() {})
                .error(function() { alert(text_error_playlist); })
                .complete(function( data ) {
                    var idPlaylist_nova = jQuery.parseJSON( data.responseText );
                    //var idPlaylist_nova = 'playlist4';
                    var url_actualitzar = pathname + "actualitzaPlaylist?idPlaylist=" + idPlaylist_nova + "&idObjecte=" + idObjecte;;
                    $.ajax({url: url_actualitzar, type: "post",
                        error: function(){alert(text_error_afegir);},
                        complete: function(){

                            recarregaPlaylistsMenu();

                            $('.close a').click();

                            $('<div class="purr"><div class="info"><span>'+text_element_afegit+'</span></div></div>').purr({
                                fadeInSpeed: 200,
                                fadeOutSpeed: 200,
                                removeTimer: 2000,
                            });
                        }
                    });
                });
            }
        });

        $('.' + id_link).click();
    };
    menu.push($.contextMenu.separator);
    menu.push(menuDict2);

    $(element).contextMenu(menu, {theme:'default'});
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
