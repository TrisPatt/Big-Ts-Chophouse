///Date picker///

$(document).ready(function(){
    $('#reservation-date').datepicker({
      format: 'yyyy-mm-dd',
      autoclose: true,
      todayHighlight: true,
      startDate: new Date(),
      templates: {
        leftArrow: '<i class="fas fa-chevron-left"></i>',
        rightArrow: '<i class="fas fa-chevron-right"></i>'
      }
    });

    $('#reservation-date').on('changeDate', function(e) {
      let selectedDate = e.format(0, 'yyyy-mm-dd');
      let today = new Date().toISOString().split('T')[0];
      if (selectedDate === today) {
          $(this).find('.datepicker-days .day').filter(function(){
              return $(this).text() === String(new Date().getDate());
          }).css('background-color', '#5bc0de'); 
      }
  });
});

  