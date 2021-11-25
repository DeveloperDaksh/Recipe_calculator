$(function (){
            $("#id_supplier").css("width","350px")
            $("#id_qtyUnits").css("width","350px")
            $("#id_country_of_origin").css("width","350px")
            $('<div id="div_id_addcustomsupplier" class="form-group"> <label style="display: none" for="id_addcustomsupplier" id="id_labeladdcustomsupplier" class=" requiredField">'+
                'Supplier Name<span class="asteriskField">*</span> </label> <div class=""> <input type="hidden" name="customsupplier" class="textinput form-control" required="" id="id_addcustomsupplier"> </div> </div>').insertAfter("#div_id_supplier")
            $("#id_supplier").change(function (){
                var selected_value = $("#id_supplier").val()
                if(selected_value === 'Add Supplier'){
                    $("#id_addcustomsupplier").attr("type","text")
                    $("#id_labeladdcustomsupplier").css({'display':'block'})
                }
                else {
                    $("#id_addcustomsupplier").attr("type","hidden")
                    $("#id_labeladdcustomsupplier").css({'display':'none'})
                }
            })
        })