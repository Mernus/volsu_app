const csrftoken = Cookies.get('csrftoken');

// Password update
$(function () {
  $("#updatePasswordButton").click(function () {
    let btn = $('#updatePasswordButton');
    btn.html('<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>Updating...');
    btn.disabled = true;
    setTimeout(validatePassword, 50);
  });

  const passwordRegexp = new RegExp('[A-Za-z0-9_%^|!`@#$&.]{8,128}');

  // Check password validity
  const checkPassword = passwordElems => {
    let passwordInput = passwordElems.first();
    let passwordFeedback = passwordElems.last();

    if (!passwordRegexp.test(passwordInput.val())) {
      passwordInput.removeClass("is-valid");
      passwordInput.addClass("is-invalid");

      if (!passwordInput.val()) {
        passwordFeedback.html("Please provide anything");
      } else if (passwordInput.val().length > 128 || passwordInput.val().length < 8) {
        passwordFeedback.html("Password length must be >= 8 and <= 128");
      } else {
        passwordFeedback.html("Password can contain latin lower/uppercase letters, numbers, and special chars _%^|!`@#$&.");
      }
      passwordFeedback.show();
      return false;
    } else {
      passwordInput.removeClass("is-invalid");
      passwordInput.addClass("is-valid");

      passwordFeedback.html("");
      passwordFeedback.hide();
    }
    return true;
  };

  // Validate all passwords
  function validatePassword() {
    let validationPassed = true;

    let oldPassword = $(".old_pass");
    if (!checkPassword(oldPassword)) {
      validationPassed = false;
    }

    let newPassword = $(".new_pass");
    if (!checkPassword(newPassword)) {
      validationPassed = false;
    }

    let confirmPassword = $(".confirm_pass");
    if (!checkPassword(confirmPassword)) {
      validationPassed = false;
    }

    if (!checkPasswordEquality(newPassword, oldPassword, true)) {
      validationPassed = false;
    }

    if (!checkPasswordEquality(newPassword, confirmPassword, false)) {
      validationPassed = false;
    }

    if (validationPassed) {
      setTimeout(updatePassword, 1000);
    } else {
      setTimeout(function () {
        $('#updatePasswordButton').html('Update password');
      }, 100);
    }
  }

  // Send ajax password update
  function updatePassword() {
    let username = $('#username').val();
    if (!username) {
      username = $('#username').attr('placeholder');
    }

    let request_data = {
      'username': username,
      'old_password': $('.old_pass').first().val(),
      'new_password': $('.new_pass').first().val()
    }

    $.ajax({
      headers: {
        'X-CSRFTOKEN': csrftoken
      },
      url: "/api/settings/update_password/",
      data: request_data,
      type: 'POST',
      credentials: 'include',
      success: function (result, status, xhr) {
        if (xhr.status === 200) {
          console.log("Password updated");
          return;
        }

        let error = result['non_field_errors'][0];

        let oldPassword = $(".old_pass");
        oldPassword.first().removeClass("is-valid");
        oldPassword.first().addClass("is-invalid");
        oldPassword.last().html(error);
        oldPassword.last().show()
      },
    });
    callbackPassword();
  }

  // Password update callback
  function callbackPassword() {
    $('#updatePasswordButton').html('Updated');

    setTimeout(function () {
      let btn = $('#updatePasswordButton');

      btn.disabled = false;
      btn.html('Update password');
    }, 100);
  }
});

