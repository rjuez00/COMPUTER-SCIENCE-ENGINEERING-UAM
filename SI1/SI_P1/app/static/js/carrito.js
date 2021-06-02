jQuery(document).ready(function() {
	jQuery('.infodesplegable').slideUp("fast")
});

$('.item').hover(
    function () {
        $(this).find(".infodesplegable").slideDown("fast")
    }, 
    function() {
        $(this).find(".infodesplegable").slideUp("fast")
    });



function copy_values(quantity){
    for(i=1; i<=quantity; i++){
        temp = document.getElementById( "quantity".concat(i.toString()) ).value;
        document.getElementById("cantidad".concat(i.toString())).value = temp;
    }
}


function post(path, params, method='post') {

    // The rest of this code assumes you are not using a library.
    // It can be made less wordy if you use one.
    const form = document.createElement('form');
    form.method = method;
    form.action = path;
    form.id = "myformularyquantity"
    for (const key in params) {
      if (params.hasOwnProperty(key)) {
        const hiddenField = document.createElement('input');
        hiddenField.type = 'hidden';
        hiddenField.name = key;
        hiddenField.value = params[key];    
        form.appendChild(hiddenField);
      }
    }
    document.body.appendChild(form);

    $.ajax({
        type: "POST",
        url: path,
        data: $("#myformularyquantity").serialize(),
        success: function(data) {
        }
      });
      console.log("COMprobarcion que hace ajax")
      var myobj = document.getElementById("myformularyquantity");
      myobj.remove();
  
  }

function updatecuantity(valueid, peliculaid, path){
    element = document.getElementById(valueid).value
    post(path, {pelid: peliculaid, newquantity: element})
    return false
}