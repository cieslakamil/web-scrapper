let productCode = $('#product_code').attr('data');

$.ajax({
    url: "/product/" + productCode + "/get-statistics"
}).done(function(response) {
    const stats = response;
    let scoreChartCtx = document.getElementById('score-chart').getContext('2d');
    let recommendationChartCtx = document.getElementById('recommendation-chart').getContext('2d');

    let scoreChart = new Chart(scoreChartCtx, {
        type: 'bar',
        data: {

            datasets: [{
                    label: 'Liczba gwiazdek ',
                    data: stats[0],
                    backgroundColor: [
                        'rgba(255, 196, 0, 0.293)',
                        'rgba(255, 196, 0, 0.293)',
                        'rgba(255, 196, 0, 0.293)',
                        'rgba(255, 196, 0, 0.293)',
                        'rgba(255, 196, 0, 0.293)',
                    ],
                    borderColor: [
                        'rgba(255, 196, 0, 1)',
                        'rgba(255, 196, 0, 1)',
                        'rgba(255, 196, 0, 1)',
                        'rgba(255, 196, 0, 1)',
                        'rgba(255, 196, 0, 1)',
                    ],
                    borderWidth: 1
                },

            ],
            labels: ['1', '2', '3', '4', '5'],

        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                yAxes: [{
                    ticks: {
                        beginAtZero: true
                    }
                }]
            }
        }
    });
    let recommendationChart = new Chart(recommendationChartCtx, {
        type: 'doughnut',
        data: {
            datasets: [{
                data: stats[1],
                backgroundColor: [
                    'rgba(155, 155, 155, 0.5)',
                    'rgba(255, 0, 0, 0.5)',
                    'rgba(0, 255, 0, 0.5)',
                ],
            }, ],

            labels: [
                'Brak',
                'Negatywne',
                'Pozytywne'
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,

        }
    });
})