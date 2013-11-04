var qty = 0;
var price = 0;
var tipoOrdem = "";

function getDecimalValue(s){
    return parseFloat(s.replace(/\,/,".")).toFixed(2);
}

function calcTotalPrice(){
    return accounting.formatMoney(parseFloat($("#formPreco").val().replace(/\,/,"."))*Number($("#formQtde").val()),"",2,".",",");
}

function validateFields(){
//TODO
//    $("#formPreco").val();
 //   $("#formPreco").val();
}

function toggleBtn(data){
  if (data == "" || data == NaN){
    $("#enviaOrdem").addClass('disabled');
  }else{
    $("#enviaOrdem").removeClass('disabled');
  }
}

function generateBook(buy,sell,last,prices){
    /*Função geradora da exibição do book*/
    /*preenche a tabela do book*/
    for(i=0;i<prices['buy'].length;i++) buy.append('<tr><td class="text-center">'+prices["buy"][i][1]+'</td><td class="text-right">'+accounting.formatMoney(prices["buy"][i][0],"",2,".",",")+'</td></tr>');
    for(i=0;i<prices['sell'].length;i++) sell.append('<tr><td class="text-left">'+accounting.formatMoney(prices["sell"][i][0],"",2,".",",")+'</td><td class="text-center">'+prices["sell"][i][1]+'</td></tr>');
    /*TODO - requisicao de last value, está vindo 99.99 fixo*/
    last.text(accounting.formatMoney(prices["last"],"",2,".",","));
}

$(document).ready(

	function() {
	$.get( "http://127.0.0.1:8000/api/get_book/"+decodeURIComponent(window.location.pathname).split('/')[3])
    .done(function(data){
  	/* generate the book */
		generateBook($("tbody[name=buy-side]"), $("tbody[name=sell-side]"),	$("span[name=last]"), data)
  });

	/* clear the form */
	$("#formPreco").val("");
	$("#formQtde").val("");

	/* refresh the total price */
	$(".form-control").on("keyup onpaste", function() {
		validateFields();
		if ($("#formPreco").val() == "" || $("#formQtde").val() == "") {
			$("#precoTotal").text("");
		} else {
			$("#precoTotal").text(calcTotalPrice());
		}
	  toggleBtn($("#precoTotal").text());
	});

	/* put the information on modal window */
	$("#enviaOrdem").click(
		function() {
			if ($("input[name=tipoOrdem]").is(":checked")){
        $("#tipoOrdem").text("Compra");
        tipoOrdem = 'C';
      }else{
        $("#tipoOrdem").text("Venda");
        tipoOrdem = 'V';
      }
      price = getDecimalValue($("#formPreco").val());
      alert('price : '+price);
      $("p[name=modalPreco]").text(price);
      qty = $("#formQtde").val();
			$("p[name=modalQtde]").text(qty);
			$("p[name=modalTotal]").text($("#precoTotal").text());
	});
    

  /*Place the order*/
  $("button[name=confirmaOrdem]").click(function(){
  /*user e stock chumabada ticker = decodeURIComponent(window.location.pathname).split('/')[3] */
    $.post( "http://127.0.0.1:8000/api/new_order/",{'user_id':3,'ticker_id':1, 'order_type':tipoOrdem,'order_qty':qty,'order_value': price})
      .done(function(data){
  	  /* generate the order */ 
      /*TODO - Wait interface and auto-close*/
        alert('operação concluida com sucesso');
        /*alert(JSON.stringify(data));*/
		    })
      .fail(function(data) {
        alert( "error" );
        alert(JSON.stringify(data));
      })
  });


  /*Order validations*/
  /* auto-refresh*/
	$("#formPreco").on("keyup", function() {
		// change to use accounting js library
		$(this).val($(this).val().replace(/\./, ","));
	});

	/*enable-disable "Comprar" button*/
  $("#precoTotal").change(function(){
    alert('mudou');

  });
        

});
