$(document).ready(function()
{
    $('body').on('click' , 'div', (function()
    {
        this_id = $(this).attr("id");
        console.log('this_id: '+this_id)
        if (typeof this_id !== 'undefined')
        {
            parsedArray = this_id.split("_",2);
            console.log('parsedArray[1]'+parsedArray[1])
            if (parsedArray[1] == "accordianItem")
            {
                $.ajax
                ({
                    method: "GET",   
                    url: "/quote/pickitem/"+parsedArray[0],
                })
                .done(function(response)
                {
                    $('#optionsTable').html(response)  
                })
                return false
            } 
            if (parsedArray[1] == "trash")
            {
                $.ajax
                ({
                    method: "GET",   
                    url: "/quote/updateitem/" + parsedArray[0] + "/remove",
                })
                .done(function(response)
                {
                    $('#optionsTable').html(response)  
                })
                return false
            }
            // update item qty
            if(parsedArray[1] == "itemQTYDiv")
            {
                updated_qty_ajax(parsedArray[0])
            } 
        }
    }))
    $('input').keyup(function()
    {
        console.log('keyup triggered')
        this_id = $(this).attr("id");
        console.log('this_id: '+this_id)
        if(parsedArray[1] == "itemQTYDiv")
        {
            updated_qty_ajax(parsedArray[0])
        }
    })
    // called by click and keyup actions
    function updated_qty_ajax(itemID)
    {
        var data = $("#" + itemID + "_itemQTY").serialize()
        $.ajax
        ({
            method: "POST",   
            url: "/quote/updateitem/" + itemID,
            data: data
        })
        .done(function(response)
        {
            $('').html(response)  
        })
        return false
    }

})

