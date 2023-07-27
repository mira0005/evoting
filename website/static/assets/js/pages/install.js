$(document).ready(function () {
    (function () {
        let accountUserImage = document.getElementById('logoApp');
        const fileInput = document.querySelector('#logo')

        if (accountUserImage) {
            fileInput.onchange = () => {
                if (fileInput.files[0]) {
                    var reader = new FileReader();
                    reader.onload = function (e) {
                        accountUserImage.src = e.target.result
                    }
                    reader.readAsDataURL(fileInput.files[0])
                }
            };
        }
    })()

    $('#formInstall').on('submit', async function (e) {
        e.preventDefault()

        var data = new FormData()
        data.append("logo", e.target.logo.files[0])
        data.append("name", e.target.name.value)
        data.append("org", e.target.org.value)
        data.append("adminName", e.target.adminName.value)
        data.append("username", e.target.username.value)
        data.append("password", e.target.password.value)
        data.append("password2", e.target.password2.value)

        if (data.get('name') && data.get('org') && data.get('adminName') && data.get('username') && data.get('password') && data.get('password2')){
            $('#preloader').addClass('d-block')
            $('#preloader #status').addClass('d-block')

            await $.ajax({
                headers: { "X-CSRFToken": token },
                type: "POST",
                url: '/install-app/install/',
                data: data,
                processData: false,
                contentType: false,
                cache: false,
                dataType: "json",
                enctype:"multipart/form-data",
            }).done((result) => {
                if (result.status) {
                    $('#preloader').removeClass('d-block')
                    $('#preloader #status').removeClass('d-block')
                    Swal.fire({
                        text: "Installasi berhasil",
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