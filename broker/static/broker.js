$(document).ready(function() {
    
    $("#content-2").hide();

    $("#btn-group").click(function(){
	$("#content-2").hide();
	$("#content").show();
    });

    $("#btn-ranking").click(function(){
	$("#content").hide();
	$("#content-2").show();
    });
});
