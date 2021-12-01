if(document.getElementById("name")){
  document.getElementById("name").addEventListener("change", function() {
    const nm = this.value;
    console.log(nm);
    const usnm = new RegExp("^(?=[a-zA-Z0-9._]{8,20}$)(?!.*[_.]{2})[^_.].*[^_.]$");
    if(!usnm.test(nm)) {
      var errmsg = "Please enter a valid username";
      this.style.color = "red";
      this.value = errmsg;
    }
  });

  document.getElementById("name").addEventListener("click", function() {
    this.style.color = "black";
    this.value="";
  });
}


if(document.getElementById("email")){
  document.getElementById("email").addEventListener("change", function() {
    const eml = this.value;
    console.log(eml);
    const email = new RegExp("^[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,4}$");
    if(!email.test(eml)) {
      var errmsg = "Please enter a valid Email ID";
      this.style.color = "red";
      this.value = errmsg;
    }
  });

  document.getElementById("email").addEventListener("click", function() {
    this.style.color = "black";
    this.value="";
  });

}


if(document.getElementById("password")){
  document.getElementById("password").addEventListener("change", function() {
    const pwd = this.value;
    console.log(pwd);
    console.log(pwd);
    const pswd = new RegExp("^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$ %^&*-]).{8,}$");
    if(!pswd.test(pwd)) {
      this.style.color = "red";
      this.type = "text";
      this.value = "";
      this.value = "Please enter a valid password";
    }
  });

  document.getElementById("password").addEventListener("click", function() {
    this.style.color = "black";
    this.type = "password";
    this.value = "";
  });
}
