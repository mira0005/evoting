$(document).ready(function () {
    $('#formLogin').on('submit', async function (e) {
        e.preventDefault()

        var data = new FormData()
        data.append("username", e.target.username.value)
        data.append("password", e.target.password.value)

        if (data.get('username') && data.get('password')){
            $('#preloader').addClass('d-block')
            $('#preloader #status').addClass('d-block')

            await $.ajax({
                headers: { "X-CSRFToken": token },
                type: "POST",
                url: '/adm/auth/login/',
                data: data,
                processData: false,
                contentType: false,
                cache: false,
                dataType: "json",
            }).done((result) => {
                if (result.status) {
                    $('#preloader').removeClass('d-block')
                    $('#preloader #status').removeClass('d-block')
                    Swal.fire({
                        text: "Login berhasil",
                        icon: "success",
                        showConfirmButton: false,
                        timer: 2000
                    }).then(() => {
                        location.href = '/adm/dashboard/'
                    })
                } else {
                    $('#preloader').removeClass('d-block')
                    $('#preloader #status').removeClass('d-block')
                    Swal.fire({
                        text: result.message,
                        icon: "warning",
                        showConfirmButton: false,
                        timer: 2000
                    })
                }
            })
        } else {
            Swal.fire({
                text: "Ada form yang masih kosong!",
                icon: "warning",
                showConfirmButton: false,
                timer: 2000
            })
        }
    })
})