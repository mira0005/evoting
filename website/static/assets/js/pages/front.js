$(document).ready(function () {
    let countMulai = new Date(tglMulai)
    let countSelesai = new Date(tglSelesai)

    let days = $('#timecount #day')
    let hours = $('#timecount #hour')
    let minutes = $('#timecount #minute')
    let seconds = $('#timecount #second')

    let countdown = setInterval(function(){
        var now = new Date()

        if (((countMulai - now) / 1000) > 0){
            var timeleft = (countMulai - now) / 1000
        } else {
            var timeleft = (countSelesai - now) / 1000
        }
        if(timeleft > 0){
            updateclock(timeleft)
        }
    }, 1000)

    function updateclock(remainingTime){
        let day = Math.floor(remainingTime / 86400)
        remainingTime -= day * 86400
        let hour = Math.floor(remainingTime / 3600) % 24
        remainingTime -= hour * 3600
        let minute = Math.floor(remainingTime / 60) % 60
        remainingTime -= minute * 60
        let second = Math.floor(remainingTime % 60)

        days.text(Number(day))
        hours.text(Number(hour))
        minutes.text(Number(minute))
        seconds.text(Number(second))

        if (day <= 0 && hour <= 0 && minute <= 0 && second <= 0){
            clearInterval(countdown)
            location.reload()
        }
    }

    function Number(number){
        return number < 10 ? "0" + number : number;
    }

    $('#formLogin').on('submit', async function (e) {
        e.preventDefault()

        var data = new FormData()
        data.append("kode", e.target.kode.value)
        data.append("kode2", e.target.kode2.value)

        if (data.get('kode') && data.get('kode2')){
            $('#formLogin button').children('span').html('<span class="spinner-border spinner-border-sm mr-2" role="status" aria-hidden="true"></span>')
            $('#formLogin button').prop('disabled', true)
            await $.ajax({
                headers: { "X-CSRFToken": token },
                type: "POST",
                url: '/auth/login/',
                data: data,
                processData: false,
                contentType: false,
                cache: false,
                dataType: "json",
            }).done((result) => {
                if (result.status) {
                    Swal.fire({
                        text: "Login berhasil",
                        icon: "success",
                        showConfirmButton: false,
                        timer: 2000
                    }).then(() => {
                        location.reload()
                    })
                } else {
                    $('#formLogin button').children('span').html('<i class="uil uil-sign-out-alt mr-2"></i>')
                    $('#formLogin button').prop('disabled', false)
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