// Données d'exemple (remplacez-les par vos données réelles)
const dates = ['2023-01-01', '2023-02-01', '2023-03-01', '2023-04-01', '2023-05-01'];

const eloScores = [1500, 1520, 1550, 1580, 1600];

const newDates = [];
const newEloScores = [];
const newWinRates = [];

const numberOfEntries = 20;

for (let i = 0; i < numberOfEntries; i++) {
    const randomIndex = Math.floor(Math.random() * dates.length);
    newDates.push(dates[randomIndex]);

    const randomElo = eloScores[randomIndex] + Math.floor(Math.random() * 100);
    newEloScores.push(randomElo);

    const randomWinRate = Math.floor(Math.random() * 51);
    newWinRates.push(randomWinRate);
}

const months = newDates.map(newDates => {
    return new Date(newDates).toLocaleDateString('default', {month: 'long'});
})

const tooltipDates = newDates.map(date => {
    const dateComplete = new Date(date).toLocaleDateString('default', {
        year: 'numeric',
        month: 'long',
        day: 'numeric'
    });
    return dateComplete;
});

// Création du graphique
const ctx = document.getElementById('eloChart').getContext('2d');
const eloChart = new Chart(ctx, {
    type: 'line',
    data: {
        labels: months,
        datasets: [{
            label: 'Elo History',
            data: newEloScores,
            borderWidth: 4,
            pointRadius: 0, // Cacher les points
            cubicInterpolationMode: 'monotone' // Courbes lisses
        },
            {
                label: 'Winrate History',
                data: newWinRates,
                borderWidth: 4,
                pointRadius: 0, // Cacher les points
                cubicInterpolationMode: 'monotone', // Courbes lisses
                yAxisID: 'percentage',
            },
        ]
    },
    options: {
        // plugins: {legend: {display: false},},
                responsive: true,
        maintainAspectRatio: false, // Permet au graphique de ne pas maintenir un aspect ratio fixe
        title: {
            display: false,
            text: 'Historique d\'Elo'
        },
        xAxes: [{
            type: 'time',
            time: {
                unit: 'month',
                // displayFormats: {
                //     month: 'MMM' // Format pour afficher uniquement le nom du mois
                // },
                // tooltipFormat: 'MMM YYYY' // Format pour les info-bulles (tooltip)
            },
            // type: 'time',
            // time: {
            //     parser: 'YYYY-MM-DD',
            //     // tooltipFormat: 'll',
            //     tooltipFormat: 'MMM YYYY', // Format pour les info-bulles (tooltip)
            //     unit: 'month',
            //     displayFormats: {
            //         'month': 'MMM'
            //     },
            // },
            scaleLabel: {
                display: true,
                labelString: 'Date'
            },
        }],
        yAxes: [{
            scaleLabel: {
                display: true,
                labelString: 'Elo'
            }
        }],
        scales: {
            x: {
                ticks: {
                    maxTicksLimit: 5,
                }
            },
            y: {
                ticks: {
                    maxTicksLimit: 5,
                }
            },
            percentage: {
                position: 'right',
                suggestedMin: 0, // Minimum de l'axe Y
                suggestedMax: 100, // Maximum de l'axe Y

                min: 0,
                max: 100,
                ticks: {
                    maxTicksLimit: 5,
                }
            }
        },
        tooltips: {
            callbacks: {
                title: function (tooltipItem, data) {
                    return "HELLO";
                }
            }
        }
    }
});


// Sample data for games per day
var data = {
    labels: ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'],
    datasets: [{
        label: 'Number of Games',
        data: [10, 15, 8, 12, 20, 17, 11],
        backgroundColor: 'rgba(235,54,69,0.6)',
        borderColor: 'rgb(154,25,64)',
        borderWidth: 1
    }]
};

// Chart configuration
var config = {
    type: 'bar',
    data: data,
    options: {
        plugins: {legend: {display: false},},
        responsive: true,
        maintainAspectRatio: false, // Permet au graphique de ne pas maintenir un aspect ratio fixe
        scales: {
            y: {
                ticks: {
                    maxTicksLimit: 10,
                }
            },
        }
    }
};

// Get the canvas element and create the chart
var ctx2 = document.getElementById('gameChart').getContext('2d');
var myChart = new Chart(ctx2, config);

