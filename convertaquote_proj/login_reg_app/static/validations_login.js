$(document).ready(function()
{
    // first_name validation
    $('#first_name').keyup(function()
    {
        var data = $("#regForm").serialize()   
        $.ajax
        ({
            method: "POST",   
            url: "/signin/reg_validate/0",
            data: data
        })
        .done(function(response)
        {
            $('#first_nameMsg').html(response)  
        })
        return false
    })
    // last_name validation
    $('#last_name').keyup(function()
    {
        var data = $("#regForm").serialize()   
        $.ajax
        ({
            method: "POST",   
            url: "/signin/reg_validate/1",
            data: data
        })
        .done(function(response)
        {
            $('#last_nameMsg').html(response)  
        })
        return false
    })
    // email validation
    $('#email').keyup(function()
    {
        var data = $("#regForm").serialize()   
        $.ajax
        ({
            method: "POST",   
            url: "/signin/reg_validate/2",
            data: data
        })
        .done(function(response)
        {
            $('#emailMsg').html(response)  
        })
        return false
    })
    //password validation
    $('#password').keyup(function()
    {
        var data = $("#regForm").serialize()  
        $.ajax
        ({
            method: "POST",   
            url: "/signin/reg_validate/3",
            data: data
        })
        .done(function(response)
        {
            $('#passwordMsg').html(response)  
        })
        return false
    })
        //password confirmation validation
        $('#confirm_PW').keyup(function()
        {
            var data = $("#regForm").serialize()  
            $.ajax
            ({
                method: "POST",   
                url: "/signin/reg_validate/4",
                data: data
            })
            .done(function(response)
            {
                $('#confirm_PWMsg').html(response)  
            })
            return false
        })
})

