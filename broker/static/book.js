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

/*enable / disable "Comprar" btn */
function toggleBtn(data){
  if (data == "" || data == NaN){
    $("#enviaOrdem").addClass('disabled');
  }else{
    $("#enviaOrdem").removeClass('disabled');
  }
}

/*Função geradora da exibição do book*/
function generateBook(buy,sell,last,prices){
    /*preenche a tabela do book*/
    for(i=0;i<prices['buy'].length;i++) buy.append('<tr><td class="text-center">'+prices["buy"][i][1]+'</td><td class="text-right">'+accounting.formatMoney(prices["buy"][i][0],"",2,".",",")+'</td></tr>');
    for(i=0;i<prices['sell'].length;i++) sell.append('<tr><td class="text-left">'+accounting.formatMoney(prices["sell"][i][0],"",2,".",",")+'</td><td class="text-center">'+prices["sell"][i][1]+'</td></tr>');
    /*TODO - requisicao de last value, está vindo 99.99 fixo*/
    last.text(accounting.formatMoney(prices["last"],"",2,".",","));
}

function modalFill(msg,img,type){
  content = '<div class="row text-center">';
  if (type) { content += '<div class="alert alert-'+type+'">' }
  if (msg)  { content += '<p><strong>'+msg+'</strong></p>'; }
  if (img)  { content += '<img src="'+img+'" />'; }
  if (type) { content += '</div>' }
  content += '</div>';
  return content;
}

/* clear the form */
function clearForm(){
	$("#formPreco").val("");
	$("#formQtde").val("");
  $("#precoTotal").text("");
	return
}

/*TODO pq está dando refresh com varios itens? */
function get_book(stock){
	$.get("http://localhost:8000/api/get_book/"+stock+"/?size=5")
    .done(function(data){
  	/* generate the book */
		generateBook($("tbody[name=buy-side]"), $("tbody[name=sell-side]"),	$("span[name=last]"), data)
  });
  return
}

$(document).ready(function() {
  var stock = decodeURIComponent(window.location.pathname).split('/')[3];
  clearForm();
  
  get_book(stock);
  
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
      $("p[name=modalPreco]").text(price);
      qty = $("#formQtde").val();
			$("p[name=modalQtde]").text(qty);
			$("p[name=modalTotal]").text($("#precoTotal").text());
	});
    

  /*Place the order*/
  $("button[name=confirmaOrdem]").click(function(){
  /*user e stock chumabada ticker = decodeURIComponent(window.location.pathname).split('/')[3] */
    /*TODO fix the host (pegar da sessao, cookie, etc)*/
    $.post( "http://localhost:8000/api/new_order/",{'user_id':3,'ticker_id':1, 'order_type':tipoOrdem,'order_qty':qty,'order_value': price})
      .always(function(){
        $(".modal-body").html(modalFill(NaN,'/images/ajax-loader.gif'));
      })
      .done(function(data){
  	  /* generate the order */ 
      /*TODO - Wait interface and auto-close & use the data to process the status*/
        $(".modal-body").html(modalFill('Ordem enviada com sucesso.',NaN,'success'));
        /* clear the form */
        clearForm();
        get_book(stock);
	    })
      .fail(function(data) {
        /*TODO process the data from error not a fixed msg*/
        $(".modal-body").html(modalFill('Não foi possível enviar sua ordem<br/>Tente Novamente.',NaN,'danger'));
        alert(JSON.stringify(data));
      })
  });


  /*Order validations*/
  /* auto-refresh*/
	$("#formPreco").on("keyup", function() {
		// change to use accounting js library
		$(this).val($(this).val().replace(/\./, ","));
	});
	



});
