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

    $('#formSettings').on('submit', async function (e) {
        e.preventDefault()

        var data = new FormData()
        data.append("name", e.target.name.value)
        data.append("org", e.target.org.value)
        data.append("start", e.target.start.value)
        data.append("end", e.target.end.value)
        data.append("logo", e.target.foto.files[0])

        if (data.get('name') && data.get('org')) {
            $('.btn-simpan').children('span.spinner-border').removeClass('d-none')
            $('.btn-simpan').addClass('disabled')
            await $.ajax({
                headers: { "X-CSRFToken": token },
                type: "POST",
                url: '/adm/settings/update/',
                data: data,
                processData: false,
                contentType: false,
                cache: false,
                dataType: "json",
                enctype:"multipart/form-data",
            }).done((result) => {
                if (result.status) {
                    Swal.fire({
                        text: "Ubah pengaturan berhasil",
                        icon: "success",
                        showConfirmButton: false,
                        timer: 2000
                    }).then(() => {
                        location.reload()
                    })
                } else {
                    $('.btn-simpan').children('span.spinner-border').addClass('d-none')
                    $('.btn-simpan').removeClass('disabled')
                    Swal.fire({
                        text: result.message,
                        icon: "warning",
                        showConfirmButton: false,
                        timer: 2000
                    })
                }
            })
        }
    })
})