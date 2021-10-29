function getOptions(){
    return  {
        'Weight': ['Ounce (oz) (28.35 g)','Pound (lb) (453.59 g)','Kilogram (Kg) (1000 g)','Tonne (T) (1000000 g)','Gram (g)'],
        'Volume': ['Pinch (pinch) (0.3 ml)','US Teaspoon (tsp) (4.93 ml)','US Tablespoon (tbsp) (14.79 ml)','Fluid-ounce (floz) (29.57 ml)','Deciliter (dL) (100 ml)','US Cup (cup) (236.59 ml)','Pint (pt) (473.18 ml)','Milliliter (ml)','Quart (qt) (946.35 ml)','Liter (L) (1000 ml)','Gallon (gal) (3785.41 ml)','Cubic Meter (kl) (1000000 ml)','Each (each)'],
        'Quantity': ['Dozen (dozen) (12 each)','Hundred (hundred) (100 each)','Thousand (thousand) (1000 each)','Million (million) (1000000 each)'],
        'Time': ['Second (s)','Minute (min) (60 s)','Hour (hr) (3600 s)']
    }
}
$(function () {
    $("#btnAdd").bind("click", function () {
        $("#btnGet").css({"visibility":"visible"});
        var div = $("<div />");
        div.html(GetDynamicTextBox(""));
        $("#TextBoxContainer").append(div);
    });
    $("#btnGet").bind("click", function () {
        var fromvalues = "";
        var tovalues = "";
        var fromunits = "";
        var tounits = "";
        var from_units_list = []
        var to_units_list = []
        $("input[name=fromMeasurment]").each(function () {
            fromvalues += $(this).val() + ",";
        });
        $("input[name=toMeasurment]").each(function () {
            tovalues += $(this).val() + ",";
        });
        $("select[name=ing-from-measuremnts]").each(function () {
            fromunits += $(this).val() + ",";
            if(getOptions().Weight.includes($(this).val())){
                from_units_list.push("Weight")
            }
            if(getOptions().Volume.includes($(this).val())){
                from_units_list.push("Volume")
            }
            if(getOptions().Quantity.includes($(this).val())){
                from_units_list.push("Quantity")
            }
            if(getOptions().Time.includes($(this).val())){
                from_units_list.push("Time")
            }
        });
        $("select[name=ing-to-measuremnts]").each(function () {
            tounits += $(this).val() + ",";
            if(getOptions().Weight.includes($(this).val())){
                to_units_list.push("Weight")
            }
            if(getOptions().Volume.includes($(this).val())){
                to_units_list.push("Volume")
            }
            if(getOptions().Quantity.includes($(this).val())){
                to_units_list.push("Volume")
            }
            if(getOptions().Time.includes($(this).val())){
                to_units_list.push("Time")
            }
        });
        var weight_volume_count = 0
        var weight_quantity_count = 0
        var weight_time_count = 0
        var volume_weight_count = 0
        var volume_quantity_count = 0
        var volume_time_count = 0
        var quantity_volume_count = 0
        var quantity_weight_count = 0
        var quantity_time_count = 0
        var time_volume_count = 0
        var time_weight_count = 0
        var time_quantity_count = 0
        var same_units = false
        for (let i=0;i<from_units_list.length;i++){
            if(from_units_list[i] === to_units_list[i]){
                same_units = true
            }
            if(from_units_list[i] === "Volume" && to_units_list[i]==="Weight"){
                volume_weight_count+=1
            }
            else if(from_units_list[i] === "Volume" && to_units_list[i]==="Quantity"){
                volume_quantity_count+=1
            }
            else if(from_units_list[i] === "Volume" && to_units_list[i]==="Time"){
                volume_time_count+=1
            }
            else if(from_units_list[i] === "Weight" && to_units_list[i]==="Time"){
                weight_time_count+=1
            }
            else if(from_units_list[i] === "Weight" && to_units_list[i]==="Quantity"){
                weight_quantity_count+=1
            }
            else if(from_units_list[i] === "Weight" && to_units_list[i]==="Volume"){
                weight_volume_count+=1
            }
            else if(from_units_list[i] === "Quantity" && to_units_list[i]==="Volume"){
                quantity_volume_count+=1
            }
            else if(from_units_list[i] === "Quantity" && to_units_list[i]==="Time"){
                quantity_time_count+=1
            }
            else if(from_units_list[i] === "Quantity" && to_units_list[i]==="Weight"){
                quantity_weight_count+=1
            }
            else if(from_units_list[i] === "Time" && to_units_list[i]==="Weight"){
                time_weight_count+=1
            }
            else if(from_units_list[i] === "Time" && to_units_list[i]==="Quantity"){
                time_quantity_count+=1
            }
            else if(from_units_list[i] === "Time" && to_units_list[i]==="Volume"){
                time_volume_count+=1
            }
        }
        if(same_units || weight_time_count>1 || weight_volume_count>1 || weight_quantity_count>1 || quantity_volume_count>1 || quantity_weight_count>1 || quantity_time_count>1 || volume_weight_count>1 || volume_quantity_count>1 || volume_time_count>1 || time_weight_count>1 || time_quantity_count>1 || time_volume_count>1){
            document.getElementById("display-units-measurment-err").innerText = "can not have more than one converter with repeated units and could not have same measurments"
        }
        else {
            document.getElementById("display-units-measurment-err").innerText = ''
            document.getElementById("id_ingMeasurementsData").value = fromvalues+";"+tovalues+";"+fromunits+";"+tounits
            alert("Measurements Saved")
        }
    });
    $("body").on("click", ".remove", function () {
        $(this).closest("div").remove();
        if($("input[name=fromMeasurment]").length===0){
            $("#btnGet").css({"visibility":"hidden"});
            document.getElementById("id_ingMeasurementsData").value=''
        }
        else {
            $("#btnGet").css({"visibility":"visible"});
        }
    });
});
function GetDynamicTextBox(value) {
    var options = document.getElementById("id_qtyUnits").innerHTML
    return '<input name = "fromMeasurment" type="number" step="any" placeholder="From Measurment" value = "' + value + '" style="width: auto" />&nbsp;' +
            '<select name="ing-from-measuremnts">'+options+'</select>&nbsp;&nbsp;=&nbsp;&nbsp;'+
            '<input name = "toMeasurment" type="number" step="any" placeholder="To Measurment" value = "' + value + '" style="width: auto" />&nbsp;' +
            '<select name="ing-to-measuremnts">'+options+'</select>&nbsp;&nbsp;'+
            '<input type="button" value="Remove" class="remove" style="width: auto" /><br/><br/>'
}