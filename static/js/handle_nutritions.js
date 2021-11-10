$(function (){
    $("#nutri-link-btn").bind('click',function (){
        document.getElementById("nut-loading").style.display="block";
    });
    $("#nutri-link-btn-change").bind('click',function (){
        document.getElementById("nut-loading").style.display="block";
    });
    $("#nutri-close-btn").bind('click',function (){
        document.getElementById("nut-loading").style.display="none";
    });
    $("#clear_food").bind('click',function (){
        //console.log($("#nutrient_database_search_results table").length)
        if($("#nutrient_database_search_results table").length>0){
            document.getElementById("nutrient_database_search_results").innerHTML = null
            //$("#nutrient_database_search_results table").remove();
        }
        const fooditem = $("#cached_usda_item_name").val();
        var settings = {
            "url": "https://api.nal.usda.gov/fdc/v1/foods/search?query="+fooditem+"&pageSize=50&api_key=hMQNzCAc55v0XsZEycBg9zgLw5OBQaJ1M9z3TCPV",
            "method": "GET",
            "timeout": 0,
        };

        $.ajax(settings).done(function (response) {
            document.getElementById("nutrient_database_search_results").style.display="block"
            var nutri_div = $("#nutrient_database_search_results");
            nutri_div.append(
                '<br/><br/>There are <strong>'+response.foods.length+'</strong> items matching this search criteria. We display the first 50 results.' +
        '<table class="table table-striped" id="table-data">'+
              '<thead>'+
                '<tr>'+
                  '<th>Search Results from Food Data Central</th>'+
                  '<th width="20%"></th>'+
                '</tr>'+
              '</thead>'+
              '<tbody class="tbody-nutri"></tbody>'
            )
            for(let i=0;i<response.foods.length;i++){
                var nutri_tbody = $(".tbody-nutri")
                if(response.foods[i].brandName){
                    nutri_tbody.append(
                        '<tr>'+
                          '<td class="ptm">'+
                            '<p>'+response.foods[i].description+'<br>'+'</p>'+
                            '<strong>Data Type:</strong> '+response.foods[i].dataType+
                                '<strong>Brand:</strong>'+response.foods[i].brandName+
                          '</td>'+
                          '<td>'+
                            '<button class="btn choose_food" >Choose</button>'+
                          '</td>'+
                        '</tr>'
                    )
                }
                else {
                    nutri_tbody.append(
                        '<tr>'+
                          '<td class="ptm">'+
                            '<p>'+response.foods[i].description+'</p>'+
                        '<strong>Data Type:</strong> '+"<span>"+response.foods[i].dataType+"</span>" +
                        "<b style='display: none'>"+response.foods[i].fdcId+"</b>"+
                          '</td>'+
                          '<td>'+
                            '<button class="btn choose_food" >Choose</button>'+
                          '</td>'+
                        '</tr>'
                    )
                }
            }
            $(".tbody-nutri button").bind('click',function (){
                console.log($(this).closest('tr').find('.ptm p').text())
                const selected_food = $(this).closest('tr').find('.ptm p').text()
                const selected_datatype = $(this).closest('tr').find('.ptm span').text()
                const fdcId = $(this).closest('tr').find('.ptm b').text()
                console.log(fdcId)
                const data = {'selected_food':selected_food,'fdcId': fdcId}
                $.ajaxSetup({
                    headers : {"X-CSRFToken":getCookie('csrftoken')},
                })
                $.post('/recipe/handle_measurements',data,function (result){
                    console.log(result)
                    document.getElementById("nutrient_database_search_results").innerHTML = null
                    $("#cached_usda_item_name").val(selected_food + '   Data Type:'+selected_datatype)
                    $("#nutri-data-link-value").val(selected_food)
                    $("#nutri-data-fdcid").val(fdcId)
                    $("#cached_usda_item_name").attr("readonly","")
                    $("#clear_food").css("display","none")
                    $("#reset_food").css("display","block")
                    $("#conversion_help").css({'display':'block'})
                    $("#nutri-link-btn").css({'display':'none'})
                    $("#nutri-link-btn-change").css({'display':'block'})
                    document.getElementById('display-selected-nutrition').innerText = selected_food
                    $("#display-selected-nutrition").css({'display':'block'})
                    var div = $("<div class='well' id='display-units-block' />")
                    if(result.measurement_units.length===0){
                        document.getElementById("display-units-msg").innerText = "No units from nutrition database"
                    }
                    for( let i=0;i<result.measurement_units.length;i++){
                        var unitsdiv = $("<div class='mb10' />");
                        unitsdiv.append("<p>Conversions provided by Food Data Central (FDC) for <strong>"+selected_food+"</strong>:</p>")
                        unitsdiv.html(
                            "<div class='mb10'>"+
                                result.measurement_units[i][0] +"<b>≈</b>"+ result.measurement_units[i][1]+
                                "<input type='hidden' name='units-hidden' value='"+result.measurement_units[i][2]+"'>"+
                                "<button class='add-measurment-button-nutri' type='button'><i class=\"fa fa-plus\" aria-hidden=\"true\"></i></button>"+
                            "</div>"
                        );
                        div.append(unitsdiv)
                    }
                    $("#conversion_help").append(div)

                    $(".add-measurment-button-nutri").bind('click',function (){
                        console.log($(this).closest("div").text().split("≈"))
                        console.log($(this).closest("div").find('input[type=hidden]').val())
                        var fromto = $(this).closest("div").text().split("≈")
                        //var options = document.getElementById("id_qtyUnits").innerHTML
                        var options = "<optgroup label=\"-- Weight --\">\n" +
                            "  <option value=\"Ounce (oz) (28.35 g)\">Ounce (oz) (28.35 g)</option>\n" +
                            "\n" +
                            "  <option value=\"Pound (lb) (453.59 g)\">Pound (lb) (453.59 g)</option>\n" +
                            "\n" +
                            "  <option value=\"Kilogram (Kg) (1000 g)\">Kilogram (Kg) (1000 g)</option>\n" +
                            "\n" +
                            "  <option value=\"Tonne (T) (1000000 g)\">Tonne (T) (1000000 g)</option>\n" +
                            "\n" +
                            "  <option value=\"Gram (g)\">Gram (g)</option>\n" +
                            "\n" +
                            "  </optgroup>\n" +
                            "  <optgroup label=\"-- Volume --\">\n" +
                            "  <option value=\"Pinch (pinch) (0.3 ml)\">Pinch (pinch) (0.3 ml)</option>\n" +
                            "\n" +
                            "  <option value=\"US Teaspoon (tsp) (4.93 ml)\">US Teaspoon (tsp) (4.93 ml)</option>\n" +
                            "\n" +
                            "  <option value=\"US Tablespoon (tbsp) (14.79 ml)\">US Tablespoon (tbsp) (14.79 ml)</option>\n" +
                            "\n" +
                            "  <option value=\"Fluid-ounce (floz) (29.57 ml)\">Fluid-ounce (floz) (29.57 ml)</option>\n" +
                            "\n" +
                            "  <option value=\"Deciliter (dL) (100 ml)\">Deciliter (dL) (100 ml)</option>\n" +
                            "\n" +
                            "  <option value=\"US Cup (cup) (236.59 ml)\">US Cup (cup) (236.59 ml)</option>\n" +
                            "\n" +
                            "  <option value=\"Pint (pt) (473.18 ml)\">Pint (pt) (473.18 ml)</option>\n" +
                            "\n" +
                            "  <option value=\"Milliliter (ml)\">Milliliter (ml)</option>\n" +
                            "\n" +
                            "  <option value=\"Quart (qt) (946.35 ml)\">Quart (qt) (946.35 ml)</option>\n" +
                            "\n" +
                            "  <option value=\"Liter (L) (1000 ml)\">Liter (L) (1000 ml)</option>\n" +
                            "\n" +
                            "  <option value=\"Gallon (gal) (3785.41 ml)\">Gallon (gal) (3785.41 ml)</option>\n" +
                            "\n" +
                            "  <option value=\"Cubic Meter (kl) (1000000 ml)\">Cubic Meter (kl) (1000000 ml)</option>\n" +
                            "\n" +
                            "  <option value=\"Each (each)\">Each (each)</option>\n" +
                            "\n" +
                            "  </optgroup>\n" +
                            "  <optgroup label=\"-- Quantity --\">\n" +
                            "  <option value=\"Dozen (dozen) (12 each)\">Dozen (dozen) (12 each)</option>\n" +
                            "\n" +
                            "  <option value=\"Hundred (hundred) (100 each)\">Hundred (hundred) (100 each)</option>\n" +
                            "\n" +
                            "  <option value=\"Thousand (thousand) (1000 each)\">Thousand (thousand) (1000 each)</option>\n" +
                            "\n" +
                            "  <option value=\"Million (million) (1000000 each)\">Million (million) (1000000 each)</option>\n" +
                            "\n" +
                            "  </optgroup>\n" +
                            "  <optgroup label=\"-- Time --\">\n" +
                            "  <option value=\"Second (s)\">Second (s)</option>\n" +
                            "\n" +
                            "  <option value=\"Minute (min) (60 s)\">Minute (min) (60 s)</option>\n" +
                            "\n" +
                            "  <option value=\"Hour (hr) (3600 s)\">Hour (hr) (3600 s)</option>\n" +
                            "\n" +
                            "  </optgroup>"
                        $("#TextBoxContainer").append(
                            '<div>' +
                            '<input name = "fromMeasurment" type="number" step="any" placeholder="From Measurment" value = "' + fromto[0].split(' ')[0] + '" style="width: auto" />&nbsp;' +
                            '<select name="ing-from-measuremnts"><option selected value="'+$(this).closest("div").find('input[type=hidden]').val()+'">'+$(this).closest("div").find('input[type=hidden]').val()+'</option>'+options+'</select>&nbsp;&nbsp;=&nbsp;&nbsp;'+
                            '<input name = "toMeasurment" type="number" step="any" placeholder="To Measurment" value = "' + fromto[1] + '" style="width: auto" />&nbsp;' +
                            '<select name="ing-to-measuremnts"><option selected="Gram (g)">Gram (g)</option>'+options+'</select>&nbsp;&nbsp;'+
                            '<input type="button" value="Remove" class="remove" style="width: auto" /><br/><br/>'+
                            '</div>'
                        );
                        $("#btnGet").css({"visibility":"visible"});
                    })
                    $("#reset_food").bind('click',function (){
                       $("#clear_food").css("display","block")
                        $("#reset_food").css("display","none")
                        $("#cached_usda_item_name").val("")
                        $("#cached_usda_item_name").removeAttr("readonly")
                        delete $.ajaxSettings.headers["X-CSRFToken"]
                        document.getElementById("display-units-msg").innerText = ''
                        document.getElementById('display-units-block').innerText = ''
                        document.getElementById('display-selected-nutrition').innerText = ''
                        $("#display-selected-nutrition").css({'display':'none'})
                        $("#nutri-link-btn").css({'display':'block'})
                        $("#nutri-link-btn-change").css({'display':'none'})
                        $("#nutri-data-link-value").val('')
                        $("#nutri-data-fdcid").val('')
                        $("#conversion_help").css({'display':'none'})
                    });
                })
            });
        });
    });
});
