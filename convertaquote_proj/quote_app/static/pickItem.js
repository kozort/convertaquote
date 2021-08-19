$(document).ready(function()
{
    $('div').click(function()
    {
        this_id = $(this).attr("id");
        parsedArray = this_id.split("_",2);
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
    })
})

