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

/*Funcao para habilitar botao de enviar ordem*/
function enableSendBtn(_preco){
  /* enable send button by clickng buy or sell*/
  if ($("#compra").hasClass('active') || $("#venda").hasClass('active')) { 
    if (_preco == "" || _preco == NaN ) {
      $("#enviaOrdem").addClass('disabled');
    }else{
      $("#enviaOrdem").removeClass('disabled');
    }
  }
}

/*configura transicoes do painel buy and sell, e define o tipo de ordem*/
/*TODO deixar mais inteligente a function ^^ */
function toggleBuySell(){
  /*Buy*/
  $("label.btn-success").click(function(){
    $("#orderPanel").addClass('buyOption');
    $("#orderPanel").removeClass('sellOption');
    $("#bidTable").addClass("orderSelected");
    $("#askTable").removeClass("orderSelected");
    $("#enviaOrdem").removeClass("btn-warning");
    $("#enviaOrdem").addClass("btn-success");
    tipoOrdem = 'C'
    $("#compra").addClass('active')
    enableSendBtn($("#precoTotal").text());
  });
  /*Sell*/
  $("label.btn-warning").click(function(){
    $("#orderPanel").addClass('sellOption');
    $("#orderPanel").removeClass('buyOption');
    $("#askTable").addClass("orderSelected");
    $("#bidTable").removeClass("orderSelected");
    $("#enviaOrdem").removeClass("btn-success");
    $("#enviaOrdem").addClass("btn-warning");
    tipoOrdem = 'V'
    $("#venda").addClass('active')
    enableSendBtn($("#precoTotal").text());
  });
}

/*Função geradora da exibição do book*/
function generateBook(buy,sell,last,prices){
    /*limpa a tabela anterior*/
    buy.html("");
    sell.html("");
    
    /*preenche a tabela do book*/
    for(i=0;i<prices['buy'].length;i++) buy.append('<tr><td class="text-center">'+prices["buy"][i][1]+'</td><td class="text-right">'+accounting.formatMoney(prices["buy"][i][0],"",2,".",",")+'</td></tr>');
    for(i=0;i<prices['sell'].length;i++) sell.append('<tr><td class="text-left">'+accounting.formatMoney(prices["sell"][i][0],"",2,".",",")+'</td><td class="text-center">'+prices["sell"][i][1]+'</td></tr>');
    /*TODO - requisicao de last value, está vindo 99.99 fixo*/
    last.text(accounting.formatMoney(prices["last"],"",2,".",","));
    
    /*heightEqualizer();*/
}


/*atualiza altura do painel de Ordens*/
function heightEqualizer(){
  $("#orderPanel").css('height', function(){
    return $("#pricesPanel").css('height');
  });
  /*TODO Centralizar o conteudo do painel?*/
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
  $("#orderPanel").removeClass('buyOption sellOption');
  $(".orderSelected").removeClass('orderSelected');
  $("#enviaOrdem").addClass('disabled');
}


/*get the book calling the API*/
function get_book(stock){
	$.get("http://localhost:8000/api/get_book/"+stock+"/?size=5")
    .done(function(data){
  	/* generate the book */
		generateBook($("tbody[name=buy-side]"), $("tbody[name=sell-side]"),	$("span[name=last]"), data)
  });
}

/***************** Document Ready ***************/
/*TODO Textura para venda e compra, melhor que a cor pura*/
$(document).ready(function() {
  /* TODO O ticker fica dependente da URL, nao sei se isso é muito bom*/
  var stock = decodeURIComponent(window.location.pathname).split('/')[3];
  var modal = $(".modal-body").html();
  
  /*alert(JSON.stringify($.cookie()));*/
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
    enableSendBtn($("#precoTotal").text());
	});

  /*Buy and Sell buttons - Panel*/
  toggleBuySell();


	/* put the information on modal window */
	$("#enviaOrdem").click(function() {
      $(".modal-body").html(modal);
      $("h2[name=modalTipoOrdem]").text(function(){return tipoOrdem == "C"? "Ordem de Compra" : "Ordem de Venda" });
      $("p[name=modalPreco]").text(getDecimalValue($("#formPreco").val()));
			$("p[name=modalQtde]").text($("#formQtde").val());
			$("p[name=modalTotal]").text($("#precoTotal").text());
			
			
      /*Place the order*/
      $("button[name=confirmaOrdem]").click(function(){
        $.post( "http://localhost:8000/api/new_order/",{'ticker':stock, 'order_type':tipoOrdem,'order_qty': $("p[name=modalQtde]").text(), 'order_value': $("p[name=modalPreco]").text()})
          .always(function(){
            $(".modal-body").html(modalFill(NaN,'/static/images/ajax-loader.gif'));
          })
          .done(function(data){
	        /* generate the order */ 
            $(".modal-body").html(modalFill('Ordem enviada com sucesso.',NaN,'success'));
            /* clear the form */
            clearForm();
            get_book(stock);
            tipoOrdem = "";
          })
          .fail(function(data) {
            /*TODO process the data from error not a fixed msg*/
            $(".modal-body").html(modalFill('Não foi possível enviar sua ordem<br/>Tente Novamente.',NaN,'danger'));
            alert(JSON.stringify(data));
          })
      });
	});
    

  /*Order validations*/
  /* auto-refresh*/
	$("#formPreco").on("keyup", function() {
		// change to use accounting js library
		$(this).val($(this).val().replace(/\./, ","));
	});
	
});
