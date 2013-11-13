$(document).ready(function() {
	/* sort the teams based on the registered prices -- descending order*/
	var teams = [];
	$("tr[name=team]").each(function(){
		teams.push([$(this).find("td[name=price]").html().replace(",","."),$(this).find("td[name=name] a").html()]);
	});
	teams.sort(function(a,b) {return Number(b[0]) - Number(a[0]);});
	/* end of sort */
	
	$("#content-2").hide();

	/*make the ranking visualization*/
	$.each(teams,function(idx,val){
		$("tbody[name=content-2]").append('<tr><td>'+Number(idx+1)+'</td><td name="name-2"><a href="book">'+val[1]+'</a></td><td name="price-2" class="text-right">'+val[0].replace(".",",")+'</td></tr>');
  });
    
  $("#btn-group").click(function(){
    $("#content-2").hide();
    $("#content").show();
  });

  $("#btn-ranking").click(function(){
    $("#content").hide();
    $("#content-2").show();
  });

  $('tr[name=team]').click( function() {
    window.location = $(this).find('a').attr('href');
  }).hover( function() {
    $(this).toggleClass('hover');
  });
  
  
});
