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
    $("select#company-select").click(function (event){
        event.preventDefault()
        $("#profile-button").toggleClass("show open");
        $("#expand-button").prop("aria-expanded","true");
        $("#drop-profile-show").toggleClass("shown open");
    })
    $("select#company-select").change(function (){
        var optionSelected = $(this).find("option:selected");
        var valueSelected = optionSelected.val();
        console.log(valueSelected)
        $.ajaxSetup(
            {
                headers : {"X-CSRFToken":getCookie('csrftoken')},
            })
        var data = {'valueSelected':valueSelected}
        $.post('/company/savecompany',data,function (result){
            if(result.status==='ok'){
                $("select#company-select").val(valueSelected)
                window.location.href=window.location.origin+"/dashboard"
            }
        })
    })
})