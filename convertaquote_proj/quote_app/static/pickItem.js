$(document).ready(function()
{
    $('body').on('click' , 'div', (function()
    {
        this_id = $(this).attr("id");
        console.log('this_id='+this_id)
        console.log('thisclass='+$(this).attr("class"))
        if (typeof this_id !== 'undefined')
        {
            
            parsedArray = this_id.split("_",2);
            console.log('this_id='+this_id)
            console.log('parsedArray='+parsedArray)
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
        }
    }))
    


})

