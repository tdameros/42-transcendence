import {Component} from '@components';

export class UserProfileChartsCards extends Component {
  constructor() {
    super();
  }

  render() {
    return (`
      <div class="row gx-3 gy-2 mb-4 mt-3">
        <div class="col-md-6">
            <user-profile-chart-component id="rank-graph"
                                          title="Rank History"
                                          type="line"
                                          placeholder="true">
            </user-profile-chart-component>
        </div>
        <div class="col-md-6">
            <user-profile-chart-component id="match-graph"
                                          title="Matches Played History"
                                          type="bar"
                                          placeholder="true">
            </user-profile-chart-component>
        </div>
     </div>
    `);
  }

  style() {
    return (`
      <style>

      </style>
    `);
  }

  postRender() {
    this.rankGraph = this.querySelector('#rank-graph');
    this.matchGraph = this.querySelector('#match-graph');
  }

  loadStatistics(eloGraph, winRateGraph, matchesPlayedGraph) {
    const {graph: eloGraphData} = eloGraph;
    const {graph: winRateGraphData} = winRateGraph;
    const {graph: matchesPlayedGraphData} = matchesPlayedGraph;

    const RankDates = eloGraphData.map((objet) => objet.date);
    const eloScores = eloGraphData.map((objet) => objet.value);
    const winRates = winRateGraphData.map((objet) => objet.value);
    const matchesPlayed = matchesPlayedGraphData.map((objet) => objet.value);
    const matchDates = matchesPlayedGraphData.map((objet) => objet.date);

    if (eloScores.length === 1 || winRates.length === 1) {
      this.rankGraph.loadNoDataChart();
    } else {
      this.rankGraph.loadConfig(
          this.#generateRankConfig(RankDates, eloScores, winRates),
      );
    }

    const totalMatchesPlayed = matchesPlayed.reduce(
        (acc, value) => acc + value, 0,
    );
    if (totalMatchesPlayed === 0) {
      this.matchGraph.loadNoDataChart();
    } else {
      this.matchGraph.loadConfig(
          this.#generateMatchConfig(matchDates, matchesPlayed),
      );
    }
  }

  #generateRankConfig(dates, eloScores, winRates) {
    winRates = winRates.map((rate) => rate.toFixed(2));
    const labels = Array.from(
        dates, (date) => this.#formatDateWithoutTime(date),
    );
    const labelsToolTip = Array.from(dates,
        (date) => this.#formatDateWithTime(date),
    );
    return {
      type: 'line',
      data: {
        labels: labels,
        datasets: [{
          label: 'Elo',
          data: eloScores,
          labelsToolTip: labelsToolTip,
          borderWidth: 4,
          pointRadius: 0,
          cubicInterpolationMode: 'monotone',
        },
        {
          label: 'Win Rate',
          data: winRates,
          labelsToolTip: labelsToolTip,
          borderWidth: 4,
          pointRadius: 0,
          cubicInterpolationMode: 'monotone',
          yAxisID: 'percentage',
        },
        ],
      },
      options: {
        plugins: {
          tooltip: {
            callbacks: {
              title: function(tooltipItems) {
                try {
                  const index = tooltipItems[0].parsed.x;
                  return tooltipItems[0].dataset.labelsToolTip[index];
                } catch (error) { }
              },
              label: function(tooltipItems) {
                try {
                  const unit = tooltipItems.datasetIndex === 0 ? '' : '%';
                  return `${tooltipItems.dataset.label} : ${tooltipItems.parsed.y}${unit}`;
                } catch (error) { }
              },
            },
          },
        },
        interaction: {
          intersect: false,
        },
        responsive: true,
        maintainAspectRatio: false,
        xAxes: [{
          scaleLabel: {
            display: true,
            labelString: 'Date',
          },
        }],
        yAxes: [{
          scaleLabel: {
            display: true,
            labelString: 'Elo',
          },
        }],
        scales: {
          x: {
            ticks: {
              maxTicksLimit: 5,
            },
          },
          y: {
            ticks: {
              maxTicksLimit: 5,
            },
          },
          percentage: {
            position: 'right',
            suggestedMin: 0,
            suggestedMax: 100,
            ticks: {
              maxTicksLimit: 5,
              callback: function(value, index, values) {
                try {
                  return value + '%';
                } catch (error) { }
              },
            },
          },
        },
      },
    };
  }

  #generateMatchConfig(dates, matchesPlayed) {
    return {
      type: 'bar',
      data: {
        labels: [
          'Monday',
          'Tuesday',
          'Wednesday',
          'Thursday',
          'Friday',
          'Saturday',
          'Sunday',
        ],
        datasets: [{
          label: 'Number of Games',
          data: matchesPlayed,
          backgroundColor: 'rgba(254,100,132,1)',
        }],
      },
      options: {
        plugins: {
          legend: {
            display: false,
          },
        },
        responsive: true,
        maintainAspectRatio: false,
        scales: {
          y: {
            ticks: {
              maxTicksLimit: 10,
            },
          },
        },
      },
    };
  }

  #formatDateWithTime(isoDateString) {
    const date = new Date(isoDateString);
    const options = {
      day: 'numeric',
      month: 'short',
      hour: '2-digit',
      minute: '2-digit',
    };
    return date.toLocaleString('en-US', options);
  }

  #formatDateWithoutTime(isoDateString) {
    const date = new Date(isoDateString);
    const options = {day: 'numeric', month: 'short'};
    return date.toLocaleString('en-US', options);
  }
}
