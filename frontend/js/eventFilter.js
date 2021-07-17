$('#id_orderPlacementDate').change(function() {
    date = new Date(this.value)
    otherDate = new Date()
    otherDate.setDate(date.getDate() + 30)

    $(".filterEvent").each(function() {
        eventItem = $(this)
        eventDate = new Date(this.textContent)

        if(eventDate >= date && eventDate <= otherDate){
           $(this).removeAttr("hidden")         
        }else{
            $(this).attr("hidden", "")
        }

    })


})