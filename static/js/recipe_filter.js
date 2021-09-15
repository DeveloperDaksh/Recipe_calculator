$(document).ready(function(){
  $("#rec-filetr-by-name").on("keyup", function() {
    const value = $(this).val().toLowerCase();
    $("#items-display-table >tbody>tr").filter(function() {
      $(this).toggle($(this).text().toLowerCase().indexOf(value) > -1)
    });
  });
});