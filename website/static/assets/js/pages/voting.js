$(document).ready(function () {
    var swiper = new Swiper(".mySwiper", {
        effect: "coverflow",
        grabCursor: true,
        centeredSlides: true,
        slidesPerView: "auto",
        coverflowEffect: {
          rotate: 20,
          stretch: 0,
          depth: 100,
          modifier: 1,
          slideShadows: true
        }
    });

    $('.right-bar-toggle').on('click', function (e) {
        let name = $(this).attr('name'),
        code = $(this).attr('code'),
        foto = $(this).attr('foto'),
        order = $(this).attr('order'),
        vision = $(this).attr('vision'),
        mission = $(this).attr('mission'),
        division = $(this).attr('division')

        if(screen.width < 768){
            $('#bottom-bar #foto').attr('src', foto)
            $('#bottom-bar .btn-vote').attr('data-code', code)
            $('#bottom-bar .btn-vote').attr('data-name', name)
            $('#bottom-bar #nama').text(name)
            $('#bottom-bar #divisi').text(division)
            $('#bottom-bar #order').text(order)
            $('#bottom-bar #visi').html(vision)
            $('#bottom-bar #misi').html(mission)

            $('body').toggleClass('right-bar-enabled');
        } else {
            $('#modalCandidate #foto').attr('src', foto)
            $('#modalCandidate .btn-vote').attr('data-code', code)
            $('#modalCandidate .btn-vote').attr('data-name', name)
            $('#modalCandidate #nama').text(name)
            $('#modalCandidate #divisi').text(division)
            $('#modalCandidate #order').text(order)
            $('#modalCandidate #visi').html(vision)
            $('#modalCandidate #misi').html(mission)
            
            $('#modalCandidate').modal('show')
        }
    });

    $('.btn-vote').on('click', function () {
        Swal.fire({
            icon: 'warning',
            html: 'Apakah anda yakin ingin memilih <b>' + $(this).attr('data-name') + '</b>?',
            showCancelButton: true,
            confirmButtonText: "Yakin",
            cancelButtonText: "Batal",
            confirmButtonColor: '#6D03FE',
            cancelButtonColor: '#ff5c75',
        }).then((r) => {
            if (r.isConfirmed) {
                $(this).children('span').html('<span class="spinner-border spinner-border-sm mr-2" role="status" aria-hidden="true"></span>')
                $(this).prop('disabled', true)
                Swal.fire({
                    title: "Harap Tunggu..",
                    text: "Sedang mengkonfimasi pilihan!",
                    icon: "info",
                    allowEscapeKey: false,
                    allowOutsideClick: false,
                    showCancelButton: false,
                    showConfirmButton: false,
                    didOpen: () => {
                        Swal.showLoading()
                    }
                })
                $.ajax({
                    headers: { "X-CSRFToken": token },
                    type: "POST",
                    url: '/voting/vote/',
                    data: {"code": $(this).attr('data-code')},
                    dataType: "json",
                }).done((result) => {
                    if (result.status) {
                        Swal.fire({
                            html: "Berhasil vote <b>" + $(this).attr('data-name') + "</b>",
                            icon: "success",
                            showConfirmButton: false,
                            timer: 2000
                        }).then(() => {
                            location.href = '/grafik/'
                        })
                    } else {
                        $(this).children('span').html('<i class="uil uil-sign-out-alt mr-2"></i>')
                        $(this).prop('disabled', false)
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

    $(document).on('click', 'body', function (e) {
        if ($(e.target).closest('.right-bar-toggle, .right-bar').length > 0) {
            return;
        }

        if ($(e.target).closest('.left-side-menu, .side-nav').length > 0 || $(e.target).hasClass('button-menu-mobile')
            || $(e.target).closest('.button-menu-mobile').length > 0) {
            return;
        }

        $('body').removeClass('right-bar-enabled');
        $('body').removeClass('sidebar-enable');
        return;
    });

    $('.btn-login').on('click', function(){
        $('#modalCandidate').modal('hide')
        $('body').toggleClass('right-bar-enabled');
    })
})