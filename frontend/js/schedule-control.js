$('#all_btn').click(function() {
    filter(".event")
    $('#all_btn').addClass('active')
    $('#done_btn').removeClass('active')
    $('#not_done_btn').removeClass('active')
});
$('#done_btn').click(function() {
    filter(".done")
    $('#all_btn').removeClass('active')
    $('#done_btn').addClass('active')
    $('#not_done_btn').removeClass('active')
});
$('#not_done_btn').click(function() {
    filter(".not_done")
    $('#all_btn').removeClass('active')
    $('#done_btn').removeClass('active')
    $('#not_done_btn').addClass('active')
});
function filter(selector){
    var allElements = $(".event")
    var filteredElements = $(selector)
    
    allElements.each(function(){
        $(this).attr('hidden', '')
    })

    filteredElements.each(function(){
        $(this).removeAttr('hidden')
    })
}