$(document).ready(function() {
	/* calculate the total prices*/
	var teams = [];
	var total = 0;
	var _total = 0;
	$("tr[name=team]").each(function(){
		_total = parseFloat($(this).find("td[name=price]").html().replace(",",".")) * Number($(this).find("td[name=quantity]").html());
		$(this).find("td[name=total]").html(accounting.formatMoney(_total,"",2,".",","));
		total += _total;
	});
	
	$("td[name=totalSum] strong").html(accounting.formatMoney(total,"",2,".",","));
	/*put the totals in the right place*/

});
