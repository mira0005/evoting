$(document).ready(function () {
  
  var option1 = {
    chart: { height: 380, type: "bar", toolbar: { show: !1 } },
    plotOptions: { 
        bar: { 
            borderRadius: 10, 
            dataLabels: { 
                position: "top" 
            },
            distributed: true
        } 
    },
    colors: ['#5369f8', '#43d39e', '#ff5c75', '#25c2e3', '#ffbe0b'],
    dataLabels: {
      enabled: true,
      formatter: function (e) {
        return e + " suara";
      },
      offsetY: -30,
      style: { fontSize: "12px" },
    },
    series: [
      {
        name: "Suara",
        data: [],
      },
    ],
    xaxis: {
      categories: [],
      position: "top",
      labels: { offsetY: -18 },
      axisBorder: { show: !1 },
      axisTicks: { show: !1 },
      tooltip: { enabled: !0, offsetY: -35 },
    },
    yaxis: {
      axisBorder: { show: !1 },
      axisTicks: { show: !1 },
      labels: {
        show: !1,
        formatter: function (e) {
          return e + " suara";
        },
      },
    },
    title: {
      text: "Grafik Perolehan Suara",
      floating: !0,
      offsetY: 350,
      align: "center",
      style: { color: "#444" },
    },
    grid: {
      row: { colors: ["transparent", "transparent"], opacity: 0.2 },
      borderColor: "#5369f8",
    },
  };
  var chart1 =  new ApexCharts(document.querySelector("#grafikVoting"), option1);
  chart1.render()

  $.ajax({
        headers: { "X-CSRFToken": token },
        type: "GET",
        url: '/adm/dashboard/get-candidates/',
        dataType: "json",
    }).done((result) => {
        if(result.status){
            let data = result.data

            data.forEach(e => {
                option1.xaxis.categories.push(e.name)
            });

            data.forEach(e => {
                option1.series[0].data.push(e.voice)
            })

            chart1.update()
        }
    })

    var option2 = {
      plotOptions: { 
        pie: { 
          donut: { 
            size: "70%" 
          }, 
          expandOnClick: !1 
        } 
      },
      chart: { 
        type: "donut" 
      },
      colors: ['#43d39e', '#ff5c75'],
      legend: {
          show: !0,
          position: "right",
          horizontalAlign: "left",
          itemMargin: { horizontal: 6, vertical: 3 },
      },
      series: [],
      labels: [],
      responsive: [
          { breakpoint: 480, options: { legend: { position: "bottom" } } },
      ],
      tooltip: {
      y: {
          formatter: function (t) {
          return t + " orang";
          },
      },
      },
    };
    var chart2 = new ApexCharts(document.querySelector("#grafikVoter"), option2)
    chart2.render();

    $.ajax({
        headers: { "X-CSRFToken": token },
        type: "GET",
        url: '/adm/dashboard/get-voters/',
        dataType: "json",
    }).done((result) => {
        if(result.status){
            let data = result.data

            data.forEach(e => {
                option2.labels.push(e.name)
            })

            data.forEach(e => {
                option2.series.push(e.total)
            })

            chart2.update()
        }
    })
})