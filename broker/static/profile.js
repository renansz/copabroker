function generatePortfolio(data){
    var _html = "";
    $.each(data,function(i,e){
        _html+= "<tr name='team'>";
	    _html+="<td name='name'><a href='book/"+e[0]+"'>"+e[0]+"</a></td>";
        _html+="<td name='price' class='text-right'></td>";
        _html+="<td name='quantity' class='text-center'>"+e[1]+"</td>";
        _html+="<td name='total' class='text-right'></td>";
        _html+="</tr>";
        /*_total = parseFloat($(this).find("td[name=price]").html().replace(",",".")) * Number($(this).find("td[name=quantity]").html());*/
    });
    $("tbody[name=myStocks]").html(_html);
	/*$("tr[name=team]").each(function(){

		$(this).find("td[name=total]").html(accounting.formatMoney(_total,"",2,".",","));
		total += _total;
	});
	$("span[name=total]").html(accounting.formatMoney(total,"",2,".",","));
	put the totals in the right place*/
}

$(document).ready(function() {
	/* calculate the total prices*/
	var teams = [];
	var total = 0;
	var _total = 0;

	$.get( "http://127.0.0.1:8000/api/get_user_portfolio/"+decodeURIComponent(window.location.pathname).split('/')[3])
        .done(function(data){
        	/* generate the book */
    		generatePortfolio(data)
        });

});
