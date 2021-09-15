$(function (){
    $("#ingredientList").change(function (){
        var options = '<option disabled>select unit</option>' +
            '<optgroup label="Volume">' +
            '<option value="Milliliter (ml)">Milliliter (ml) </option>\n' +
            '<option value="US Teaspoon (tsp) (4.93 ml)">US Teaspoon (tsp) (4.93 ml)</option>\n' +
            '<option value="US Tablespoon (tbsp) (14.79 ml)">US Tablespoon (tbsp) (14.79 ml)</option>\n' +
            '<option value="Fluid-ounce (floz) (29.57 ml)">Fluid-ounce (floz) (29.57 ml)</option>\n' +
            '<option value="Deciliter (dL) (100 ml)">Deciliter (dL) (100 ml)</option>\n' +
            '<option value=">US Cup (cup) (236.59 ml)">US Cup (cup) (236.59 ml)</option>\n' +
            '<option value="Pint (pt) (473.18 ml)">Pint (pt) (473.18 ml)</option>\n' +
            '<option value="Quart (qt) (946.35 ml)">Quart (qt) (946.35 ml)</option>\n' +
            '<option value="Liter (L) (1000 ml)">Liter (L) (1000 ml)</option>\n' +
            '<option value="Gallon (gal) (3785.41 ml)">Gallon (gal) (3785.41 ml)</option>\n' +
            '<option value="Cubic metre (kL) (1000000 ml)">Cubic metre (kL) (1000000 ml)</option' +
            '</optgroup>'
        var optionSelected = $(this).find("option:selected");
        var valueSelected = optionSelected.val();
        console.log(valueSelected)
        var div = $("<div />");
        div.html(
            '<label>'+valueSelected+'</label>' +
            '<input type="hidden" value="'+valueSelected+'" name="ingridientName">'+
            '<input name = "ingAmount" type="number" placeholder="Amount" style="width: auto" required />&nbsp;' +
            '<select name="ingUnits" required>'+options+'</select>&nbsp;&nbsp;=&nbsp;&nbsp;'+
            '<input type="text" name="ingDescription" placeholder="Description(optional)">' +
            '<input type="button" value="Remove" class="remove" style="width: auto" /><br/><br/>'
        );
        $("#selected-ingredients").append(div)
    });
    $("body").on("click", ".remove", function () {
        $(this).closest("div").remove();
    });
});