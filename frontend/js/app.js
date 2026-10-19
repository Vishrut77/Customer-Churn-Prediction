/**
 * Customer Churn Prediction Dashboard - Main Application Logic
 * Modular Vanilla JavaScript interacting with FastAPI endpoints:
 * - GET  /api/dashboard
 * - GET  /api/customers
 * - POST /api/predict
 */

(function () {
  'use strict';

  // =========================================================================
  // 1. Constants & Configuration
  // =========================================================================

  const API_ENDPOINTS = {
    DASHBOARD: '/api/dashboard',
    CUSTOMERS: '/api/customers',
    PREDICT: '/api/predict',
  };

  const BINARY_FIELDS = [
    'SeniorCitizen',
    'Partner',
    'Dependents',
    'PhoneService',
    'MultipleLines',
    'OnlineSecurity',
    'OnlineBackup',
    'DeviceProtection',
    'TechSupport',
    'StreamingTV',
    'StreamingMovies',
    'PaperlessBilling',
  ];

  const CATEGORICAL_FIELDS = [
    'InternetService',
    'Contract',
    'PaymentMethod',
  ];

  const NUMERIC_FIELDS = [
    'tenure',
    'MonthlyCharges',
    'TotalCharges',
  ];

  // Presets for rapid testing
  const PRESET_HIGH_RISK = {
    tenure: '3',
    Contract: 'Month-to-month',
    PaymentMethod: 'Electronic check',
    MonthlyCharges: '89.85',
    TotalCharges: '269.55',
    PaperlessBilling: 'Yes',
    SeniorCitizen: 'No',
    Partner: 'No',
    Dependents: 'No',
    PhoneService: 'Yes',
    MultipleLines: 'Yes',
    InternetService: 'Fiber optic',
    OnlineSecurity: 'No',
    OnlineBackup: 'No',
    DeviceProtection: 'No',
    TechSupport: 'No',
    StreamingTV: 'Yes',
    StreamingMovies: 'Yes',
  };

  const PRESET_LOYAL = {
    tenure: '62',
    Contract: 'Two year',
    PaymentMethod: 'Bank transfer (automatic)',
    MonthlyCharges: '59.90',
    TotalCharges: '3713.80',
    PaperlessBilling: 'No',
    SeniorCitizen: 'No',
    Partner: 'Yes',
    Dependents: 'Yes',
    PhoneService: 'Yes',
    MultipleLines: 'Yes',
    InternetService: 'DSL',
    OnlineSecurity: 'Yes',
    OnlineBackup: 'Yes',
    DeviceProtection: 'Yes',
    TechSupport: 'Yes',
    StreamingTV: 'Yes',
    StreamingMovies: 'No',
  };

  // State Management
  const state = {
    customers: {
      data: [],
      total: 0,
      page: 1,
      limit: 10,
      search: '',
      churn: 'all',
      contract: 'all',
      selectedCustomer: null,
      isLoading: false,
    },
    dashboard: {
      data: null,
      isLoading: false,
    },
    charts: {
      contract: null,
      tenure: null,
      charges: null,
    },
    backendConnected: false,
  };

  // =========================================================================
  // 2. DOM Element Selectors
  // =========================================================================

  const DOM = {
    statusPill: document.getElementById('backend-status-pill'),
    statusDot: document.getElementById('status-indicator'),
    statusText: document.getElementById('status-text'),
    globalAlertContainer: document.getElementById('global-alert-container'),

    // KPI Cards
    kpiTotal: document.getElementById('kpi-total-customers'),
    kpiChurned: document.getElementById('kpi-churned-customers'),
    kpiRetained: document.getElementById('kpi-retained-customers'),
    kpiRate: document.getElementById('kpi-churn-rate'),
    kpiRateTag: document.getElementById('kpi-rate-tag'),

    // Canvas elements
    canvasContract: document.getElementById('chart-contract'),
    canvasTenure: document.getElementById('chart-tenure'),
    canvasCharges: document.getElementById('chart-charges'),

    // Customer table & controls
    searchInput: document.getElementById('customer-search-input'),
    btnClearSearch: document.getElementById('btn-clear-search'),
    churnFilter: document.getElementById('churn-filter-select'),
    contractFilter: document.getElementById('contract-filter-select'),
    pageSizeSelect: document.getElementById('page-size-select'),
    btnScrollLeft: document.getElementById('btn-scroll-left'),
    btnScrollRight: document.getElementById('btn-scroll-right'),
    btnExportCsv: document.getElementById('btn-export-csv'),
    btnRefreshTable: document.getElementById('btn-refresh-table'),
    tableContainer: document.getElementById('table-scroll-container'),
    tableBody: document.getElementById('customer-table-body'),
    tableInfo: document.getElementById('table-pagination-info'),
    btnPrevPage: document.getElementById('btn-prev-page'),
    btnNextPage: document.getElementById('btn-next-page'),
    pageIndicator: document.getElementById('current-page-indicator'),

    // Prediction Form
    predictionForm: document.getElementById('churn-prediction-form'),
    predictCard: document.querySelector('.predict-form-card'),
    btnPredictSubmit: document.getElementById('btn-predict-submit'),
    btnPredictSpinner: document.getElementById('btn-predict-spinner'),
    btnPredictText: document.getElementById('btn-predict-text'),
    formValidationAlert: document.getElementById('form-validation-alert'),
    btnLoadHighRisk: document.getElementById('btn-load-high-risk'),
    btnLoadLowRisk: document.getElementById('btn-load-low-risk'),
    btnClearForm: document.getElementById('btn-clear-form'),

    // Result Card
    resultCard: document.getElementById('prediction-result-card'),
    resultStandbyView: document.getElementById('result-standby-view'),
    resultActiveView: document.getElementById('result-active-view'),
    resultOutcomeBanner: document.getElementById('result-outcome-banner'),
    resultIconContainer: document.getElementById('result-icon-container'),
    resultPredictionTitle: document.getElementById('result-prediction-title'),
    resultPredictionSubtitle: document.getElementById('result-prediction-subtitle'),
    resultProbabilityText: document.getElementById('result-probability-text'),
    resultProgressFill: document.getElementById('result-progress-fill'),
    resultExplanationText: document.getElementById('result-explanation-text'),
    resultTimestampBadge: document.getElementById('result-timestamp-badge'),
    btnPredictAnother: document.getElementById('btn-predict-another'),

    // Customer Inspection Modal
    modalBackdrop: document.getElementById('customer-modal-backdrop'),
    modalCustomerTitle: document.getElementById('modal-customer-title'),
    modalCustomerSubtitle: document.getElementById('modal-customer-subtitle'),
    modalChurnBadge: document.getElementById('modal-churn-badge'),
    modalCustomerContent: document.getElementById('modal-customer-content'),
    btnCloseModal: document.getElementById('btn-close-modal'),
    btnModalDismiss: document.getElementById('btn-modal-dismiss'),
    btnModalPredict: document.getElementById('btn-modal-predict-action'),

    // Toast Container
    toastContainer: document.getElementById('toast-container'),

    // Nav links
    navLinks: document.querySelectorAll('.nav-link'),
  };

  // =========================================================================
  // 3. Helper Functions
  // =========================================================================

  function formatNumber(num) {
    if (num === null || num === undefined || isNaN(num)) return '--';
    return new Intl.NumberFormat('en-US').format(num);
  }

  function formatCurrency(amount) {
    if (amount === null || amount === undefined || isNaN(amount)) return '$0.00';
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: 'USD',
      minimumFractionDigits: 2,
    }).format(amount);
  }

  function setBackendStatus(isOnline, message) {
    state.backendConnected = isOnline;
    if (DOM.statusDot && DOM.statusText) {
      DOM.statusDot.className = 'status-dot ' + (isOnline ? 'online' : 'offline');
      DOM.statusText.textContent = message || (isOnline ? 'Backend Connected' : 'Backend Offline');
    }
  }

  function showAlert(message, type = 'error', container = DOM.globalAlertContainer) {
    if (!container) return;
    const banner = document.createElement('div');
    banner.className = `alert-banner ${type}`;
    banner.innerHTML = `
      <div class="alert-message">
        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
          ${
            type === 'error'
              ? '<circle cx="12" cy="12" r="10"></circle><line x1="12" y1="8" x2="12" y2="12"></line><line x1="12" y1="16" x2="12.01" y2="16"></line>'
              : '<path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path><polyline points="22 4 12 14.01 9 11.01"></polyline>'
          }
        </svg>
        <span>${message}</span>
      </div>
      <button type="button" class="alert-close" aria-label="Close notification">&times;</button>
    `;
    const closeBtn = banner.querySelector('.alert-close');
    closeBtn.addEventListener('click', () => banner.remove());
    container.innerHTML = '';
    container.appendChild(banner);
  }

  function clearAlert(container = DOM.globalAlertContainer) {
    if (container) container.innerHTML = '';
  }

  // =========================================================================
  // 4. Dashboard Analytics & Charts
  // =========================================================================

  async function fetchDashboardData() {
    state.dashboard.isLoading = true;
    renderKpiLoadingState();

    try {
      const response = await fetch(API_ENDPOINTS.DASHBOARD);
      if (!response.ok) {
        throw new Error(`HTTP ${response.status}: ${response.statusText}`);
      }
      const data = await response.json();
      state.dashboard.data = data;
      setBackendStatus(true, 'Backend Connected');
      clearAlert(DOM.globalAlertContainer);

      renderKpiCards(data);
      renderAnalyticsCharts(data);
    } catch (error) {
      console.warn('Dashboard fetch error:', error);
      setBackendStatus(false, 'Backend Offline');
      renderKpiErrorState();
      renderAnalyticsChartsError();
      showAlert(
        `Unable to reach FastAPI backend at <code>${API_ENDPOINTS.DASHBOARD}</code>. Please ensure the backend server is running.`,
        'error',
        DOM.globalAlertContainer
      );
    } finally {
      state.dashboard.isLoading = false;
    }
  }

  function renderKpiLoadingState() {
    if (DOM.kpiTotal) DOM.kpiTotal.innerHTML = '<span class="skeleton" style="display:inline-block; width:80px; height:32px;"></span>';
    if (DOM.kpiChurned) DOM.kpiChurned.innerHTML = '<span class="skeleton" style="display:inline-block; width:80px; height:32px;"></span>';
    if (DOM.kpiRetained) DOM.kpiRetained.innerHTML = '<span class="skeleton" style="display:inline-block; width:80px; height:32px;"></span>';
    if (DOM.kpiRate) DOM.kpiRate.innerHTML = '<span class="skeleton" style="display:inline-block; width:80px; height:32px;"></span>';
  }

  function renderKpiErrorState() {
    if (DOM.kpiTotal) DOM.kpiTotal.textContent = '--';
    if (DOM.kpiChurned) DOM.kpiChurned.textContent = '--';
    if (DOM.kpiRetained) DOM.kpiRetained.textContent = '--';
    if (DOM.kpiRate) DOM.kpiRate.textContent = '--%';
  }

  function renderKpiCards(data) {
    // Backend returns stats nested under data.stats
    const statsObj = data.stats ?? data;
    const total = statsObj.total_customers ?? statsObj.totalCustomers ?? statsObj.total ?? 0;
    const churned = statsObj.churned_customers ?? statsObj.churnedCustomers ?? statsObj.churned ?? 0;
    const retained = statsObj.retained_customers ?? statsObj.retainedCustomers ?? statsObj.retained ?? (total - churned);

    let rate = statsObj.churn_rate ?? statsObj.churnRate;
    if (rate === undefined || rate === null) {
      rate = total > 0 ? (churned / total) * 100 : 0;
    } else if (typeof rate === 'number' && rate <= 1 && total > 0) {
      // If returned as decimal between 0 and 1
      rate = rate * 100;
    }

    if (DOM.kpiTotal) DOM.kpiTotal.textContent = formatNumber(total);
    if (DOM.kpiChurned) DOM.kpiChurned.textContent = formatNumber(churned);
    if (DOM.kpiRetained) DOM.kpiRetained.textContent = formatNumber(retained);
    if (DOM.kpiRate) DOM.kpiRate.textContent = `${Number(rate).toFixed(1)}%`;

    if (DOM.kpiRateTag) {
      if (rate > 30) {
        DOM.kpiRateTag.className = 'kpi-badge badge-danger';
        DOM.kpiRateTag.textContent = 'High Churn';
      } else if (rate > 20) {
        DOM.kpiRateTag.className = 'kpi-badge badge-warning';
        DOM.kpiRateTag.textContent = 'Moderate Churn';
      } else {
        DOM.kpiRateTag.className = 'kpi-badge badge-success';
        DOM.kpiRateTag.textContent = 'Healthy Retention';
      }
    }
  }

  // --- Chart.js Visualization Builders ---

  function renderAnalyticsCharts(data) {
    if (typeof Chart === 'undefined') {
      console.error('Chart.js library not loaded');
      return;
    }

    // Default chart font & styling tokens
    Chart.defaults.font.family = "'Plus Jakarta Sans', -apple-system, sans-serif";
    Chart.defaults.color = '#64748b';

    renderContractChart(data);
    renderTenureChart(data);
    renderChargesChart(data);
  }

  function renderContractChart(data) {
    if (!DOM.canvasContract) return;

    if (state.charts.contract) {
      state.charts.contract.destroy();
    }

    // Extract contract breakdown if provided by API
    const contractData = data.churn_by_contract ?? data.contract_churn ?? data.contracts;
    // Compute retained from customers - churned if not provided
    if (Array.isArray(contractData)) {
      contractData.forEach(c => { if (c.retained === undefined) c.retained = (c.customers ?? 0) - (c.churned ?? 0); });
    }
    let labels = ['Month-to-month', 'One year', 'Two year'];
    let retainedValues = [0, 0, 0];
    let churnedValues = [0, 0, 0];

    if (contractData) {
      if (Array.isArray(contractData)) {
        labels = contractData.map(c => c.contract ?? c.name);
        retainedValues = contractData.map(c => c.retained ?? 0);
        churnedValues = contractData.map(c => c.churned ?? 0);
      } else if (typeof contractData === 'object') {
        labels = Object.keys(contractData);
        retainedValues = labels.map(k => contractData[k].retained ?? 0);
        churnedValues = labels.map(k => contractData[k].churned ?? 0);
      }
    } else {
      // If backend did not provide chart data, display empty message or fallback
      renderChartEmptyState(DOM.canvasContract, 'Contract churn data not returned by backend');
      return;
    }

    state.charts.contract = new Chart(DOM.canvasContract, {
      type: 'bar',
      data: {
        labels,
        datasets: [
          {
            label: 'Retained',
            data: retainedValues,
            backgroundColor: '#10b981',
            borderRadius: 4,
          },
          {
            label: 'Churned',
            data: churnedValues,
            backgroundColor: '#f43f5e',
            borderRadius: 4,
          },
        ],
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: { position: 'top', labels: { boxWidth: 12, font: { weight: '600' } } },
          tooltip: {
            callbacks: {
              afterLabel: function(context) {
                const total = (retainedValues[context.dataIndex] || 0) + (churnedValues[context.dataIndex] || 0);
                if (total > 0 && context.datasetIndex === 1) {
                  const rate = ((context.raw / total) * 100).toFixed(1);
                  return `Churn Rate: ${rate}%`;
                }
                return '';
              }
            }
          }
        },
        scales: {
          x: { grid: { display: false } },
          y: { grid: { color: '#f1f5f9' }, beginAtZero: true },
        },
      },
    });
  }

  function renderTenureChart(data) {
    if (!DOM.canvasTenure) return;

    if (state.charts.tenure) {
      state.charts.tenure.destroy();
    }

    const tenureData = data.churn_by_tenure ?? data.tenure_churn ?? data.tenure_groups;
    let labels = ['0-12m', '13-24m', '25-48m', '49-72m'];
    let retainedValues = [];
    let churnedValues = [];

    if (tenureData) {
      if (Array.isArray(tenureData)) {
        // Backend returns tenure_group key
        labels = tenureData.map(t => t.tenure_group ?? t.group ?? t.tier ?? t.name);
        churnedValues = tenureData.map(t => t.churned ?? 0);
        retainedValues = tenureData.map(t => t.retained ?? ((t.customers ?? 0) - (t.churned ?? 0)));
      } else if (typeof tenureData === 'object') {
        labels = Object.keys(tenureData);
        retainedValues = labels.map(k => tenureData[k].retained ?? 0);
        churnedValues = labels.map(k => tenureData[k].churned ?? 0);
      }
    } else {
      renderChartEmptyState(DOM.canvasTenure, 'Tenure distribution data not returned by backend');
      return;
    }

    state.charts.tenure = new Chart(DOM.canvasTenure, {
      type: 'bar',
      data: {
        labels: labels.map(l => String(l).includes('m') ? l : `${l} mos`),
        datasets: [
          {
            label: 'Retained',
            data: retainedValues,
            backgroundColor: '#10b981',
            borderRadius: 4,
          },
          {
            label: 'Churned',
            data: churnedValues,
            backgroundColor: '#f43f5e',
            borderRadius: 4,
          },
        ],
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: { position: 'top', labels: { boxWidth: 12, font: { weight: '600' } } },
          tooltip: {
            callbacks: {
              afterLabel: function(context) {
                const total = (retainedValues[context.dataIndex] || 0) + (churnedValues[context.dataIndex] || 0);
                if (total > 0 && context.datasetIndex === 1) {
                  const rate = ((context.raw / total) * 100).toFixed(1);
                  return `Churn Rate: ${rate}%`;
                }
                return '';
              }
            }
          }
        },
        scales: {
          x: { grid: { display: false } },
          y: { grid: { color: '#f1f5f9' }, beginAtZero: true },
        },
      },
    });
  }

  function renderChargesChart(data) {
    if (!DOM.canvasCharges) return;

    if (state.charts.charges) {
      state.charts.charges.destroy();
    }

    // Backend returns average_charges_by_churn: [{churn: 'No', average_monthly_charges: X}, {churn: 'Yes', average_monthly_charges: Y}]
    const chargesData = data.average_charges_by_churn ?? data.avg_monthly_charges ?? data.charges_churn ?? data.monthly_charges_comparison;
    let retainedAvg = 0;
    let churnedAvg = 0;

    if (chargesData) {
      if (Array.isArray(chargesData)) {
        chargesData.forEach(item => {
          const churnVal = String(item.churn ?? '').toLowerCase();
          const avg = item.average_monthly_charges ?? item.avg ?? item.average ?? 0;
          if (churnVal === 'no' || churnVal === '0' || churnVal === 'retained') retainedAvg = avg;
          else if (churnVal === 'yes' || churnVal === '1' || churnVal === 'churned') churnedAvg = avg;
        });
      } else {
        retainedAvg = chargesData.retained ?? chargesData.non_churned ?? chargesData[0] ?? 0;
        churnedAvg = chargesData.churned ?? chargesData[1] ?? 0;
      }
    } else {
      renderChartEmptyState(DOM.canvasCharges, 'Average charges metric not returned by backend');
      return;
    }

    state.charts.charges = new Chart(DOM.canvasCharges, {
      type: 'bar',
      data: {
        labels: ['Retained Customers', 'Churned Customers'],
        datasets: [
          {
            label: 'Avg Monthly Spend ($)',
            data: [retainedAvg, churnedAvg],
            backgroundColor: ['#10b981', '#f43f5e'],
            borderRadius: 6,
            barThickness: 50,
          },
        ],
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: { display: false },
          tooltip: {
            callbacks: {
              label: context => `Average Spend: $${Number(context.raw).toFixed(2)}/mo`,
            },
          },
        },
        scales: {
          x: { grid: { display: false } },
          y: {
            grid: { color: '#f1f5f9' },
            beginAtZero: true,
            ticks: {
              callback: value => `$${value}`,
            },
          },
        },
      },
    });
  }

  function renderChartEmptyState(canvas, message) {
    const parent = canvas.parentElement;
    if (!parent) return;
    const existing = parent.querySelector('.chart-notice');
    if (existing) existing.remove();

    canvas.style.display = 'none';
    const notice = document.createElement('div');
    notice.className = 'chart-notice';
    notice.style.cssText = 'height:100%; display:flex; align-items:center; justify-content:center; text-align:center; color:#94a3b8; font-size:0.875rem; padding:1rem;';
    notice.innerHTML = `<span>${message}</span>`;
    parent.appendChild(notice);
  }

  function renderAnalyticsChartsError() {
    [DOM.canvasContract, DOM.canvasTenure, DOM.canvasCharges].forEach(canvas => {
      if (canvas) renderChartEmptyState(canvas, 'Awaiting connection to FastAPI backend');
    });
  }

  // =========================================================================
  // 5. Customer Records Table, Search & Pagination
  // =========================================================================

  // Helper badge renderers for all 21 dataset features
  function renderBoolBadge(val) {
    const isYes = val === 1 || val === '1' || val === 'Yes' || val === true;
    const isNo =
      val === 0 ||
      val === '0' ||
      val === 'No' ||
      val === false ||
      String(val).toLowerCase().includes('no');
    if (isYes) return `<span class="badge-tag yes">Yes</span>`;
    if (isNo) return `<span class="badge-tag no">No</span>`;
    return `<span class="badge-tag no">${val ?? '--'}</span>`;
  }

  function renderGenderBadge(gender) {
    if (!gender) return '--';
    const g = String(gender).toLowerCase();
    if (g === 'female') return `<span class="badge-tag female">Female</span>`;
    if (g === 'male') return `<span class="badge-tag male">Male</span>`;
    return `<span class="badge-tag">${gender}</span>`;
  }

  function renderInternetBadge(service) {
    if (!service) return '--';
    const s = String(service);
    if (s.toLowerCase().includes('fiber')) return `<span class="badge-tag fiber">Fiber Optic</span>`;
    if (s.toLowerCase().includes('dsl')) return `<span class="badge-tag dsl">DSL</span>`;
    return `<span class="badge-tag no">None</span>`;
  }

  function renderContractBadge(contract) {
    if (!contract) return '--';
    const c = String(contract);
    if (c.toLowerCase().includes('month')) return `<span class="badge-tag contract-month">Month-to-month</span>`;
    if (c.toLowerCase().includes('two')) return `<span class="badge-tag contract-twoyear">Two year</span>`;
    if (c.toLowerCase().includes('one')) return `<span class="badge-tag contract-year">One year</span>`;
    return `<span class="badge-tag contract-year">${contract}</span>`;
  }

  function renderPaymentBadge(payment) {
    if (!payment) return '--';
    return `<span class="badge-tag payment" title="${payment}">${payment}</span>`;
  }

  function showToast(message, type = 'info', duration = 3200) {
    if (!DOM.toastContainer) return;
    const toast = document.createElement('div');
    toast.className = `toast ${type}`;
    toast.innerHTML = `
      <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
        <path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path>
        <polyline points="22 4 12 14.01 9 11.01"></polyline>
      </svg>
      <span>${message}</span>
    `;
    DOM.toastContainer.appendChild(toast);
    setTimeout(() => {
      toast.style.animation = 'toastFadeOut 250ms ease forwards';
      setTimeout(() => toast.remove(), 250);
    }, duration);
  }

  function exportCustomersToCsv() {
    if (!state.customers.data || state.customers.data.length === 0) {
      showToast('No customer records loaded to export.', 'info');
      return;
    }

    const columns = [
      'customerID', 'gender', 'SeniorCitizen', 'Partner', 'Dependents',
      'tenure', 'PhoneService', 'MultipleLines', 'InternetService',
      'OnlineSecurity', 'OnlineBackup', 'DeviceProtection', 'TechSupport',
      'StreamingTV', 'StreamingMovies', 'Contract', 'PaperlessBilling',
      'PaymentMethod', 'MonthlyCharges', 'TotalCharges', 'Churn'
    ];

    const headerLine = columns.join(',');
    const rowsLines = state.customers.data.map(row => {
      return columns.map(col => {
        let val = row[col] ?? '';
        let strVal = String(val).replace(/"/g, '""');
        if (strVal.includes(',') || strVal.includes('"') || strVal.includes('\n')) {
          return `"${strVal}"`;
        }
        return strVal;
      }).join(',');
    });

    const csvContent = [headerLine, ...rowsLines].join('\n');
    const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
    const url = URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.setAttribute('download', `customer_churn_page_${state.customers.page}.csv`);
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    URL.revokeObjectURL(url);
    showToast(`Exported ${state.customers.data.length} records to CSV!`, 'success');
  }

  function openCustomerModal(customer) {
    if (!DOM.modalBackdrop || !customer) return;
    state.customers.selectedCustomer = customer;

    const idDisplay = customer.customerID ?? customer.id ?? 'Profile Details';
    const isChurned =
      customer.Churn === 1 ||
      customer.Churn === '1' ||
      customer.Churn === 'Yes' ||
      customer.churn === 1 ||
      customer.churn === 'Yes';

    if (DOM.modalCustomerTitle) {
      DOM.modalCustomerTitle.textContent = `Customer ${idDisplay}`;
    }
    if (DOM.modalCustomerSubtitle) {
      DOM.modalCustomerSubtitle.textContent = `Tenure: ${customer.tenure ?? 0} months • Contract: ${customer.Contract ?? '--'}`;
    }
    if (DOM.modalChurnBadge) {
      DOM.modalChurnBadge.className = `status-badge ${isChurned ? 'churned' : 'retained'}`;
      DOM.modalChurnBadge.innerHTML = `<span class="status-pulse-dot"></span>${isChurned ? 'Churned Customer' : 'Retained Customer'}`;
    }

    if (DOM.modalCustomerContent) {
      DOM.modalCustomerContent.innerHTML = `
        <div class="modal-grid">
          <!-- Card 1: Identity & Demographics -->
          <div class="modal-card">
            <h5>
              <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"></path>
                <circle cx="12" cy="7" r="4"></circle>
              </svg>
              Demographics
            </h5>
            <div class="modal-attr-list">
              <div class="modal-attr-row"><span class="attr-label">Gender</span><span class="attr-value">${customer.gender ?? '--'}</span></div>
              <div class="modal-attr-row"><span class="attr-label">Senior Citizen</span><span class="attr-value">${renderBoolBadge(customer.SeniorCitizen)}</span></div>
              <div class="modal-attr-row"><span class="attr-label">Partner</span><span class="attr-value">${renderBoolBadge(customer.Partner)}</span></div>
              <div class="modal-attr-row"><span class="attr-label">Dependents</span><span class="attr-value">${renderBoolBadge(customer.Dependents)}</span></div>
              <div class="modal-attr-row"><span class="attr-label">Tenure</span><span class="attr-value">${customer.tenure ?? 0} months</span></div>
            </div>
          </div>

          <!-- Card 2: Connectivity Services -->
          <div class="modal-card">
            <h5>
              <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72 12.84 12.84 0 0 0 .7 2.81 2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45 12.84 12.84 0 0 0 2.81.7A2 2 0 0 1 22 16.92z"></path>
              </svg>
              Connectivity Services
            </h5>
            <div class="modal-attr-list">
              <div class="modal-attr-row"><span class="attr-label">Phone Service</span><span class="attr-value">${renderBoolBadge(customer.PhoneService)}</span></div>
              <div class="modal-attr-row"><span class="attr-label">Multiple Lines</span><span class="attr-value">${renderBoolBadge(customer.MultipleLines)}</span></div>
              <div class="modal-attr-row"><span class="attr-label">Internet Service</span><span class="attr-value">${renderInternetBadge(customer.InternetService)}</span></div>
              <div class="modal-attr-row"><span class="attr-label">Contract</span><span class="attr-value">${renderContractBadge(customer.Contract)}</span></div>
            </div>
          </div>

          <!-- Card 3: Security & Streaming -->
          <div class="modal-card">
            <h5>
              <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <rect x="3" y="11" width="18" height="11" rx="2" ry="2"></rect>
                <path d="M7 11V7a5 5 0 0 1 10 0v4"></path>
              </svg>
              Security & Streaming
            </h5>
            <div class="modal-attr-list">
              <div class="modal-attr-row"><span class="attr-label">Online Security</span><span class="attr-value">${renderBoolBadge(customer.OnlineSecurity)}</span></div>
              <div class="modal-attr-row"><span class="attr-label">Online Backup</span><span class="attr-value">${renderBoolBadge(customer.OnlineBackup)}</span></div>
              <div class="modal-attr-row"><span class="attr-label">Device Protection</span><span class="attr-value">${renderBoolBadge(customer.DeviceProtection)}</span></div>
              <div class="modal-attr-row"><span class="attr-label">Tech Support</span><span class="attr-value">${renderBoolBadge(customer.TechSupport)}</span></div>
              <div class="modal-attr-row"><span class="attr-label">Streaming TV</span><span class="attr-value">${renderBoolBadge(customer.StreamingTV)}</span></div>
              <div class="modal-attr-row"><span class="attr-label">Streaming Movies</span><span class="attr-value">${renderBoolBadge(customer.StreamingMovies)}</span></div>
            </div>
          </div>

          <!-- Card 4: Billing & Financials -->
          <div class="modal-card">
            <h5>
              <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <line x1="12" y1="1" x2="12" y2="23"></line>
                <path d="M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"></path>
              </svg>
              Billing & Charges
            </h5>
            <div class="modal-attr-list">
              <div class="modal-attr-row"><span class="attr-label">Monthly Charges</span><span class="attr-value" style="font-size:1rem; color:var(--primary-700); font-weight:700;">${formatCurrency(customer.MonthlyCharges)}</span></div>
              <div class="modal-attr-row"><span class="attr-label">Total Charges</span><span class="attr-value">${formatCurrency(customer.TotalCharges)}</span></div>
              <div class="modal-attr-row"><span class="attr-label">Paperless Billing</span><span class="attr-value">${renderBoolBadge(customer.PaperlessBilling)}</span></div>
              <div class="modal-attr-row"><span class="attr-label">Payment Method</span><span class="attr-value">${customer.PaymentMethod ?? '--'}</span></div>
            </div>
          </div>
        </div>
      `;
    }

    DOM.modalBackdrop.style.display = 'flex';
    DOM.modalBackdrop.setAttribute('aria-hidden', 'false');
    document.body.style.overflow = 'hidden';
  }

  function closeCustomerModal() {
    if (DOM.modalBackdrop) {
      DOM.modalBackdrop.style.display = 'none';
      DOM.modalBackdrop.setAttribute('aria-hidden', 'true');
    }
    document.body.style.overflow = '';
    state.customers.selectedCustomer = null;
  }

  async function fetchCustomerData() {
    state.customers.isLoading = true;
    renderCustomerTableLoading();

    try {
      // Backend expects offset (0-based), convert from 1-based page number
      const offset = (state.customers.page - 1) * state.customers.limit;
      const queryParams = new URLSearchParams({
        offset: offset,
        limit: state.customers.limit,
      });

      if (state.customers.search.trim()) {
        queryParams.append('search', state.customers.search.trim());
      }

      if (state.customers.churn !== 'all') {
        queryParams.append('churn', state.customers.churn);
      }

      if (state.customers.contract && state.customers.contract !== 'all') {
        queryParams.append('contract', state.customers.contract);
      }

      const response = await fetch(`${API_ENDPOINTS.CUSTOMERS}?${queryParams.toString()}`);
      if (!response.ok) {
        throw new Error(`HTTP ${response.status}: ${response.statusText}`);
      }

      const data = await response.json();
      setBackendStatus(true, 'Backend Connected');

      let items = [];
      let total = 0;

      if (Array.isArray(data)) {
        items = data;
        total = data.length;
      } else if (typeof data === 'object') {
        items = data.rows ?? data.customers ?? data.items ?? data.data ?? [];
        total = data.total ?? data.count ?? items.length;
      }

      state.customers.data = items;
      state.customers.total = total;

      renderCustomerTable(items, total);
      updatePaginationControls(total);
    } catch (error) {
      console.warn('Customer records fetch error:', error);
      renderCustomerTableError(error.message);
    } finally {
      state.customers.isLoading = false;
    }
  }

  function renderCustomerTableLoading() {
    if (!DOM.tableBody) return;
    DOM.tableBody.innerHTML = Array(state.customers.limit)
      .fill(0)
      .map(
        () => `
        <tr>
          <td class="sticky-col-left"><div class="skeleton" style="width: 80px; height: 18px;"></div></td>
          <td><div class="skeleton" style="width: 50px; height: 18px;"></div></td>
          <td><div class="skeleton" style="width: 35px; height: 18px;"></div></td>
          <td><div class="skeleton" style="width: 35px; height: 18px;"></div></td>
          <td><div class="skeleton" style="width: 35px; height: 18px;"></div></td>
          <td><div class="skeleton" style="width: 45px; height: 18px;"></div></td>
          <td><div class="skeleton" style="width: 35px; height: 18px;"></div></td>
          <td><div class="skeleton" style="width: 45px; height: 18px;"></div></td>
          <td><div class="skeleton" style="width: 65px; height: 18px;"></div></td>
          <td><div class="skeleton" style="width: 35px; height: 18px;"></div></td>
          <td><div class="skeleton" style="width: 35px; height: 18px;"></div></td>
          <td><div class="skeleton" style="width: 35px; height: 18px;"></div></td>
          <td><div class="skeleton" style="width: 35px; height: 18px;"></div></td>
          <td><div class="skeleton" style="width: 35px; height: 18px;"></div></td>
          <td><div class="skeleton" style="width: 35px; height: 18px;"></div></td>
          <td><div class="skeleton" style="width: 85px; height: 18px;"></div></td>
          <td><div class="skeleton" style="width: 35px; height: 18px;"></div></td>
          <td><div class="skeleton" style="width: 100px; height: 18px;"></div></td>
          <td><div class="skeleton" style="width: 60px; height: 18px;"></div></td>
          <td><div class="skeleton" style="width: 70px; height: 18px;"></div></td>
          <td><div class="skeleton" style="width: 75px; height: 22px; border-radius: 999px;"></div></td>
          <td class="sticky-col-right"><div class="skeleton" style="width: 90px; height: 26px;"></div></td>
        </tr>
      `
      )
      .join('');
    if (DOM.tableInfo) DOM.tableInfo.textContent = 'Loading records...';
  }

  function renderCustomerTable(items, total) {
    if (!DOM.tableBody) return;

    if (items.length === 0) {
      DOM.tableBody.innerHTML = `
        <tr>
          <td colspan="22">
            <div class="table-empty-state">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
                <circle cx="11" cy="11" r="8"></circle>
                <line x1="21" y1="21" x2="16.65" y2="16.65"></line>
              </svg>
              <h4>No Customer Records Found</h4>
              <p>Try adjusting your search keyword, contract type, or churn status criteria.</p>
            </div>
          </td>
        </tr>
      `;
      if (DOM.tableInfo) DOM.tableInfo.textContent = 'Showing 0 records';
      return;
    }

    const startRecord = (state.customers.page - 1) * state.customers.limit + 1;
    const endRecord = Math.min(startRecord + items.length - 1, total);

    DOM.tableBody.innerHTML = items
      .map((customer, index) => {
        const idDisplay = customer.customerID ?? customer.id ?? customer.row ?? customer.Unnamed_0 ?? `#${startRecord + index}`;
        const isChurned =
          customer.Churn === 1 ||
          customer.Churn === '1' ||
          customer.Churn === 'Yes' ||
          customer.churn === 1 ||
          customer.churn === 'Yes';

        const tenure = customer.tenure ?? 0;
        const monthly = formatCurrency(customer.MonthlyCharges);
        const totalCharges = formatCurrency(customer.TotalCharges);

        return `
        <tr data-customer-index="${index}">
          <!-- 1. Customer ID (Sticky Left) -->
          <td class="sticky-col-left">
            <span class="customer-id-pill" title="Customer Identifier">${idDisplay}</span>
          </td>

          <!-- 2. Gender -->
          <td>${renderGenderBadge(customer.gender)}</td>

          <!-- 3. Senior Citizen -->
          <td>${renderBoolBadge(customer.SeniorCitizen)}</td>

          <!-- 4. Partner -->
          <td>${renderBoolBadge(customer.Partner)}</td>

          <!-- 5. Dependents -->
          <td>${renderBoolBadge(customer.Dependents)}</td>

          <!-- 6. Tenure -->
          <td>
            <strong>${tenure}</strong>
            <span style="font-size:0.75rem; color:var(--slate-500);">mo${tenure !== 1 ? 's' : ''}</span>
          </td>

          <!-- 7. Phone Service -->
          <td>${renderBoolBadge(customer.PhoneService)}</td>

          <!-- 8. Multiple Lines -->
          <td>${renderBoolBadge(customer.MultipleLines)}</td>

          <!-- 9. Internet Service -->
          <td>${renderInternetBadge(customer.InternetService)}</td>

          <!-- 10. Online Security -->
          <td>${renderBoolBadge(customer.OnlineSecurity)}</td>

          <!-- 11. Online Backup -->
          <td>${renderBoolBadge(customer.OnlineBackup)}</td>

          <!-- 12. Device Protection -->
          <td>${renderBoolBadge(customer.DeviceProtection)}</td>

          <!-- 13. Tech Support -->
          <td>${renderBoolBadge(customer.TechSupport)}</td>

          <!-- 14. Streaming TV -->
          <td>${renderBoolBadge(customer.StreamingTV)}</td>

          <!-- 15. Streaming Movies -->
          <td>${renderBoolBadge(customer.StreamingMovies)}</td>

          <!-- 16. Contract -->
          <td>${renderContractBadge(customer.Contract)}</td>

          <!-- 17. Paperless Billing -->
          <td>${renderBoolBadge(customer.PaperlessBilling)}</td>

          <!-- 18. Payment Method -->
          <td>${renderPaymentBadge(customer.PaymentMethod)}</td>

          <!-- 19. Monthly Charges -->
          <td><strong style="color:var(--slate-900); font-weight:700;">${monthly}</strong></td>

          <!-- 20. Total Charges -->
          <td><span style="font-weight:600; color:var(--slate-700);">${totalCharges}</span></td>

          <!-- 21. Churn Status -->
          <td>
            <span class="status-badge ${isChurned ? 'churned' : 'retained'}">
              <span class="status-pulse-dot"></span>
              ${isChurned ? 'Churned' : 'Retained'}
            </span>
          </td>

          <!-- 22. Actions (Sticky Right) -->
          <td class="sticky-col-right text-center">
            <div class="row-actions-group">
              <button type="button" class="btn-use-row" data-row-idx="${index}" title="Load full profile into predictor and evaluate churn risk">
                <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
                  <polygon points="5 3 19 12 5 21 5 3"></polygon>
                </svg>
                Test
              </button>
              <button type="button" class="btn-view-row" data-row-idx="${index}" title="Inspect all 21 customer attributes in full detail">
                <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                  <path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"></path>
                  <circle cx="12" cy="12" r="3"></circle>
                </svg>
                View
              </button>
            </div>
          </td>
        </tr>
      `;
      })
      .join('');

    // Attach click handlers to row action buttons
    DOM.tableBody.querySelectorAll('.btn-use-row').forEach(button => {
      button.addEventListener('click', () => {
        const idx = Number(button.getAttribute('data-row-idx'));
        if (items[idx]) {
          populateFormWithCustomer(items[idx], true);
        }
      });
    });

    DOM.tableBody.querySelectorAll('.btn-view-row').forEach(button => {
      button.addEventListener('click', () => {
        const idx = Number(button.getAttribute('data-row-idx'));
        if (items[idx]) {
          openCustomerModal(items[idx]);
        }
      });
    });

    if (DOM.tableInfo) {
      DOM.tableInfo.textContent = `Showing ${startRecord}–${endRecord} of ${formatNumber(total)} customers • All 21 features displayed`;
    }

    updateTableScrollButtons();
  }

  function renderCustomerTableError(errorMessage) {
    if (!DOM.tableBody) return;
    DOM.tableBody.innerHTML = `
      <tr>
        <td colspan="22">
          <div class="table-empty-state">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" style="color:var(--rose-400);">
              <circle cx="12" cy="12" r="10"></circle>
              <line x1="12" y1="8" x2="12" y2="12"></line>
              <line x1="12" y1="16" x2="12.01" y2="16"></line>
            </svg>
            <h4>Error Loading Customer Records</h4>
            <p style="margin-bottom:1rem;">${errorMessage}</p>
            <button type="button" class="btn-refresh" id="btn-retry-customers" style="margin:0 auto;">
              Retry Connection
            </button>
          </div>
        </td>
      </tr>
    `;

    const retryBtn = document.getElementById('btn-retry-customers');
    if (retryBtn) {
      retryBtn.addEventListener('click', fetchCustomerData);
    }
    if (DOM.tableInfo) DOM.tableInfo.textContent = 'Connection error';
  }

  function updatePaginationControls(total) {
    const totalPages = Math.max(1, Math.ceil(total / state.customers.limit));
    const currentPage = state.customers.page;

    if (DOM.pageIndicator) {
      DOM.pageIndicator.textContent = `${currentPage} / ${totalPages}`;
    }

    if (DOM.btnPrevPage) {
      DOM.btnPrevPage.disabled = currentPage <= 1;
    }
    if (DOM.btnNextPage) {
      DOM.btnNextPage.disabled = currentPage >= totalPages;
    }
  }

  // =========================================================================
  // 6. Prediction Form Validation & Submission
  // =========================================================================

  function populateFormWithCustomer(record, autoRun = true) {
    if (!record) return;

    // 1. Fill binary fields
    BINARY_FIELDS.forEach(field => {
      const select = document.getElementById(field);
      if (select && record[field] !== undefined) {
        const val = record[field];
        if (val === 1 || val === '1' || val === 'Yes' || val === true) {
          select.value = 'Yes';
        } else if (
          val === 0 ||
          val === '0' ||
          val === 'No' ||
          val === false ||
          String(val).toLowerCase().includes('no')
        ) {
          select.value = 'No';
        }
      }
    });

    // 2. Fill categorical fields
    CATEGORICAL_FIELDS.forEach(field => {
      const select = document.getElementById(field);
      if (select && record[field] !== undefined) {
        let val = record[field];
        if (field === 'InternetService' && (val === '0' || val === 0 || val === 'No' || val === 'None')) {
          val = 'No';
        }
        select.value = val;
      }
    });

    // 3. Fill numeric fields
    NUMERIC_FIELDS.forEach(field => {
      const input = document.getElementById(field);
      if (input && record[field] !== undefined) {
        input.value = record[field] !== null ? record[field] : 0;
      }
    });

    clearFormValidation();
    if (DOM.btnLoadHighRisk) DOM.btnLoadHighRisk.classList.remove('active');
    if (DOM.btnLoadLowRisk) DOM.btnLoadLowRisk.classList.remove('active');

    // Pulse highlight the form card for feedback
    if (DOM.predictCard) {
      DOM.predictCard.classList.remove('form-pulse-highlight');
      void DOM.predictCard.offsetWidth; // trigger DOM reflow
      DOM.predictCard.classList.add('form-pulse-highlight');
      setTimeout(() => {
        if (DOM.predictCard) DOM.predictCard.classList.remove('form-pulse-highlight');
      }, 1600);
    }

    const customerId = record.customerID || record.id || 'Customer Profile';
    showToast(`Loaded ${customerId} into Prediction Form!`, 'success');

    // Smooth scroll to prediction form
    const predictSection = document.getElementById('predict');
    if (predictSection) {
      predictSection.scrollIntoView({ behavior: 'smooth' });
    }

    // Auto run prediction if requested
    if (autoRun) {
      setTimeout(() => {
        handlePredictionSubmit(new Event('submit'));
      }, 250);
    }
  }

  function applyPreset(presetData, buttonEl) {
    if (DOM.btnLoadHighRisk) DOM.btnLoadHighRisk.classList.remove('active');
    if (DOM.btnLoadLowRisk) DOM.btnLoadLowRisk.classList.remove('active');
    if (buttonEl) buttonEl.classList.add('active');

    Object.entries(presetData).forEach(([field, value]) => {
      const element = document.getElementById(field);
      if (element) {
        element.value = value;
      }
    });
    clearFormValidation();

    if (DOM.predictCard) {
      DOM.predictCard.classList.remove('form-pulse-highlight');
      void DOM.predictCard.offsetWidth;
      DOM.predictCard.classList.add('form-pulse-highlight');
      setTimeout(() => {
        if (DOM.predictCard) DOM.predictCard.classList.remove('form-pulse-highlight');
      }, 1600);
    }

    showToast('Loaded preset profile & evaluating churn probability...', 'info');

    setTimeout(() => {
      handlePredictionSubmit(new Event('submit'));
    }, 150);
  }

  function clearForm() {
    if (DOM.predictionForm) {
      DOM.predictionForm.reset();
      // Ensure select placeholders are selected
      const selects = DOM.predictionForm.querySelectorAll('select');
      selects.forEach(s => (s.selectedIndex = 0));
    }
    if (DOM.btnLoadHighRisk) DOM.btnLoadHighRisk.classList.remove('active');
    if (DOM.btnLoadLowRisk) DOM.btnLoadLowRisk.classList.remove('active');
    clearFormValidation();
    resetResultCard();
  }

  function clearFormValidation() {
    if (DOM.formValidationAlert) {
      DOM.formValidationAlert.style.display = 'none';
      DOM.formValidationAlert.innerHTML = '';
    }
    if (DOM.predictionForm) {
      const invalidInputs = DOM.predictionForm.querySelectorAll('.invalid');
      invalidInputs.forEach(el => el.classList.remove('invalid'));
    }
  }

  function validatePredictionForm() {
    clearFormValidation();
    const missingFields = [];

    // Validate Binary Fields
    BINARY_FIELDS.forEach(field => {
      const select = document.getElementById(field);
      if (!select || !select.value) {
        if (select) select.classList.add('invalid');
        const label = select?.closest('.form-group')?.querySelector('.form-label')?.textContent?.replace('*', '').trim() || field;
        missingFields.push(label);
      }
    });

    // Validate Categorical Fields
    CATEGORICAL_FIELDS.forEach(field => {
      const select = document.getElementById(field);
      if (!select || !select.value) {
        if (select) select.classList.add('invalid');
        const label = select?.closest('.form-group')?.querySelector('.form-label')?.textContent?.replace('*', '').trim() || field;
        missingFields.push(label);
      }
    });

    // Validate Numeric Fields
    NUMERIC_FIELDS.forEach(field => {
      const input = document.getElementById(field);
      if (!input || input.value === '' || isNaN(Number(input.value)) || Number(input.value) < 0) {
        if (input) input.classList.add('invalid');
        const label = input?.closest('.form-group')?.querySelector('.form-label')?.textContent?.replace('*', '').trim() || field;
        missingFields.push(label);
      }
    });

    if (missingFields.length > 0) {
      if (DOM.formValidationAlert) {
        DOM.formValidationAlert.style.display = 'block';
        showAlert(
          `Please provide valid values for all required fields: <strong>${missingFields.slice(0, 3).join(', ')}${missingFields.length > 3 ? ` and ${missingFields.length - 3} more` : ''}</strong>.`,
          'error',
          DOM.formValidationAlert
        );
      }
      return false;
    }

    return true;
  }

  function collectPredictionData() {
    const formData = new FormData(DOM.predictionForm);
    const customerData = {};

    formData.forEach((value, key) => {
      customerData[key] = value;
    });

    // 1. Convert Binary Fields: 'Yes' -> 1, 'No' -> 0
    BINARY_FIELDS.forEach(field => {
      if (customerData[field] === 'Yes') {
        customerData[field] = 1;
      } else if (customerData[field] === 'No') {
        customerData[field] = 0;
      }
    });

    // 2. Convert Numeric Fields
    customerData.tenure = Number(customerData.tenure);
    customerData.MonthlyCharges = Number(customerData.MonthlyCharges);
    customerData.TotalCharges = Number(customerData.TotalCharges);

    // 3. Keep InternetService, Contract, PaymentMethod as exact strings

    return customerData;
  }

  async function handlePredictionSubmit(event) {
    event.preventDefault();

    if (!validatePredictionForm()) {
      return;
    }

    const payload = collectPredictionData();

    // Disable button & show spinner
    setPredictButtonLoading(true);

    try {
      const response = await fetch(API_ENDPOINTS.PREDICT, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(payload),
      });

      if (!response.ok) {
        let errMessage = `HTTP ${response.status}: ${response.statusText}`;
        try {
          const errData = await response.json();
          if (errData.detail) {
            errMessage = Array.isArray(errData.detail)
              ? errData.detail.map(d => d.msg || JSON.stringify(d)).join('; ')
              : errData.detail;
          }
        } catch (_) {}
        throw new Error(errMessage);
      }

      const result = await response.json();
      setBackendStatus(true, 'Backend Connected');
      displayPredictionResult(result);
    } catch (error) {
      console.error('Prediction request failure:', error);
      if (DOM.formValidationAlert) {
        DOM.formValidationAlert.style.display = 'block';
        showAlert(
          `Prediction request failed: ${error.message}. Check backend logs.`,
          'error',
          DOM.formValidationAlert
        );
      }
    } finally {
      setPredictButtonLoading(false);
    }
  }

  function setPredictButtonLoading(isLoading) {
    if (!DOM.btnPredictSubmit) return;
    DOM.btnPredictSubmit.disabled = isLoading;
    if (DOM.btnPredictSpinner) DOM.btnPredictSpinner.style.display = isLoading ? 'inline-block' : 'none';
    if (DOM.btnPredictText) DOM.btnPredictText.textContent = isLoading ? 'Predicting...' : 'Predict Churn Risk';
  }

  // =========================================================================
  // 7. Prediction Result Display
  // =========================================================================

  function displayPredictionResult(result) {
    if (!DOM.resultCard || !DOM.resultStandbyView || !DOM.resultActiveView) return;

    // Check predicted churn key from backend
    const rawChurn =
      result.predicted_churn ??
      result.churn_prediction ??
      result.prediction ??
      result.churn;

    // Check churn probability
    const rawProb =
      result.churn_probability ??
      result.probability ??
      result.churn_prob ??
      result.confidence ??
      0;

    let probNumber = Number(rawProb);
    // If backend returns probability as decimal [0, 1], convert to percentage without multiplying twice
    let probPercentage = probNumber <= 1 ? (probNumber * 100).toFixed(1) : probNumber.toFixed(1);
    const numericPct = parseFloat(probPercentage);

    const churnStr = String(rawChurn ?? '').trim().toLowerCase();
    const isChurn =
      rawChurn === 1 ||
      rawChurn === '1' ||
      rawChurn === true ||
      churnStr === 'yes' ||
      churnStr === 'churn' ||
      (rawChurn === undefined && numericPct >= 50);

    // Update Result View Visibility
    DOM.resultStandbyView.style.display = 'none';
    DOM.resultActiveView.style.display = 'flex';

    // Update Banner Appearance
    DOM.resultCard.className = `result-card ${isChurn ? 'status-churn' : 'status-nochurn'}`;
    DOM.resultOutcomeBanner.className = `result-banner ${isChurn ? 'churn' : 'nochurn'}`;

    if (DOM.resultIconContainer) {
      DOM.resultIconContainer.innerHTML = isChurn
        ? `<svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
            <line x1="18" y1="6" x2="6" y2="18"></line>
            <line x1="6" y1="6" x2="18" y2="18"></line>
          </svg>`
        : `<svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
            <polyline points="20 6 9 17 4 12"></polyline>
          </svg>`;
    }

    if (DOM.resultPredictionTitle) {
      DOM.resultPredictionTitle.textContent = isChurn ? 'High Churn Risk' : 'Low Churn Risk';
    }

    if (DOM.resultPredictionSubtitle) {
      DOM.resultPredictionSubtitle.textContent = isChurn
        ? 'Customer is likely to cancel their subscription service'
        : 'Customer is likely to remain retained and active';
    }

    if (DOM.resultProbabilityText) {
      DOM.resultProbabilityText.textContent = `${probPercentage}%`;
    }

    // Progress Bar Fill
    if (DOM.resultProgressFill) {
      DOM.resultProgressFill.style.width = `${Math.min(100, Math.max(0, numericPct))}%`;
      if (numericPct >= 50) {
        DOM.resultProgressFill.className = 'progress-bar-fill high';
      } else if (numericPct >= 30) {
        DOM.resultProgressFill.className = 'progress-bar-fill medium';
      } else {
        DOM.resultProgressFill.className = 'progress-bar-fill low';
      }
    }

    // Contextual Note
    if (DOM.resultExplanationText) {
      DOM.resultExplanationText.textContent = isChurn
        ? `Model inference estimates a ${probPercentage}% churn risk. Proactive retention measures such as contract incentives, fee adjustments, or dedicated account support are strongly recommended.`
        : `Model inference estimates a low churn likelihood (${probPercentage}% probability). This customer profile aligns with sustained long-term retention.`;
    }

    if (DOM.resultTimestampBadge) {
      const now = new Date();
      DOM.resultTimestampBadge.textContent = `Calculated at ${now.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit', second: '2-digit' })}`;
      DOM.resultTimestampBadge.className = isChurn ? 'kpi-badge badge-danger' : 'kpi-badge badge-success';
    }
  }

  function resetResultCard() {
    if (!DOM.resultCard || !DOM.resultStandbyView || !DOM.resultActiveView) return;
    DOM.resultCard.className = 'result-card';
    DOM.resultStandbyView.style.display = 'flex';
    DOM.resultActiveView.style.display = 'none';
    if (DOM.resultTimestampBadge) {
      DOM.resultTimestampBadge.textContent = 'Model Ready';
      DOM.resultTimestampBadge.className = 'kpi-badge badge-neutral';
    }
  }

  // =========================================================================
  // 8. Event Listeners & Navigation Handling
  // =========================================================================

  function updateTableScrollButtons() {
    if (!DOM.tableContainer) return;
    const { scrollLeft, scrollWidth, clientWidth } = DOM.tableContainer;
    if (DOM.btnScrollLeft) {
      DOM.btnScrollLeft.disabled = scrollLeft <= 5;
    }
    if (DOM.btnScrollRight) {
      DOM.btnScrollRight.disabled = scrollLeft + clientWidth >= scrollWidth - 5;
    }
  }

  function setupEventListeners() {
    // Prediction Form Submission
    if (DOM.predictionForm) {
      DOM.predictionForm.addEventListener('submit', handlePredictionSubmit);

      // Clear .invalid class on change or input
      DOM.predictionForm.querySelectorAll('input, select').forEach(element => {
        element.addEventListener('input', () => element.classList.remove('invalid'));
        element.addEventListener('change', () => element.classList.remove('invalid'));
      });
    }

    // Preset Buttons
    if (DOM.btnLoadHighRisk) {
      DOM.btnLoadHighRisk.addEventListener('click', () => applyPreset(PRESET_HIGH_RISK, DOM.btnLoadHighRisk));
    }
    if (DOM.btnLoadLowRisk) {
      DOM.btnLoadLowRisk.addEventListener('click', () => applyPreset(PRESET_LOYAL, DOM.btnLoadLowRisk));
    }
    if (DOM.btnClearForm) {
      DOM.btnClearForm.addEventListener('click', clearForm);
    }
    if (DOM.btnPredictAnother) {
      DOM.btnPredictAnother.addEventListener('click', () => {
        clearForm();
        const tenureInput = document.getElementById('tenure');
        if (tenureInput) {
          tenureInput.scrollIntoView({ behavior: 'smooth', block: 'center' });
          tenureInput.focus();
        }
      });
    }

    // Customer Explorer Filters & Search
    let searchDebounceTimer = null;
    if (DOM.searchInput) {
      DOM.searchInput.addEventListener('input', e => {
        const val = e.target.value;
        if (DOM.btnClearSearch) {
          DOM.btnClearSearch.style.display = val.length > 0 ? 'flex' : 'none';
        }
        clearTimeout(searchDebounceTimer);
        searchDebounceTimer = setTimeout(() => {
          state.customers.search = val;
          state.customers.page = 1;
          fetchCustomerData();
        }, 300);
      });
    }

    if (DOM.btnClearSearch) {
      DOM.btnClearSearch.addEventListener('click', () => {
        if (DOM.searchInput) {
          DOM.searchInput.value = '';
          DOM.btnClearSearch.style.display = 'none';
        }
        state.customers.search = '';
        state.customers.page = 1;
        fetchCustomerData();
      });
    }

    if (DOM.churnFilter) {
      DOM.churnFilter.addEventListener('change', e => {
        state.customers.churn = e.target.value;
        state.customers.page = 1;
        fetchCustomerData();
      });
    }

    if (DOM.contractFilter) {
      DOM.contractFilter.addEventListener('change', e => {
        state.customers.contract = e.target.value;
        state.customers.page = 1;
        fetchCustomerData();
      });
    }

    if (DOM.pageSizeSelect) {
      DOM.pageSizeSelect.addEventListener('change', e => {
        state.customers.limit = Number(e.target.value);
        state.customers.page = 1;
        fetchCustomerData();
      });
    }

    // Horizontal Scroll Buttons
    if (DOM.btnScrollLeft && DOM.tableContainer) {
      DOM.btnScrollLeft.addEventListener('click', () => {
        DOM.tableContainer.scrollBy({ left: -320, behavior: 'smooth' });
      });
    }

    if (DOM.btnScrollRight && DOM.tableContainer) {
      DOM.btnScrollRight.addEventListener('click', () => {
        DOM.tableContainer.scrollBy({ left: 320, behavior: 'smooth' });
      });
    }

    if (DOM.tableContainer) {
      DOM.tableContainer.addEventListener('scroll', updateTableScrollButtons);
    }

    // Export CSV
    if (DOM.btnExportCsv) {
      DOM.btnExportCsv.addEventListener('click', exportCustomersToCsv);
    }

    if (DOM.btnRefreshTable) {
      DOM.btnRefreshTable.addEventListener('click', () => {
        fetchCustomerData();
        showToast('Refreshed customer records from database', 'info');
      });
    }

    // Modal Events
    if (DOM.btnCloseModal) {
      DOM.btnCloseModal.addEventListener('click', closeCustomerModal);
    }
    if (DOM.btnModalDismiss) {
      DOM.btnModalDismiss.addEventListener('click', closeCustomerModal);
    }
    if (DOM.modalBackdrop) {
      DOM.modalBackdrop.addEventListener('click', e => {
        if (e.target === DOM.modalBackdrop) {
          closeCustomerModal();
        }
      });
    }
    document.addEventListener('keydown', e => {
      if (e.key === 'Escape' && DOM.modalBackdrop && DOM.modalBackdrop.style.display === 'flex') {
        closeCustomerModal();
      }
    });

    if (DOM.btnModalPredict) {
      DOM.btnModalPredict.addEventListener('click', () => {
        if (state.customers.selectedCustomer) {
          const cust = state.customers.selectedCustomer;
          closeCustomerModal();
          populateFormWithCustomer(cust, true);
        }
      });
    }

    // Pagination
    if (DOM.btnPrevPage) {
      DOM.btnPrevPage.addEventListener('click', () => {
        if (state.customers.page > 1) {
          state.customers.page -= 1;
          fetchCustomerData();
        }
      });
    }

    if (DOM.btnNextPage) {
      DOM.btnNextPage.addEventListener('click', () => {
        const totalPages = Math.ceil(state.customers.total / state.customers.limit);
        if (state.customers.page < totalPages) {
          state.customers.page += 1;
          fetchCustomerData();
        }
      });
    }

    // Navigation links smooth scroll & click handler
    DOM.navLinks.forEach(link => {
      link.addEventListener('click', e => {
        const targetId = link.getAttribute('href')?.replace('#', '');
        const targetEl = document.getElementById(targetId);
        if (targetEl) {
          e.preventDefault();
          targetEl.scrollIntoView({ behavior: 'smooth' });
          DOM.navLinks.forEach(l => l.classList.remove('active'));
          link.classList.add('active');
        }
      });
    });

    // Smooth navigation active states on scroll
    window.addEventListener('scroll', handleScrollSpy);
  }

  function handleScrollSpy() {
    const sections = ['overview', 'analytics', 'customers', 'predict'];

    // Check if scrolled near the bottom of page
    const isAtBottom = window.innerHeight + window.scrollY >= document.documentElement.scrollHeight - 80;
    if (isAtBottom) {
      DOM.navLinks.forEach(l => l.classList.remove('active'));
      const lastLink = document.querySelector('.nav-link[href="#predict"]');
      if (lastLink) lastLink.classList.add('active');
      return;
    }

    const scrollPos = window.scrollY + 140;
    for (let i = sections.length - 1; i >= 0; i--) {
      const secId = sections[i];
      const sectionEl = document.getElementById(secId);
      const link = document.querySelector(`.nav-link[href="#${secId}"]`);
      if (sectionEl && link) {
        if (scrollPos >= sectionEl.offsetTop) {
          DOM.navLinks.forEach(l => l.classList.remove('active'));
          link.classList.add('active');
          break;
        }
      }
    }
  }

  // =========================================================================
  // 9. Application Bootstrap
  // =========================================================================

  function initApp() {
    setupEventListeners();
    fetchDashboardData();
    fetchCustomerData();
  }

  // Run on DOM ready
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initApp);
  } else {
    initApp();
  }
})();
