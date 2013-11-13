function getDecimalValue(s){
    return parseFloat(s.replace(/\,/,".")).toFixed(2);
}

function calcTotalPrice(){
    return accounting.formatMoney(parseFloat($("#formPreco").val().replace(/\,/,"."))*Number($("#formQtde").val()),"",2,".",",");
}

function getLastPrice(ticker){
/*	$.get( "http://localhost:8000/api/get_last_price/"+ticker)
    .done(function(data){
  		return data;
  	.fail(function(data) {
  	  alert(data);
  	}
  });*/
  return getDecimalValue('12.5');
}


function generatePortfolio(data){
  var _html = "";
  var total = 0;
  var available = Number(getDecimalValue($("span[name=available]").html()));
  $.each(data,function(i,e){
    _lastPrice = getLastPrice(e[0]);
    _html+= "<tr name='team'>";
    _html+="<td name='name'><a href='book/"+e[0]+"'>"+e[0]+"</a></td>";
    _html+="<td name='price' class='text-right'>"+accounting.formatMoney(_lastPrice,"",2,".",",")+"</td>";
    _html+="<td name='quantity' class='text-center'>"+e[1]+"</td>";
    _html+="<td name='total' class='text-right'>"+accounting.formatMoney(_lastPrice*e[1],"",2,".",",")+"</td>"+"</td>";
    _html+="</tr>";
    total += _lastPrice*e[1];
  });
  $("tbody[name=myStocks]").html(_html);

	/*put the totals in the right place*/
	$("span[name=stocksTotal]").html(accounting.formatMoney(total,"",2,".",","));
	$("span[name=total]").html(accounting.formatMoney(total+available,"",2,".",","));
}


$(document).ready(function() {

	$.get( "http://localhost:8000/api/get_user_portfolio/")
    .done(function(data){
    /* generate the book */
    generatePortfolio(data);
  })
       
});
