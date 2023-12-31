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

    $(".summernote-editor").summernote({
        height: 250,
        minHeight: null,
        maxHeight: null,
        focus: !1,
    })

    $("#smartwizard-circles").smartWizard({
        theme: "circles",
        useURLhash: !1,
        showStepURLhash: !1,
    })

    $('#formTambahData').on('submit', async function (e) {
        e.preventDefault()

        var data = new FormData()
        data.append("name", e.target.name.value)
        data.append("order", e.target.order.value)
        data.append("division", e.target.division.value)
        data.append("foto", e.target.foto.files[0])
        data.append("vision", e.target.vision.value)
        data.append("mission", e.target.mission.value)

        if (data.get('name') && data.get('order') && data.get('division') && data.get('foto') && data.get('vision') && data.get('mission')) {
            $('.btn-simpan').children('span.spinner-border').removeClass('d-none')
            $('.btn-simpan').addClass('disabled')
            await $.ajax({
                headers: { "X-CSRFToken": token },
                type: "POST",
                url: '/adm/candidates/add/',
                data: data,
                processData: false,
                contentType: false,
                cache: false,
                dataType: "json",
                enctype:"multipart/form-data",
            }).done((result) => {
                if (result.status) {
                    Swal.fire({
                        text: "Tambah data kandidat berhasil",
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

    $('.candidate-card').on('click', function(){
        location.href = `/adm/candidates/${$(this).attr('data-code')}/detail/`
    })

    $('[data-plugin="customselect"]').select2()
})