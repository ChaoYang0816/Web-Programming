$(function(){
  $("#email").keyup(function(){
      var val = $("#email").val();
      console.log(val);

      $.ajax({
        url: '/checkUser/',
        type: 'GET',
        datatype: 'text',
        data: {'input': val},
        success: function(data){

        }
      });
  });
})
