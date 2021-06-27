function getCookie(c_name)
{
    if (document.cookie.length > 0)
    {
        c_start = document.cookie.indexOf(c_name + "=");
        if (c_start != -1)
        {
            c_start = c_start + c_name.length + 1;
            c_end = document.cookie.indexOf(";", c_start);
            if (c_end == -1) c_end = document.cookie.length;
            return unescape(document.cookie.substring(c_start,c_end));
        }
    }
    return "";
}

$(document).on('click','#delete',function(event){
    url = $(this).data('link');
    card = $(this).data('card');
    modal = "#Modal_" + card;
    card = "#"+card;
    $.ajax({
        type: 'POST',
        url: url,
        success: function() {
            $(modal).modal('hide');
            $(modal).on('hidden.bs.modal', function(){
                $(card).remove();
            });
        },
        headers: { "X-CSRFToken": getCookie("csrftoken") }
    });
});