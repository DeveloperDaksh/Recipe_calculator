$(function (){
    $("#nutri-link-btn").bind('click',function (){
        document.getElementById("nut-loading").style.display="block";
    });
    $("#nutri-close-btn").bind('click',function (){
        document.getElementById("nut-loading").style.display="none";
    });
    $("#clear_food").bind('click',function (){
        //document.getElementById("nutrient_database_search_results").innerHTML=null
        //document.getElementById("table-data").innerHTML=null
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
                console.log(response.foods[i]);
                var nutri_tbody = $(".tbody-nutri")
                if(response.foods[i].brandName){
                    nutri_tbody.append(
                        '<tr>'+
                          '<td class="ptm">'+
                            response.foods[i].description+'<br>'+
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
                            response.foods[i].description+'<br>'+
                            '<strong>Data Type:</strong> '+response.foods[i].dataType+
                          '</td>'+
                          '<td>'+
                            '<button class="btn choose_food" >Choose</button>'+
                          '</td>'+
                        '</tr>'
                    )
                }
            }
            $(".tbody-nutri button").bind('click',function (){
                console.log($(this).closest('tr').find('.ptm').text())
            });
        });
    })
});
