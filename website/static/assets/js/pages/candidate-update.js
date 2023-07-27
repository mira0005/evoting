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

    $('#formUbahData').on('submit', async function (e) {
        e.preventDefault()

        var data = new FormData()
        data.append("name", e.target.name.value)
        data.append("order", e.target.order.value)
        data.append("division", e.target.division.value)
        data.append("foto", e.target.foto.files[0])
        data.append("vision", e.target.vision.value)
        data.append("mission", e.target.mission.value)
        data.append("code", $(this).attr("data-code"))

        if (data.get('name') && data.get('order') && data.get('division') && data.get('vision') && data.get('mission')) {
            $('.btn-simpan').children('span.spinner-border').removeClass('d-none')
            $('.btn-simpan').addClass('disabled')
            await $.ajax({
                headers: { "X-CSRFToken": token },
                type: "POST",
                url: '/adm/candidates/update/',
                data: data,
                processData: false,
                contentType: false,
                cache: false,
                dataType: "json",
                enctype:"multipart/form-data",
            }).done((result) => {
                if (result.status) {
                    Swal.fire({
                        text: "Ubah data kandidat berhasil",
                        icon: "success",
                        showConfirmButton: false,
                        timer: 2000
                    }).then(() => {
                        location.href = '/adm/candidates/'
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

    $('#btn-hapus').on('click', function(){
        Swal.fire({
            icon: 'warning',
            html: 'Apakah anda yakin ingin menghapus <b>' + $(this).attr('data') + '</b>?',
            showCancelButton: true,
            confirmButtonText: "Yakin",
            cancelButtonText: "Batal",
            confirmButtonColor: '#5369f8',
            cancelButtonColor: '#ff5c75',
        }).then((r) => {
            if (r.isConfirmed) {
                $.ajax({
                    headers: { "X-CSRFToken": token },
                    type: "POST",
                    url: '/adm/candidates/delete/',
                    data: {"code": $(this).attr("data-code")},
                    dataType: "json",
                }).done((result) => {
                    if (result.status) {
                        Swal.fire({
                            text: "Hapus data kandidat berhasil",
                            icon: "success",
                            showConfirmButton: false,
                            timer: 2000
                        }).then(() => {
                            location.href = '/adm/candidates/'
                        })
                    } else {
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

    $('[data-plugin="customselect"]').select2()
})