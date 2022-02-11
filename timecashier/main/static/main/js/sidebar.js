$(document).ready(function(){
    $("#sidebarCollapse").on('click', function(){
    if($("#sidebar").is(":visible")){
        $("#sidebar").toggleClass('collapse');
        $(".grid-container").css("grid-template-columns", "0px 1fr 100px");
     }else{
        $("#sidebar").toggleClass('collapse');
        $(".grid-container").css("grid-template-columns", "220px 1fr 100px");
     }
      return false;


//    $(".grid-container").toggleClass('red');
    });
});