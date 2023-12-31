$(document).ready(function () {

    var options = {
        series: [],
        chart: {
            type: 'donut',
        },
        labels: [],
        responsive: [{
            breakpoint: 480,
            options: {
                legend: {
                    position: 'bottom'
                }
            }
        }]
    }

    var chart = new ApexCharts(document.querySelector("#grafikVoting"), options);
    chart.render();


    $.ajax({
        headers: { "X-CSRFToken": token },
        type: "GET",
        url: '/adm/dashboard/get-candidates/',
        dataType: "json",
    }).done((result) => {
        if(result.status){
            let data = result.data
            
            data.forEach(e => {
                options.labels.push(e.name)
            })
            data.forEach(e => {
                options.series.push(e.voice)
            })

            chart.update()
        }
    })

    $('#btn-refresh').on('click', function(){
        $(this).children('span').html('<span class="spinner-border spinner-border-sm mr-2" role="status" aria-hidden="true"></span>')
        $(this).attr('disabled', true)
        $.ajax({
            headers: { "X-CSRFToken": token },
            type: "GET",
            url: '/adm/dashboard/get-candidates/',
            dataType: "json",
        }).done((result) => {
            if(result.status){
                let data = result.data

                options.labels.length = 0
                options.series.length = 0
                
                data.forEach(e => {
                    options.labels.push(e.name)
                })
                data.forEach(e => {
                    options.series.push(e.voice)
                })
    
                chart.update()

                $(this).children('span').html('<i class="uil uil-refresh mr-2"></i>')
                $(this).attr('disabled', false)
            }
        })
    })
})