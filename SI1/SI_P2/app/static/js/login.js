function getCookie(cname) {
  var name = cname + "=";
  var decodedCookie = decodeURIComponent(document.cookie);
  var ca = decodedCookie.split(';');
  for(var i = 0; i <ca.length; i++) {
    var c = ca[i];
    while (c.charAt(0) == ' ') {
      c = c.substring(1);
    }
    if (c.indexOf(name) == 0) {
      return c.substring(name.length, c.length);
    }
  }
  return "";
}


function setCookie() {
  document.cookie = "nombre" + "=" + document.getElementById("nombre").value + ";"

}


function checkCookie() {
    var user=getCookie("nombre");
    if (user != "")
        document.getElementById('nombre').value=user;
  }


checkCookie();
