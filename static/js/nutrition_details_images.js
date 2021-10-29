$(function (){
    $("#id_weight").focus(function (){
        $("#h3_display_msg").text("Weight")
        $("#p_display_msg").text("In the 'Weight' field, you need to enter a weight that represents the serving " +
            "size from the food item you are entering. In the example above, " +
            "the serving size is actually given as a volume (240ml). When this is the case," +
            " we recommend using a kitchen scale to weigh 240ml of the food " +
            "product and enter that into the 'Weight' field.")
        $("#img_display_nutri").attr("src","/static/images/weight.png")
    })
    $("#id_calories").focus(function (){
        $("#h3_display_msg").text("Calories")
        $("#p_display_msg").text("In the 'Calories' field, you need to enter a numeric value representing\n" +
            "the number of calories in the serving size.")
        $("#img_display_nutri").attr("src","/static/images/calories.png")
    })
    $("#id_total_fat").focus(function (){
        $("#h3_display_msg").text("Total Fat")
        $("#p_display_msg").text("In the 'Total Fat' field, you need to enter a numeric value representing\n" +
            "        the amount of total fat in the serving size.")
        $("#img_display_nutri").attr("src","/static/images/total_fat.png")
    })
    $("#id_saturated_fat").focus(function (){
        $("#h3_display_msg").text("Saturated Fat")
        $("#p_display_msg").text("In the 'Saturated Fat' field, you need to enter a numeric value representing\n" +
            "        the amount of saturated fat in the serving size.")
        $("#img_display_nutri").attr("src","/static/images/saturated_fat.png")
    })
    $("#id_trans_fat").focus(function (){
        $("#h3_display_msg").text("Trans Fat")
        $("#p_display_msg").html("In the 'Trans Fat' field, you need to enter a numeric value representing\n" +
            "        the amount of trans fat in the serving size.<br><br>\n" +
            "        <strong>NOTE:</strong> There is no trans-fat listed in this product. In this\n" +
            "        case, enter 0.")
        $("#img_display_nutri").attr("src","/static/images/trans_fat.png")
    })
    $("#id_cholesterol").focus(function (){
        $("#h3_display_msg").text("Cholesterol")
        $("#p_display_msg").text("In the 'Cholesterol' field, you need to enter a numeric value representing\n" +
            "        the amount of cholesterol in the serving size.")
        $("#img_display_nutri").attr("src","/static/images/cholesterol.png")
    })
    $("#id_sodium").focus(function (){
        $("#h3_display_msg").text("Sodium")
        $("#p_display_msg").text("In the 'Sodium' field, you need to enter a numeric value representing\n" +
            "        the amount of sodium in the serving size.")
        $("#img_display_nutri").attr("src","/static/images/sodium.png")
    })
    $("#id_total_carbohydrates").focus(function (){
        $("#h3_display_msg").text("Total Carbohydrates")
        $("#p_display_msg").text("In the 'Total Carbohydrates' field, you need to enter a numeric value representing\n" +
            "        the amount of total carbohydrates in the serving size.")
        $("#img_display_nutri").attr("src","/static/images/carbohydrates.png")
    })
    $("#id_dietary_fiber").focus(function (){
        $("#h3_display_msg").text("Dietary Fiber")
        $("#p_display_msg").text("In the 'Dietary Fiber' field, you need to enter a numeric value representing\n" +
            "        the amount of dietary fiber in the serving size.")
        $("#img_display_nutri").attr("src","/static/images/fibre.png")
    })
    $("#id_sugar").focus(function (){
        $("#h3_display_msg").text("Sugar")
        $("#p_display_msg").text("In the 'Sugar' field, you need to enter a numeric value representing\n" +
            "        the amount of sugar in the serving size.")
        $("#img_display_nutri").attr("src","/static/images/sugars.png")
    })
    $("#id_protein").focus(function (){
        $("#h3_display_msg").text("Protein")
        $("#p_display_msg").text("In the 'Protein' field, you need to enter a numeric value representing\n" +
            "        the amount of protein in the serving size.")
        $("#img_display_nutri").attr("src","/static/images/protein.png")
    })
    $("#id_vitamin_a").focus(function (){
        $("#h3_display_msg").text("Vitamin A")
        $("#p_display_msg").text("In the 'Vitamin A' field, you need to enter a numeric value representing\n" +
            "        the amount of vitamin A in the serving size.")
        $("#img_display_nutri").attr("src","/static/images/vitamin_a.png")
    })
    $("#id_vitamin_c").focus(function (){
        $("#h3_display_msg").text("Vitamin C")
        $("#p_display_msg").text("In the 'Vitamin C' field, you need to enter a numeric value representing\n" +
            "        the amount of vitamin C in the serving size.")
        $("#img_display_nutri").attr("src","/static/images/vitamin_c.png")
    })
    $("#id_calcium").focus(function (){
        $("#h3_display_msg").text("Calcium")
        $("#p_display_msg").text("In the 'Calcium' field, you need to enter a numeric value representing\n" +
            "        the amount of calcium in the serving size.")
        $("#img_display_nutri").attr("src","/static/images/calcium.png")
    })
    $("#id_iron").focus(function (){
        $("#h3_display_msg").text("Iron")
        $("#p_display_msg").text("In the 'Iron' field, you need to enter a numeric value representing\n" +
            "        the amount of iron in the serving size.")
        $("#img_display_nutri").attr("src","/static/images/iron.png")
    })
    $("#id_vitamin_d").focus(function (){
        $("#h3_display_msg").text("Vitamin D")
        $("#p_display_msg").text("In the 'Vitamin D' field, you need to enter a numeric value representing\n" +
            "         the number of mcg based on the serving size (this is not entered as\n" +
            "         a percent daily value)")
        $("#img_display_nutri").removeAttr("src")
    })
    $("#id_potassium").focus(function (){
        $("#h3_display_msg").text("Potassium")
        $("#p_display_msg").text("In the 'Potassium' field, you need to enter a numeric value representing\n" +
            "         the number of mg based on the serving size (this is not entered as\n" +
            "         a percent daily value).")
        $("#img_display_nutri").removeAttr("src")
    })
})