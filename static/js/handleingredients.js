$(document).ready(function (){
    console.log("Hello")
    $("#id_suppliers").change(function (){
        if($("#id_suppliers").val()==='Add Supplier'){
            console.log("Add Input")
            $("#customsupplierid").attr("type","text")
        }
        else {
            $("#customsupplierid").attr("type","hidden")
        }
    })
    $("#id_hasMajorAllergens").change(function (){
        if($("#id_hasMajorAllergens").val()==='true'){
            console.log("True")
            $("#display-major-allergens").css("visibility","visible")
        }
        else {
            console.log("False")
            $("#display-major-allergens").css("visibility","hidden")
        }
    })
})