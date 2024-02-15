import {Component} from '@components';
import {Chart} from 'chart.js/auto';

export class UserProfileChart extends Component {
  constructor() {
    super();
  }

  render() {
    this.chart = null;
    this.title = this.getAttribute('title');
    this.type = this.getAttribute('type');
    this.placeholder = this.getAttribute('placeholder');
    if (this.placeholder === 'true') {
      return this.renderPlaceholder();
    } else {
      return this.renderChart();
    }
  }

  renderPlaceholder() {
    const placeholderClass = 'placeholder placeholder-lg ' +
      'bg-body-secondary rounded hide-placeholder-text';
    return (`
      <div class="card placeholder-glow">
          <div class="card-header d-flex align-items-center">
            <h5 class="mb-0 ${placeholderClass} col-6">_</h5>
          </div>
          <div class="card-body position-relative">
            <canvas class="opacity-25" style="height: 30vh;"></canvas>
            <div class="position-absolute top-50 start-50 translate-middle">
              <h2 class="text-center h3 font-bold placeholder bg-transparent">Loading data...</h2>
            </div>
          </div>
      </div>
    `);
  }

  renderChart() {
    return (`
      <div class="card">
          <div class="card-header d-flex align-items-center">
            <h5 class="mb-0">${this.title}</h5>
          </div>
          <div class="card-body">
              <canvas style="height: 30vh;"></canvas>
          </div>
      </div>
    `);
  }

  renderNoDataChart() {
    return (`
      <div class="card">
          <div class="card-header d-flex align-items-center">
            <h5 class="mb-0">${this.title}</h5>
          </div>
          <div class="card-body position-relative">
            <canvas class="opacity-25" style="height: 30vh;"></canvas>
            <div class="position-absolute top-50 start-50 translate-middle">
              <h2 class="text-center h3 font-bold bg-transparent">Not enough data</h2>
            </div>
          </div>
      </div>
    `);
  }

  postRender() {
    this.canvas = this.querySelector('canvas');
    this.ctx = this.canvas.getContext('2d');
    if (this.type === 'line') {
      this.config = this.lineChartConfig;
    } else {
      this.config = this.barChartConfig;
    }
    this.chart = new Chart(this.ctx, this.config);
  }

  get barChartConfig() {
    return {
      type: 'bar',
      data: {
        labels: [
          'January',
          'March',
          'May',
          'July',
          'September',
          'November',
          'December'],
        datasets: [{
          label: '',
          data: this.#generateRandomData(7),
          backgroundColor: 'rgb(200,200,200)',
          borderColor: 'rgb(200,200,200)',
          borderWidth: 4,
          pointRadius: 0,
        },
        ],
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        scales: {
          x: {
            ticks: {
              maxTicksLimit: 7,
            },
          },
          y: {
            ticks: {
              maxTicksLimit: 7,
            },
          },
          percentage: {
            position: 'right',
            suggestedMin: 0,
            suggestedMax: 100,

            min: 0,
            max: 100,
            ticks: {
              maxTicksLimit: 7,
            },
          },
        },
      },
    };
  }

  get lineChartConfig() {
    return {
      type: 'line',
      data: {
        labels: [
          'January',
          'March',
          'May',
          'July',
          'September',
          'November',
          'December',
        ],
        datasets: [{
          label: '',
          data: this.#generateRandomData(7),
          backgroundColor: 'rgb(200,200,200)',
          borderColor: 'rgb(200,200,200)',
          borderWidth: 4,
          pointRadius: 0,
          cubicInterpolationMode: 'monotone',
        }, {
          label: '',
          data: this.#generateRandomData(7),
          backgroundColor: 'rgb(200,200,200)',
          borderColor: 'rgb(200,200,200)',
          borderWidth: 4,
          pointRadius: 0,
          cubicInterpolationMode: 'monotone',
        },
        ],
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        scales: {
          x: {
            ticks: {
              maxTicksLimit: 7,
            },
          },
          y: {
            ticks: {
              maxTicksLimit: 7,
            },
          },
          percentage: {
            position: 'right',
            suggestedMin: 0,
            suggestedMax: 100,
            ticks: {
              maxTicksLimit: 7,
            },
          },
        },
      },
    };
  }

  loadConfig(newConfig) {
    if (this.chart) {
      this.chart.destroy();
    }
    this.innerHTML = this.renderChart() + this.style();
    this.canvas = this.querySelector('canvas');
    this.ctx = this.canvas.getContext('2d');
    this.chart = new Chart(this.ctx, newConfig);
  }

  loadNoDataChart() {
    this.innerHTML = this.renderNoDataChart() + this.style();
    this.canvas = this.querySelector('canvas');
    this.ctx = this.canvas.getContext('2d');
    if (this.type === 'line') {
      this.config = this.lineChartConfig;
    } else {
      this.config = this.barChartConfig;
    }
    if (this.chart) {
      this.chart.destroy();
    }
    this.chart = new Chart(this.ctx, this.config);
  }

  #generateRandomData(number) {
    return Array.from({length: number}, () => Math.random() * 100);
  }

  style() {
    return (`
      <style>
      .hide-placeholder-text {
        color: var(--bs-secondary-bg);
        background-color: var(--bs-secondary-bg)!important;
      }
      </style>
    `);
  }
}
