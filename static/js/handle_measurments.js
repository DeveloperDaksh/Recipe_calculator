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
        $("input[name=fromMeasurment]").each(function () {
            fromvalues += $(this).val() + ",";
        });
        $("input[name=toMeasurment]").each(function () {
            tovalues += $(this).val() + ",";
        });
        $("select[name=ing-from-measuremnts]").each(function () {
            fromunits += $(this).val() + ",";
        });
        $("select[name=ing-to-measuremnts]").each(function () {
            tounits += $(this).val() + ",";
        });
        document.getElementById("id_ingMeasurementsData").value = fromvalues+";"+tovalues+";"+fromunits+";"+tounits
        alert("Measurements Saved")
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
    return '<input name = "fromMeasurment" type="number" placeholder="From Measurment" value = "' + value + '" style="width: auto" />&nbsp;' +
            '<select name="ing-from-measuremnts">'+options+'</select>&nbsp;&nbsp;=&nbsp;&nbsp;'+
            '<input name = "toMeasurment" type="number" placeholder="To Measurment" value = "' + value + '" style="width: auto" />&nbsp;' +
            '<select name="ing-to-measuremnts">'+options+'</select>&nbsp;&nbsp;'+
            '<input type="button" value="Remove" class="remove" style="width: auto" /><br/><br/>'
}