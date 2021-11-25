function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
$(function (){
    $("#recipeList").change(function (){
        var selected_recipe = $("#recipeList").val()
        if(selected_recipe !== ''){
            $.ajaxSetup(
            {
                headers : {"X-CSRFToken":getCookie('csrftoken')},
            })
            $.post('/recipe/getrecipedetails',{'selected_recipe':selected_recipe},function (result){
                $("#recipeList").val('')
                var div = $("<div />");
                div.html(
                    '<label>'+result.recipe_name+'  :  </label>' +
                    '<input type="hidden" value="'+result.recipe_name+'" name="recipename">' +
                    '<label>Target Yield</label>' +
                    '<input name = "yieldCount" type="text" placeholder="Target Yield" value="'+result.yield_count+'" style="width: auto" required />&nbsp;' +
                    '<input name = "categorybatch" type="text" value="'+result.yield_units+'(Batch size is '+result.yield_count+')" readonly style="width: auto" required />&nbsp;' +
                    '<input type="button" value="Remove" class="remove" style="width: auto" />'
                );
                $("#selected-recipes_list").append(div)
                $("body").on("click", ".remove", function () {
                    $(this).closest("div").remove();
                });
            })
        }
    })
    $("body").on("click", ".remove", function () {
        $(this).closest("div").remove();
    });
    $("#recipecategoryList").change(function (){
        var selected_category = $("#recipecategoryList").val()
        if(selected_category !== ''){
            $.ajaxSetup(
            {
                headers : {"X-CSRFToken":getCookie('csrftoken')},
            })
            $.post('/recipe/getrecipesfromcategory',{'selected_category': selected_category},function (result){
                $("#recipecategoryList").val('')
                for(let i=0;i<result.recipe_data.length;i++){
                    var div = $("<div />");
                    div.html(
                        '<label>'+result.recipe_data[i][0]+'</label>' +
                        '<input type="hidden" value="'+result.recipe_data[i][0]+'" name="recipename">' +
                        '<input name = "yieldCount" type="text" placeholder="Target Yield" value="'+result.recipe_data[i][1]+'" style="width: auto" required />&nbsp;' +
                        '<input name = "categorybatch" type="text" value="'+result.recipe_data[i][2]+'(Batch size is '+result.recipe_data[i][1]+')" readonly style="width: auto" required />&nbsp;' +
                        '<input type="button" value="Remove" class="remove" style="width: auto" />'
                    );
                    $("#selected-recipes_list").append(div)
                    $("body").on("click", ".remove", function () {
                        $(this).closest("div").remove();
                    });
                }
            })
        }
    })
})