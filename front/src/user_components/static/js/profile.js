// Données d'exemple (remplacez-les par vos données réelles)
const dates = ['2023-01-01', '2023-02-01', '2023-03-01', '2023-04-01', '2023-05-01'];
const eloScores = [1500, 1520, 1550, 1580, 1600];

const newDates = [];
const newEloScores = [];

const numberOfEntries = 20;

for (let i = 0; i < numberOfEntries; i++) {
    const randomIndex = Math.floor(Math.random() * dates.length);
    newDates.push(dates[randomIndex]);

    const randomElo = eloScores[randomIndex] + Math.floor(Math.random() * 100);
    newEloScores.push(randomElo);
}

// Création du graphique
const ctx = document.getElementById('eloChart').getContext('2d');
const eloChart = new Chart(ctx, {
    type: 'line',
    data: {
        labels: newDates,
        datasets: [{
            label: 'Historique d\'Elo',
            data: newEloScores,
            borderWidth: 3
        }]
    },
    options: {
        responsive: true,
        title: {
            display: true,
            text: 'Historique d\'Elo'
        },
        scales: {
            xAxes: [{
                type: 'time',
                time: {
                    parser: 'YYYY-MM-DD',
                    tooltipFormat: 'll',
                    unit: 'month',
                    unitStepSize: 1,
                    displayFormats: {
                        'month': 'MMM YYYY'
                    }
                },
                scaleLabel: {
                    display: true,
                    labelString: 'Date'
                }
            }],
            yAxes: [{
                scaleLabel: {
                    display: true,
                    labelString: 'Elo'
                }
            }]
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
        responsive: true,
        scales: {
          y: {
            beginAtZero: true,
            title: {
              display: true,
              text: 'Number of Games'
            }
          },
          x: {
            title: {
              display: true,
              text: 'Days'
            }
          }
        }
      }
    };

    // Get the canvas element and create the chart
var ctx2 = document.getElementById('gameChart').getContext('2d');
var myChart = new Chart(ctx2, config);

