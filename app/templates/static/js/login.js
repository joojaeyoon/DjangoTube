const loginForm = $("#login-form");
const registerForm = $("#register-form");

loginForm.on("submit", function(e) {
  e.preventDefault();

  const form = e.target;
  const loginData = {
    csrfmiddlewaretoken: form.csrfmiddlewaretoken.value,
    username: form.materialLoginFormUsername.value,
    password: form.materialLoginFormPassword.value
  };

  $.ajax("/rest-auth/login/", {
    type: "POST",
    data: loginData
  })
    .done(function(res, statusText, xhr) {
      console.log("Login success!");
      localStorage.setItem("token", res.key);
      window.location.href = "/";
    })
    .fail(function(xhr, statusText) {
      // 에러처리 하기
      console.log("Login failure!");
    });
});

registerForm.on("submit", function(e) {
  e.preventDefault();

  const form = e.target;
  const loginData = {
    csrfmiddlewaretoken: form.csrfmiddlewaretoken.value,
    username: form.materialRegisterFormUsername.value,
    password1: form.materialRegisterFormPassword.value,
    password2: form.materialRegisterFormPasswordCheck.value
  };

  $.ajax("/rest-auth/registration/", {
    type: "POST",
    data: loginData
  })
    .done(function(res, statusText, xhr) {
      console.log("register success!");
      localStorage.setItem("token", res.key);
      window.location.href = "/";
    })
    .fail(function(xhr, statusText) {
      console.log(xhr.responseJSON); // 에러처리 하기
      console.log("register failure!");
      console.log(statusText);
    });
});

$("#to-register").on("click", () => {
  $("#Login").hide();
  $("#Register").show();
});
$("#to-login").on("click", () => {
  $("#Login").show();
  $("#Register").hide();
});
