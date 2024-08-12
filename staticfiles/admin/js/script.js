///Date picker///
$(document).ready(function(){
    $('#reservation-date').datepicker({
      format: 'yyyy-mm-dd',
      autoclose: true,
      todayHighlight: true,
      startDate: new Date()
    });
  });