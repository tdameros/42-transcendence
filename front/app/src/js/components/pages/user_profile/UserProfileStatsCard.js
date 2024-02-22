import {Component} from '@components';

export class UserProfileStatsCard extends Component {
  constructor() {
    super();
  }

  render() {
    this.placeholder = this.getAttribute('placeholder');
    this.title = this.getAttribute('title');
    this.value = this.getAttribute('value');
    this.icon = this.getAttribute('icon');
    this.iconBackground = this.getAttribute('icon-bg');
    this.footerValue = this.getAttribute('footer-value');
    this.valueConcatenate = this.getAttribute('value-concatenate') || '';
    this.footerTitle = this.getAttribute('footer-title');
    this.footerType = this.getAttribute('footer-type');
    if (this.placeholder === 'true') {
      return this.renderPlaceholder();
    } else {
      return this.renderWithValues();
    }
  }

  renderPlaceholder() {
    const placeholderClass = 'placeholder placeholder-lg' +
      'bg-body-secondary rounded hide-placeholder-text';
    return (`
        <div class="card placeholder-glow">
            <div class="card-body">
                <div class="row">
                    <div class="col">
                        <span class="h6 font-semibold text-sm d-block mb-2 ${placeholderClass} col-5">_</span>
                        <span class="h3 font-bold mb-0 ${placeholderClass} col-3">_</span>
                    </div>
                    <div class="col-auto">
                        <div class="icon icon-shape text-lg rounded-circle ${placeholderClass}">
                        </div>
                    </div>
                </div>
                <div class="mt-2 mb-0 text-sm">
                    <span class="text-nowrap text-xs ${placeholderClass} col-8">_</span>
                </div>
            </div>
        </div>
      `);
  }

  renderWithValues() {
    this.#generateFooterValues();
    return (`
        <div class="card">
            <div class="card-body">
                <div class="row">
                    <div class="col"><span
                            class="h6 font-semibold text-muted text-sm d-block mb-2">${this.title}</span>
                        <span class="h3 font-bold mb-0">${this.value}</span>
                    </div>
                    <div class="col-auto">
                        <div class="icon icon-shape text-white text-lg rounded-circle ${this.iconBackground}">
                            <i class="bi ${this.icon}"></i>
                        </div>
                    </div>
                </div>
                <div class="d-flex align-items-center mt-2 mb-0 text-sm"><span
                        class="badge ${this.footerValueBrackground} ${this.footerValueColor} me-2"><i
                        class="bi ${this.footerArrow} me-1"></i>${this.footerValue}</span><span
                        class="text-nowrap text-xs text-muted">${this.footerTitle}</span>
                </div>
            </div>
        </div>
    `);
  }

  #generateFooterValues() {
    if (this.footerValue < 0) {
      this.footerArrow = 'bi-arrow-down';
      this.footerValueBrackground = 'bg-soft-danger';
      this.footerValueColor = 'text-danger';
      this.footerValue = `${this.footerValue}${this.valueConcatenate}`;
      this.value = `${this.value}${this.valueConcatenate}`;
    } else {
      this.footerArrow = 'bi-arrow-up';
      this.footerValueBrackground = 'bg-soft-success';
      this.footerValueColor = 'text-success';
      this.footerValue = `+${this.footerValue}${this.valueConcatenate}`;
      this.value = `${this.value}${this.valueConcatenate}`;
    }
  }

  loadValues(mainValue, footerValue, valueConcatenate = '') {
    this.footerValue = footerValue;
    this.valueConcatenate = valueConcatenate;
    this.value = mainValue;
    this.innerHTML = this.renderWithValues() + this.style();
  }

  style() {
    return (`
      <style>
      .hide-placeholder-text {
        color: var(--bs-secondary-bg);
        background-color: var(--bs-secondary-bg)!important;
      }
      
      .icon-shape {
          width: 3rem;
          height: 3rem;
          display: flex;
          justify-content: center;
          align-items: center;
      }
      
      .bg-soft-success {
          background-color: #ccf5e7!important;
      }
      
      .bg-soft-danger {
          background-color: #ffd6e0!important;
      }
      </style>
    `);
  }
}
