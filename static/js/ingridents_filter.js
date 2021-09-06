$(document).ready(function(){
  $("#filetr-by-name").on("keyup", function() {
    const value = $(this).val().toLowerCase();
    $("#items-display-table *").filter(function() {
      $(this).toggle($(this).text().toLowerCase().indexOf(value) > -1)
    });
  });
  $("#ingrident-filter-category").change(function (){
      console.log("Change")
      const item = $(this).val().toLowerCase();
      console.log(item)
      $("#ingrident-category-item *").filter(function() {
        $(this).toggle($(this).text().toLowerCase().indexOf(item) > -1)
      });
  })
});