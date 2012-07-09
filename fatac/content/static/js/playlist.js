$(document).ready(function() {

    var pathname = '';
    var order = [];

    pathname = getPath();

    // Assign handlers immediately after making the request,
    // and remember the jqxhr object for this request
    if ((window.location.pathname.indexOf("edit") == -1) &&
        (window.location.pathname.indexOf("@@edit") == -1))
    {
        resultatsPerPagina = 66;

        if (pathname.indexOf("sortingView") != -1)
        {
            pathname = pathname.split("sortingView")[0];
            resultatsPerPagina = 400;
        }

        response = drawOrderedList(pathname, resultatsPerPagina);

    }

/*
    // The sortable list of objects
    $('#sortable').sortable({
        update: function() {
            pathname = getPath();
            order = getOrder();

            updateList(pathname, order);
        }
    });
*/
    // Check and Uncheck all the selection
    $("#forRemove_all").click(function()
    {
        $("input[id$=forRemove]").each(function()
        {
            if (this.checked == false)
            {
                this.checked = true;
            }
            else
            {
                this.checked = false;
            }
        });
    });

    // Delete all the selection
    $("#deleteAll").click(function()
    {
        $("#sortable").children().each(function()
        {
            var inputChecked = jQuery(this).find("input")[0].checked;
            if (inputChecked == true)
            {
                jQuery(this).remove();
            }
        });

        pathname = getPath();
        order = getOrder();
        updateList(pathname, order);
    });


});

function drawOrderedList(pathname, resultatsPerPagina) {
    $.getJSON(pathname + "returnOrderedList", function() {})
        .error(function() { alert("No s'ha pogut carregar la llista d'objectes"); })
        .complete(function( data ) {

            // var llista_ids = ['Expedient_Ana_Mendieta', 'Expedient_Antoni_Tapies_Els_llocs_de_lart'];

            llista_ids = jQuery.parseJSON( data.responseText );

            parametres_visualitzacio = {llista_ids: llista_ids['Ids'], visualitzacio: 'imatge', zoom: '1', pagina_actual: 1, resultats_per_pagina: resultatsPerPagina};

            $('#visual-portal-wrapper').get(0).parametres_visualitzacio = parametres_visualitzacio;

            parametres_visualitzacio_json = JSON.stringify(parametres_visualitzacio);

            var currentView = '';
            if (window.location.pathname.indexOf("sortingView") != -1)
            {
                currentView = 'orderPlaylistView';
            }
            else
            {
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
                // Enable bind to be able to delete elements from the playlist
                $("#sortable").on("click", ".trashbin", function(event) {
                    event.preventDefault();
                    removeSelectedObject($(this).attr("data-id"), $(this).attr("data-order"));
                });
                }


            });
        });
};

// Returns the order of the sortable list
function getOrder()
{
    //Get new order
    var order = [];
    var serialized_order = $('#sortable').sortable('serialize');

    //Parse order and create an Array with the elements
    var raworder = serialized_order.split("&");
    var len = raworder.length;
    for (i=0;i<len;i++)
    {
        order.push(raworder[i].split("=")[1]);
    }

    return order;
}

// Parse url to get the correct path of the object
function getPath()
{
    //Get the current path
    var path = window.location.pathname;

    //Parse for different paths
    if (path.indexOf("view") != -1)
    {
        path = path.split("view")[0];
    }
    else if (path.indexOf("@@view") != -1)
    {
        path = path.split("@@view")[0];
    }
    else if (path[-1] != '/')
    {
        path = path + '/';
    }

    return path;
}


// Update the Ordered List of the current selected
function updateList(pathname, order)
{
    //Send the new List and update async.
    $.ajax({
        url: pathname + "updateList?order=[" + order + "]",
        type: "post",
        error: function(){alert("Ha donat un error al ordenar la llista! No s'han guardat els canvis");},
        success: function(){drawOrderedList(pathname, resultatsPerPagina)}
    });

}


function removeSelectedObject(objectId, tagObjectId)
{
    //Get the current path
    var pathname = getPath();

    //Parse for different paths
    if (pathname.indexOf("sortingView") != -1)
    {
        pathname = pathname.split("sortingView")[0];
    }
    else if (pathname[-1] != '/')
    {
        pathname = pathname + '/';
    }

    path = pathname + "deleteObjectId?objectId=" + objectId; //tagObjectId.replace("#","");

    $( "#dialog-confirm" ).dialog({
        resizable: false,
        height:200,
        width:350,
        modal: true,
        buttons: {
            "Esborra aquest element": function() {
                $.ajax({url: path,
                    type: "post",
                    error: function() { alert("No s'ha eliminat l'objecte de la playlist"); },
                    success: function() { //window.location.href = pathname + "sortingView";
                                            $(tagObjectId).remove();
                                        },
                });
                $( this ).dialog( "close" );
            },
            "Cancel·la": function() {
                $( this ).dialog( "close" );
            }
        }
    });

}