// Update settings
$(function () {
    $("#updateButton").click(function () {
      let btn = $('#updateButton');
      btn.html('<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>Updating...');
      btn.disabled = true;
      setTimeout(validateSettings, 50);
    });

    const usernameRegexp = new RegExp('[A-Za-z0-9.@+-]{3,80}');
    const fullnameRegexp = new RegExp('[А-ЯA-Za-zа-я- ]{1,100}');
    // https://developer.mozilla.org/en-US/docs/Web/HTML/Element/input/email
    const emailRegexp = new RegExp('[a-zA-Z0-9.!#$%&\'*+\\/=?^_`{|}~-]+@[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?(?:\\.[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)*');
    const orgRegexp = new RegExp('[^!\"\'$^;?*,<>]{,120}');

    const checkUsername = usernameElems => {
      let usernameInput = usernameElems.first();
      let usernameFeedback = usernameElems.last();

      if (usernameInput.val() !== "" && !usernameRegexp.test(usernameInput.val())) {
        usernameInput.removeClass("is-valid");
        usernameInput.addClass("is-invalid");

        if (usernameInput.val().length > 80 || usernameInput.val().length < 3) {
          usernameFeedback.html("Username length must be >= 3 and <= 80");
        } else {
          usernameFeedback.html("Username can contain latin lower/uppercase letters, numbers, and special chars .@+-");
        }
        return false;
      } else {
        usernameInput.removeClass("is-invalid");
        usernameInput.addClass("is-valid");
        usernameFeedback.html("");
      }
      return true;
    };

    const checkFullname = fullnameElems => {
      let fullnameInput = fullnameElems.first();
      let fullnameFeedback = fullnameElems.last();

      if (fullnameInput.val() !== "" && !fullnameRegexp.test(fullnameInput.val())) {
        fullnameInput.removeClass("is-valid");
        fullnameInput.addClass("is-invalid");

        if (fullnameInput.val().length > 100) {
          fullnameFeedback.html("Fullname length must be <= 100");
        } else {
          fullnameFeedback.html("Fullname can contain latin/russian lower/uppercase letters, numbers, and special chars `-`,` `");
        }
        return false;
      } else {
        fullnameInput.removeClass("is-invalid");
        fullnameInput.addClass("is-valid");
        fullnameFeedback.html("");
      }
      return true;
    };

    const checkEmail = emailElems => {
      let emailInput = emailElems.first();
      let emailFeedback = emailElems.last();

      if (emailInput.val() !== "" && !emailRegexp.test(emailInput.val())) {
        emailInput.removeClass("is-valid");
        emailInput.addClass("is-invalid");
        emailFeedback.html("Email must match pattern from https://emailregex.com/");
        return false;
      } else {
        emailInput.removeClass("is-invalid");
        emailInput.addClass("is-valid");
        emailFeedback.html("");
      }
      return true;
    };

    const checkOrg = orgElems => {
      let orgInput = orgElems.first();
      let orgFeedback = orgElems.last();

      if (orgInput.val() !== "" && !orgRegexp.test(orgInput.val())) {
        orgInput.removeClass("is-valid");
        orgInput.addClass("is-invalid");

        if (orgInput.val().length > 120) {
          orgFeedback.html("Organization name length must be <= 120");
        } else {
          orgFeedback.html("Organization name mustn't contain !\"'$^;?*,<>");
        }
        return false;
      } else {
        orgInput.removeClass("is-invalid");
        orgInput.addClass("is-valid");
        orgFeedback.html("");
      }
      return true;
    };

    function validateSettings() {
      let validationPassed = true;
      let request_data = {}

      let username = $(".username");
      let currentUsername = $('.username').first().attr('placeholder');
      if (currentUsername !== username.first().val()) {
        if (!checkUsername(username)) {
          validationPassed = false;
        } else if (username.first().val() !== "") {
          request_data['username'] = username.first().val();
        }
      }

      let newTimezone = $("#timezoneInputSelect");
      let currentTimezone = $("#timezone").html();
      if (currentTimezone !== newTimezone.first().val() && newTimezone.first().val() !== "") {
        request_data['timezone'] = newTimezone.first().val();
      }

      let fullname = $(".fullname");
      let currentFullname = $('.fullname').first().attr('placeholder');
      if (currentFullname !== fullname.first().val()) {
        if (!checkFullname(fullname)) {
          validationPassed = false;
        } else if (fullname.first().val() !== "") {
          request_data['fullname'] = fullname.first().val();
        }
      }

      let org = $(".org");
      if (org.length) {
        let currentOrg = $('.org').first().attr('placeholder');
        if (currentOrg !== org.first().val()) {
          if (!checkOrg(org)) {
            validationPassed = false;
          } else if (org.first().val() !== "") {
            request_data['organization'] = org.first().val();
          }
        }
      }

      let email = $(".email");
      let currentEmail = $('.email').first().attr('placeholder');
      if (currentEmail !== email.first().val()) {
        if (!checkEmail(email)) {
          validationPassed = false;
        } else if (email.first().val() !== "") {
          request_data['email'] = email.first().val();
        }
      }

      if (validationPassed && Object.keys(request_data).length !== 0) {
        setTimeout(function () {
          updateSettings(request_data);
        }, 1000);
      } else {
        setTimeout(function () {
          $('#updateButton').html('Update');
        }, 100);
      }
    }

    // Send ajax update
    function updateSettings(data) {
      let user_id = $('.header')[0].id;

      $.ajax({
        headers: {
          'X-CSRFTOKEN': csrftoken
        },
        url: "/api/settings/" + user_id + "/",
        data: data,
        type: 'PATCH',
        credentials: 'include',
        success: function (result, status, xhr) {
          if (xhr.status === 200) {
            console.log("Settings updated");
            location.reload();
          }

          let error = result['non_field_errors'][0];
          let username = $(".username");
          username.first().removeClass("is-valid");
          username.first().addClass("is-invalid");
          username.last().html(error);

          let fullname = $(".fullname");
          fullname.first().removeClass("is-valid");
          fullname.first().addClass("is-invalid");
          fullname.last().html(error);

          let email = $(".email");
          email.first().removeClass("is-valid");
          email.first().addClass("is-invalid");
          email.last().html(error);
        },
      });
      callbackSettings();
    }

    // Update callback
    function callbackSettings() {
      $('#updateButton').html('Updated');

      setTimeout(function () {
        let btn = $('#updateButton');

        btn.disabled = false;
        btn.html('Update');
      }, 100);
    }
  }
);

