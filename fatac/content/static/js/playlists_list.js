/*
* playlist_list.js
* jQuery Plugin for listing playlists
* 2012.6.27 lpmayos
*
* @version 1.0
*
* Per fer servir aquest pluggin, cal:
*     - xxx
*
*/

funtion carrega_elements() {
    var resultatsPerPagina = 9999;

    $.getJSON(pathname + "returnOrderedList", function() {
    })
    .error(function() { alert("No s'ha pogut carregar la llista d'objectes"); })
    .complete(function( data ) {
        var llista_ids = [];
        llista_ids = jQuery.parseJSON( data.responseText );
        parametres_visualitzacio = {llista_ids: llista_ids['Ids'], visualitzacio: 'fitxa_home', pagina_actual: 1, resultats_per_pagina: resultatsPerPagina};
        $('#visual-portal-wrapper').get(0).parametres_visualitzacio = parametres_visualitzacio;
        parametres_visualitzacio_json = JSON.stringify(parametres_visualitzacio);
        var currentView = '';
        if (window.location.pathname.indexOf("sortingView") != -1) {
            currentView = 'orderPlaylistView';
        }
        else {
            currentView = 'playlistView';
        }

        $.post(pathname + currentView, {parametres_visualitzacio: parametres_visualitzacio_json}, function(data){
            $('div#zona_resultats').replaceWith(data);
        })
        .complete(function( data ){
            // The sortable list of objects
            if (currentView == 'orderPlaylistView')
            {
                $('#sortable').sortable({
                    update: function() {
                        pathname = getPath();
                        order = getOrder();

                        updateList(pathname.split('sortingView')[0], order);
                    }
                });
            }
        });
    });
}


function crea_scrolls() {
    // ordena els elements en files de 3 i inicialitza la funcionalitat per fer scroll

    $('.items_' + nom).replaceWith(data);
    //envolcallem cada 3 elements en un div, xq funcioni l'scrollable
    var fila_actual = 1;
    var nova_fila = 1;
    $('.scrollable_' + nom + ' .genericview_fitxa_home').each(function(i) {
        nova_fila = (parseInt(i/3) + 1);
        if (nova_fila !== fila_actual) {
            $('.scrollable_' + nom + ' .fila' + fila_actual).wrapAll( '<div class="fila fila' + fila_actual + '" />' );
            fila_actual = nova_fila;
        }
        $(this).addClass('fila' + nova_fila);
    });
    $('.scrollable_' + nom + ' .fila' + fila_actual).wrapAll( '<div class="fila fila' + fila_actual + '" />' );
    if (fila_actual === 1) {
        $('#scrollable_' + nom + ' .arrow_up').addClass("hidden");
        $('#scrollable_' + nom + ' .arrow_down').addClass("hidden");
    }
    $('.scrollable_' + nom).scrollable({api:true, vertical: true, mousewheel: true});
}

