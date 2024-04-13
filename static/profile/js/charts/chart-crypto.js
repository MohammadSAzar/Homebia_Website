!(function (NioApp, $) {
    "use strict";
    //////// for developer - accountBalance ////////
    // Avilable options to pass from outside
    // labels: array,
    // dataUnit: string, (Used in tooltip or other section for display)
    // datasets: [{label : string, color: string (color code with # or other format), data: array}]

    var mainBalance = {
        labels: ["01 شهریور", "02 شهریور", "03 شهریور", "04 شهریور", "05 شهریور", "06 شهریور", "07 شهریور", "08 شهریور", "09 شهریور", "10 شهریور", "11 شهریور", "12 شهریور", "13 شهریور", "14 شهریور", "15 شهریور", "16 شهریور", "17 شهریور", "18 شهریور", "19 شهریور", "20 شهریور", "21 شهریور", "22 شهریور", "23 شهریور", "24 شهریور", "25 شهریور", "26 شهریور", "27 شهریور", "28 شهریور", "29 شهریور", "30 شهریور"],
        dataUnit: 'بیت کوین',
        datasets: [{
            label: "ارسال",
            color: "#6baafe",
            data: [110, 80, 125, 55, 95, 75, 90, 110, 80, 125, 55, 95, 75, 90, 110, 80, 125, 55, 95, 75, 90, 110, 80, 125, 55, 95, 75, 90, 75, 90]
        }, {
            label: "دریافت",
            color: "#baaeff",
            data: [80, 54, 105, 120, 82, 85, 60, 80, 54, 105, 120, 82, 85, 60, 80, 54, 105, 120, 82, 85, 60, 80, 54, 105, 120, 82, 85, 60, 85, 60]
        }, {
            label: "برداشت",
            color: "#a7ccff",
            data: [90, 98, 115, 70, 87, 95, 67, 90, 98, 115, 70, 87, 95, 67, 90, 98, 115, 70, 87, 95, 67, 90, 98, 115, 70, 87, 95, 67, 95, 67]
        }]
    };

    function accountBalance(selector, set_data) {
        var $selector = (selector) ? $(selector) : $('.chart-account-balance');
        $selector.each(function () {
            var $self = $(this), _self_id = $self.attr('id'), _get_data = (typeof set_data === 'undefined') ? eval(_self_id) : set_data;

            var selectCanvas = document.getElementById(_self_id).getContext("2d");
            var chart_data = [];
            for (var i = 0; i < _get_data.datasets.length; i++) {
                chart_data.push({
                    label: _get_data.datasets[i].label,
                    data: _get_data.datasets[i].data,
                    // Styles
                    backgroundColor: _get_data.datasets[i].color,
                    borderWidth: 2,
                    borderColor: 'transparent',
                    hoverBorderColor: 'transparent',
                    borderSkipped: 'bottom',
                    barPercentage: NioApp.State.asMobile ? 1 : .75,
                    categoryPercentage: NioApp.State.asMobile ? 1 : .75
                });
            }
            var chart = new Chart(selectCanvas, {
                type: 'bar',
                data: {
                    labels: _get_data.labels,
                    datasets: chart_data,
                },
                options: {
                    plugins: {
                        legend: {
                            display: false,
                        },
                        tooltip: {
                            enabled: true,
                            rtl: NioApp.State.isRTL,
                            callbacks: {
                                label: function (context) {
                                    return `${context.parsed.y} ${_get_data.dataUnit}`;
                                },
                            },
                            backgroundColor: '#eff6ff',
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
                    maintainAspectRatio: false,
                    scales: {
                        y: {
                            display: false,
                        },
                        x: {
                            display: false,
                            ticks: {
                                reverse: NioApp.State.isRTL
                            }
                        }
                    }
                }
            });
        })
    }
    // init accountBalance
    NioApp.coms.docReady.push(function () { accountBalance(); });

    //////// for developer - referStats ////////
    // Avilable options to pass from outside
    // labels: array,
    // dataUnit: string, (Used in tooltip or other section for display)
    // datasets: [{label : string, color: string (color code with # or other format), data: array}]

    var refBarChart = {
        labels: ["01 شهریور", "02 شهریور", "03 شهریور", "04 شهریور", "05 شهریور", "06 شهریور", "07 شهریور", "08 شهریور", "09 شهریور", "10 شهریور", "11 شهریور", "12 شهریور", "13 شهریور", "14 شهریور", "15 شهریور", "16 شهریور", "17 شهریور", "18 شهریور", "19 شهریور", "20 شهریور", "21 شهریور", "22 شهریور", "23 شهریور", "24 شهریور", "25 شهریور", "26 شهریور", "27 شهریور", "28 شهریور", "29 شهریور", "30 شهریور"],
        dataUnit: 'نفر',
        datasets: [{
            label: "عضو",
            color: "#6baafe",
            data: [110, 80, 125, 55, 95, 75, 90, 110, 80, 125, 55, 95, 75, 90, 110, 80, 125, 55, 95, 75, 90, 110, 80, 125, 55, 95, 75, 90, 75, 90]
        }]
    };

    function referStats(selector, set_data) {
        var $selector = (selector) ? $(selector) : $('.chart-refer-stats');
        $selector.each(function () {
            var $self = $(this), _self_id = $self.attr('id'), _get_data = (typeof set_data === 'undefined') ? eval(_self_id) : set_data;

            var selectCanvas = document.getElementById(_self_id).getContext("2d");
            var chart_data = [];
            for (var i = 0; i < _get_data.datasets.length; i++) {
                chart_data.push({
                    label: _get_data.datasets[i].label,
                    data: _get_data.datasets[i].data,
                    // Styles
                    backgroundColor: _get_data.datasets[i].color,
                    borderWidth: 2,
                    borderColor: 'transparent',
                    hoverBorderColor: 'transparent',
                    borderSkipped: 'bottom',
                    barPercentage: .8,
                    categoryPercentage: .8
                });
            }
            var chart = new Chart(selectCanvas, {
                type: 'bar',
                data: {
                    labels: _get_data.labels,
                    datasets: chart_data,
                },
                options: {
                    plugins: {
                        legend: {
                            display: false,
                        },
                        tooltip: {
                            enabled: true,
                            rtl: NioApp.State.isRTL,
                            callbacks: {
                                label: function (context) {
                                    return `${context.parsed.y} ${_get_data.dataUnit}`;
                                },
                            },
                            backgroundColor: '#fff',
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
                    maintainAspectRatio: false,
                    scales: {
                        y: {
                            display: false,
                            ticks: {
                                beginAtZero: true
                            },
                        },
                        x: {
                            display: false,
                            ticks: {
                                reverse: NioApp.State.isRTL
                            }
                        }
                    }
                }
            });
        })
    }
    // init chart
    NioApp.coms.docReady.push(function () { referStats(); });


    //////// for developer - accountSummary ////////
    // Avilable options to pass from outside
    // labels: array,
    // dataUnit: string, (Used in tooltip or other section for display)
    // datasets: [{label : string, color: string (color code with # or other format), data: array}]
    var summaryBalance = {
        labels: ["فروردین", "اردیبهشت", "خرداد", "تیر", "مرداد", "شهریور", "مهر", "آبان", "آذر", "دی", "بهمن", "اسفند"],
        dataUnit: 'بیت کوین',
        datasets: [{
            label: "مجموع دریافت شده",
            color: "#5ce0aa",
            data: [110, 80, 125, 55, 95, 75, 90, 110, 80, 125, 55, 95]
        }, {
            label: "مجموع ارسال",
            color: "#3a8dfe",
            data: [80, 54, 105, 120, 82, 85, 60, 80, 54, 105, 120, 82]
        }, {
            label: "مجموع برداشت",
            color: "#f6ca3e",
            data: [90, 98, 115, 70, 87, 95, 67, 90, 98, 115, 70, 87]
        }]
    };

    function accountSummary(selector, set_data) {
        var $selector = (selector) ? $(selector) : $('.chart-account-summary');
        $selector.each(function () {
            var $self = $(this), _self_id = $self.attr('id'), _get_data = (typeof set_data === 'undefined') ? eval(_self_id) : set_data;
            var selectCanvas = document.getElementById(_self_id).getContext("2d");

            var chart_data = [];
            for (var i = 0; i < _get_data.datasets.length; i++) {
                chart_data.push({
                    label: _get_data.datasets[i].label,
                    tension: .4,
                    backgroundColor: 'transparent',
                    fill: true,
                    borderWidth: 2,
                    borderColor: _get_data.datasets[i].color,
                    pointBorderColor: 'transparent',
                    pointBackgroundColor: 'transparent',
                    pointHoverBackgroundColor: "#fff",
                    pointHoverBorderColor: _get_data.datasets[i].color,
                    pointBorderWidth: 2,
                    pointHoverRadius: 4,
                    pointHoverBorderWidth: 2,
                    pointRadius: 4,
                    pointHitRadius: 4,
                    data: _get_data.datasets[i].data,
                });
            }
            var chart = new Chart(selectCanvas, {
                type: 'line',
                data: {
                    labels: _get_data.labels,
                    datasets: chart_data,
                },
                options: {
                    plugins: {
                        legend: {
                            display: false,
                        },
                        tooltip: {
                            rtl: NioApp.State.isRTL,
                            callbacks: {
                                label: function (context) {
                                    return `${context.parsed.y} ${_get_data.dataUnit}`;
                                },
                            },
                            backgroundColor: '#eff6ff',
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
                    maintainAspectRatio: false,
                    scales: {
                        y: {
                            position: NioApp.State.isRTL ? "right" : "left",
                            ticks: {
                                beginAtZero: false,
                                font: {
                                    size: 12,
                                },
                                color: '#9eaecf',
                                padding: 10
                            },
                            grid: {
                                color: NioApp.hexRGB("#526484", .2),
                                tickLength: 0,
                                zeroLineColor: NioApp.hexRGB("#526484", .2),
                                drawTicks: false,
                            },
                        },
                        x: {
                            ticks: {
                                font: {
                                    size: 12,
                                },
                                color: '#9eaecf',
                                source: 'auto',
                                padding: 5,
                                reverse: NioApp.State.isRTL
                            },
                            grid: {
                                color: "transparent",
                                tickLength: 20,
                                zeroLineColor: NioApp.hexRGB("#526484", .2),
                                offset: true,
                                drawTicks: false,
                            }
                        }
                    }
                }
            });
        })
    }

    // init accountSummary
    NioApp.coms.docReady.push(function () { accountSummary(); });

})(NioApp, jQuery);