// Update profile image
$(function () {
    $("#button-image").click(function () {
      let btn = $('#button-image');
      btn.html('<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>Uploading...');
      btn.disabled = true;
      console.log(btn);
      setTimeout(validateProfileImg, 50);
    });

    function validateProfileImg() {
      let input_file = $('#updateImage')[0].files;
      console.log(input_file);
      if (input_file.length === 0) {
        setTimeout(function () {
          $('#button-image').html('Update');

          let image = $("#updateImage");
          image.removeClass("is-valid");
          image.addClass("is-invalid");
        }, 100);
      } else {
        setTimeout(function () {
          let data = new FormData();
          data.append('profile_img', input_file[0]);
          updateProfileImg(data);
        }, 1000);
      }
    }

    // Send ajax update profile image
    function updateProfileImg(data) {
      let user_id = $('.header')[0].id;

      $.ajax({
        headers: {
          'X-CSRFTOKEN': csrftoken
        },
        url: "/api/settings/" + user_id + "/",
        data: data,
        contentType: false,
        processData: false,
        type: 'PATCH',
        credentials: 'include',
        traditional: true, // Do not add [] to array
        success: function (result, status, xhr) {
          let image = $("#updateImage");

          if (xhr.status === 200) {
            image.removeClass("is-invalid");
            image.addClass("is-valid");
            location.reload();
          }

          let error = result['non_field_errors'][0];
          image.removeClass("is-valid");
          image.addClass("is-invalid");
          $('#image-tooltip').html(error);
        },
      });
      callbackProfileImg();
    }

    // Update profile image callback
    function callbackProfileImg() {
      $('#button-image').html('Uploaded');

      setTimeout(function () {
        let btn = $('#button-image');

        btn.disabled = false;
        btn.html('Upload');
      }, 100);
    }
  }
);

// Show button event
$('div.d-flex > button').click(function (e) {
  showPassword(e)
});

// Check equality of new and confirm passwords
function checkPasswordEquality(newPassword, confirmPassword, equal) {
  let newPasswordInput = newPassword.first();
  let confirmPasswordInput = confirmPassword.first();

  let check = confirmPasswordInput.val() !== newPasswordInput.val();
  let feedback = "Passwords are not equal";
  if (equal) {
    check = confirmPasswordInput.val() === newPasswordInput.val();
    feedback = "Passwords are equal";
  }

  if (check) {
    newPasswordInput.removeClass("is-valid");
    newPasswordInput.addClass("is-invalid");

    confirmPasswordInput.removeClass("is-valid");
    confirmPasswordInput.addClass("is-invalid");

    let newPasswordFeedback = newPassword.last();
    newPasswordFeedback.html(feedback);
    newPasswordFeedback.show();

    let confirmPasswordFeedback = confirmPassword.last();
    confirmPasswordFeedback.html(feedback);
    confirmPasswordFeedback.show();
    return false;
  }
  return true;
}

// Show or hide password input
function showPassword(e) {
  let target_tag = e.target.nodeName.toLowerCase();
  let input = $(e.target).parents().eq(0).children(":first");
  if (target_tag === 'i') {
    input = $(e.target).parents().eq(1).children(":first");
  }

  if (input.attr("type") === 'text') {
    input.attr('type', 'password');
  } else {
    input.attr('type', 'text');
  }
}