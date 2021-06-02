var URL;

function users() {
    $.ajax({
      url: URL, 
      success: function(data) {
          $('#usuarios').html("Usuarios: " + data);
      },
      complete: function() {
        setTimeout(users, 3000);
      }
    });
  };

  function initURL(url) {
    URL = url;
    users();
  }