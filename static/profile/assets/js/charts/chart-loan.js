!(function (NioApp, $) {
  "use strict";


  var LoanReportDoughnutData = {
    labels: ["پرداخت شده", "باقی مانده", "پرداخت نشده"],
    dataUnit: 'قسط',
    legend: false,
    datasets: [{
      borderColor: "#fff",
      background: ["#33d895", "#f9db7b", "#ff80b7"],
      data: [36, 12, 2]
    }]
  };

  function analyticsDoughnut(selector, set_data) {
    var $selector = (selector) ? $(selector) : $('.analytics-doughnut');
    $selector.each(function () {
      var $self = $(this), _self_id = $self.attr('id'), _get_data = (typeof set_data === 'undefined') ? eval(_self_id) : set_data;
      var selectCanvas = document.getElementById(_self_id).getContext("2d");

      var chart_data = [];
      for (var i = 0; i < _get_data.datasets.length; i++) {
        chart_data.push({
          backgroundColor: _get_data.datasets[i].background,
          borderWidth: 2,
          borderColor: _get_data.datasets[i].borderColor,
          hoverBorderColor: _get_data.datasets[i].borderColor,
          data: _get_data.datasets[i].data,
        });
      }
      var chart = new Chart(selectCanvas, {
        type: 'doughnut',
        data: {
          labels: _get_data.labels,
          datasets: chart_data,
        },
        options: {
          plugins: {
            legend: {
              display: (_get_data.legend) ? _get_data.legend : false,
              rtl: NioApp.State.isRTL,
              labels: {
                boxWidth: 12,
                padding: 20,
                color: '#6783b8',
              }
            },
            tooltip: {
              enabled: true,
              rtl: NioApp.State.isRTL,
              callbacks: {
                label: function (context) {
                  return `${context.parsed} ${_get_data.dataUnit}`;
                },
              },
              backgroundColor: '#fff',
              borderColor: '#eff6ff',
              borderWidth: 2,
              titleFont: {
                size: 13,
              },
              titleColor: '#6783b8',
              titleMarginBottom: 6,
              bodyColor: '#9eaecf',
              bodyFont: {
                size: 12
              },
              bodySpacing: 4,
              padding: 10,
              footerMarginTop: 0,
              displayColors: false
            },
          },
          rotation: -1.5,
          cutoutPercentage: 70,
          maintainAspectRatio: false,
        }
      });
    })
  }
  // init chart
  NioApp.coms.docReady.push(function () { analyticsDoughnut(); });

})(NioApp, jQuery);