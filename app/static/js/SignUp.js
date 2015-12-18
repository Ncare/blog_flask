function validatePassword() {
    var pw1 = document.getElementById("inputPassword").value;
    var pw2 = document.getElementById("rePassword").value;

    if(pw1==pw2){
        document.getElementById("submit").disabled = false;
        document.getElementById("remind").innerHTML = "";

    }
    else{
        document.getElementById("submit").disabled = true;
        document.getElementById("remind").innerHTML = "<font color='red'>密码不一样</font>"
    }
}


function validateUsername() {
    var username = document.getElementById("Username").value;


    if(username.length<4){
        document.getElementById("remind").innerHTML = "<font color='red'>用户名太短</font>"
    }
    else{
        document.getElementById("remind").innerHTML = "";
    }
}