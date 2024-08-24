///Date picker///

$(document).ready(function(){
    $('#reservation-date').datepicker({
      format: 'yyyy-mm-dd',
      autoclose: true,
      todayHighlight: true,
      startDate: new Date(),
      templates: {
        leftArrow: '<i class="fas fa-chevron-left"></i>',
        rightArrow: '<i class="fas fa-chevron-right"></i>',
      }
    });
});

$(document).ready(function(){
  $('#visit-date').datepicker({
    format: 'yyyy-mm-dd',
    autoclose: true,
    templates: {
      leftArrow: '<i class="fas fa-chevron-left"></i>',
      rightArrow: '<i class="fas fa-chevron-right"></i>',
    },
    endDate: new Date(),
  });
});