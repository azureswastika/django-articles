$(document).ready(function () {
    function emailValid() {
        if ($("#id_email").val()) {
            $.ajax({
                data: {email: $("#id_email").val()},
                url: '/validate/email/',
                method: 'post',
                success: function (response) {
                    if (response.is_taken == true) {
                        $('#id_email').removeClass('is-valid').addClass('is-invalid');
                    }
                    else {
                        $('#id_email').removeClass('is-invalid').addClass('is-valid');
                    }
                },
            });
            return $("#id_email").hasClass("is-valid")
        } else {
            return false
        }
    }

    function usernameValid() {
        if ($("#id_username").val()) {
            $.ajax({
                data: {username: $("#id_username").val()},
                url: '/validate/username/',
                method: 'post',
                success: function (response) {
                    if (response.is_taken == true) {
                        $('#id_username').removeClass('is-valid').addClass('is-invalid');
                    }
                    else {
                        $('#id_username').removeClass('is-invalid').addClass('is-valid');
                    }
                }
            });
            return $("#id_username").hasClass("is-valid")
        }
    }

    function passwordValid() {
        if ($("#id_password1").val()) {
            $.ajax({
                data: {password: $("#id_password1").val()},
                url: "/validate/password/",
                method: 'post',
                success: function (response) {
                    if (response.valid == true) {
                        $('#id_password1').removeClass('is-invalid').addClass('is-valid');
                    }
                    else {
                        $('#id_password1').removeClass('is-valid').addClass('is-invalid');
                    }
                }
            });
            if ($('#id_password1').val() == $('#id_password2').val()) {
                $('#id_password2').removeClass('is-invalid').addClass('is-valid');
            }
            else {
                $('#id_password2').removeClass('is-valid').addClass('is-invalid');
            }
            return $("#id_password1").hasClass("is-valid") && $("#id_password2").hasClass("is-valid")
        } else {
            return false
        }
    }

    function isEmpty() {
        if (emailValid() & usernameValid() & passwordValid()) {
            $("button[type='submit']").prop('disabled', false);
        } else {
            $("button[type='submit']").prop('disabled', true);
        }
    }

    $('#id_email').keyup(function () {
        isEmpty()
    });

    $('#id_username').keyup(function () {
        isEmpty()
    });

    $('#id_password1').keyup(function () {
        isEmpty()
    });

    $('#id_password2').keyup(function () {
        isEmpty()
    });
})