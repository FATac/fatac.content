$(document).ready(function() {
    var pathname = '';
    var order = [];

    // The sortable list of objects
    $('#sortable').sortable({ 
        update: function() {        
            pathname = getPath();
            order = getOrder();

            updateList(pathname, order);
        }                                         
    });

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
    $.ajax({url: pathname + "updateList?order=[" + order + "]", type: "post", error: function(){alert("Ha donat un error al ordenar la llista! No s'han guardat els canvis");}});
}


