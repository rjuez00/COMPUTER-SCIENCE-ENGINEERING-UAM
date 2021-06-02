$('.orderrow').hover(
    function () {
        console.log($(this).children().find(".infodesplegable"))
        $(this).find(".infodesplegable").css("display", "table-cell")
    }, 
    function() {
        $(this).find(".infodesplegable").css("display", "None")
    });
