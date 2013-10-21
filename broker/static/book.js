function getDecimalValue(s){
    return parseFloat(s).toFixed(2);
}

function calcTotalPrice(){
    return accounting.formatMoney(parseFloat($("#formPreco").val().replace(/\,/,"."))*Number($("#formQtde").val()),"",2,".",",");
}

function validateFields(){
//TODO
//    $("#formPreco").val();
 //   $("#formPreco").val();
}

function generateBook(buy,sell,last,prices){
    for(i=0;i<prices["buy"].length;i++) buy.append('<tr><td class="text-center">'+prices["buy"][i][1]+'</td><td class="text-right">'+accounting.formatMoney(prices["buy"][i][0],"",2,".",",")+'</td></tr>');
    for(i=0;i<prices["sell"].length;i++) sell.append('<tr><td class="text-left">'+accounting.formatMoney(prices["sell"][i][0],"",2,".",",")+'</td><td class="text-center">'+prices["sell"][i][1]+'</td></tr>');
    last.text(accounting.formatMoney(prices["last"],"",2,".",","));
}

$(document).ready(
		function() {
			var book = {
				"sell" : [ [ 22.7, 800 ], [ 22.95, 400 ], [ 23.0, 1000 ],[ 23.8, 300 ] ],
				"buy" : [ [ 22.5, 300 ], [ 22.45, 400 ], [ 22.36, 100 ],[ 21.9, 600 ] ],
				"last" : 23.50
			}

			/* generate the book */
			generateBook($("tbody[name=buy-side]"), $("tbody[name=sell-side]"),	$("span[name=last]"), book)

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
			});

			/* put the information on modal window */
			$("#enviaOrdem").click(
					function() {
						$("input[name=tipoOrdem]").is(":checked") ? $("#tipoOrdem").text("Compra") : $("#tipoOrdem").text("Venda");
						$("p[name=modalPreco]").text(getDecimalValue($("#formPreco").val()));
						$("p[name=modalQtde]").text($("#formQtde").val());
						$("p[name=modalTotal]").text($("#precoTotal").text());
					});

			$("#formPreco").on("keyup", function() {
				// change to use accounting js library
				$(this).val($(this).val().replace(/\./, ","));
			});

		});
