$(function (){
    $("#ingredientList").change(function (){
        var options = '<option value="">select unit</option>' +
            '<optgroup label="Volume">' +
            '<option value="Milliliter (ml)">Milliliter (ml) </option>\n' +
            '<option value="US Teaspoon (tsp) (4.93 ml)">US Teaspoon (tsp) (4.93 ml)</option>\n' +
            '<option value="US Tablespoon (tbsp) (14.79 ml)">US Tablespoon (tbsp) (14.79 ml)</option>\n' +
            '<option value="Fluid-ounce (floz) (29.57 ml)">Fluid-ounce (floz) (29.57 ml)</option>\n' +
            '<option value="Deciliter (dL) (100 ml)">Deciliter (dL) (100 ml)</option>\n' +
            '<option value="US Cup (cup) (236.59 ml)">US Cup (cup) (236.59 ml)</option>\n' +
            '<option value="Pint (pt) (473.18 ml)">Pint (pt) (473.18 ml)</option>\n' +
            '<option value="Quart (qt) (946.35 ml)">Quart (qt) (946.35 ml)</option>\n' +
            '<option value="Liter (L) (1000 ml)">Liter (L) (1000 ml)</option>\n' +
            '<option value="Gallon (gal) (3785.41 ml)">Gallon (gal) (3785.41 ml)</option>\n' +
            '<option value="Cubic metre (kL) (1000000 ml)">Cubic metre (kL) (1000000 ml)</option' +
            '</optgroup>' +
            '<optgroup label="-- Weight --">\n' +
            '  <option value="Ounce (oz) (28.35 g)">Ounce (oz) (28.35 g)</option>\n' +
            '\n' +
            '  <option value="Pound (lb) (453.59 g)">Pound (lb) (453.59 g)</option>\n' +
            '\n' +
            '  <option value="Kilogram (Kg) (1000 g)">Kilogram (Kg) (1000 g)</option>\n' +
            '\n' +
            '  <option value="Tonne (T) (1000000 g)">Tonne (T) (1000000 g)</option>\n' +
            '\n' +
            '  <option value="Gram (g)">Gram (g)</option>\n' +
            '\n' +
            '  </optgroup>\n' +
            ' \n' +
            '<optgroup label="-- Quantity --">\n' +
            '  <option value="Dozen (dozen) (12 each)">Dozen (dozen) (12 each)</option>\n' +
            '\n' +
            '  <option value="Hundred (hundred) (100 each)">Hundred (hundred) (100 each)</option>\n' +
            '\n' +
            '  <option value="Thousand (thousand) (1000 each)">Thousand (thousand) (1000 each)</option>\n' +
            '\n' +
            '  <option value="Million (million) (1000000 each)">Million (million) (1000000 each)</option>\n' +
            '\n' +
            '  </optgroup>\n' +
            '\n' +
            '<optgroup label="-- Time --">\n' +
            '  <option value="Second (s)">Second (s)</option>\n' +
            '\n' +
            '  <option value="Minute (min) (60 s)">Minute (min) (60 s)</option>\n' +
            '\n' +
            '  <option value="Hour (hr) (3600 s)">Hour (hr) (3600 s)</option>\n' +
            '\n' +
            '  </optgroup>'
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