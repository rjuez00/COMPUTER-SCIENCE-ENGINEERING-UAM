var psw1 = document.getElementById("psw1");
var psw2 = document.getElementById("psw2");

psw2.onkeyup = function () {
  // Validate lowercase letters
  if (psw2.value === psw1.value) {
    psw2.style.background = "#88f572";
  }
  else {
    psw2.style.background = "#f57272";
  }
}


psw1.onkeyup = function () {
  // Validate lowercase letters
  if (psw2.value === psw1.value && psw1.value !== "") {
    psw2.style.background = "#88f572";
  }
  else {
    psw2.style.background = "#f57272";
  }

  var pwd = psw1.value;

  if (pwd.length === 0) {
    $('#progress').val("0");
    return;
  }

  var prog = [/[A-Z]/, /[0-9]/, /[a-z]/]
    .reduce((memo, test) => memo + test.test(pwd), 0);

  // Length must be at least 8 chars
  if (pwd.length > 8) {
    prog++;
  }

  // Display it
  var progress = "";
  var color = "";
  switch (prog) {
    case 0:
      progress = "0";
      color = "white";
      break;
    case 1:
      progress = "25";
      color = "red";
      break;
    case 2:
      progress = "50";
      color = "orange";
      break;
    case 3:
      progress = "75";
      color = "yellow";
      break;
    case 4:
      progress = "100";
      color = "green";
      break;
  }
  $('#progress').val(progress);
}