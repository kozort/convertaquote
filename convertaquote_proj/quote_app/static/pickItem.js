$(document).ready(function()
{
    $('#accordianItem1').click(function()
    { 
        $.ajax
        ({
            method: "POST",   
            url: "/quote/pickitem/1",
        })
        .done(function(response)
        {
            $('#optionsTable').html(response)  
        })
        return false
    })

})

