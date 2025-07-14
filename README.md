# 🚗 Car Sales Dashboard

[![Python 3.12+](https://img.shields.io/badge/python-3.12+-blue.svg)](https://www.python.org/downloads/)
[![Code Quality](https://img.shields.io/badge/code%20quality-87.1%2F100-brightgreen.svg)](docs/testing/fix6_code_quality.md)
[![Tests](https://img.shields.io/badge/tests-passing-brightgreen.svg)](docs/testing/fix6_test_report.md)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

An interactive machine learning dashboard for car sales forecasting with real-time exogenous variable manipulation. Built with **Reflex** (Python full-stack framework) and **SARIMAX** time series models.

## ✨ Features

- 🎛️ **Interactive Controls**: Real-time adjustment of gas prices, CPI, search volume
- 📊 **ML Forecasting**: SARIMAX time series models with exogenous variables
- 🗺️ **Geographic Analysis**: Regional and state-level sales breakdowns
- 🚗 **Vehicle Insights**: Category, make, model filtering and analysis
- ⚡ **Performance Optimized**: Caching, batch processing, and responsive design
- 🧪 **Comprehensive Testing**: 87.1/100 code quality score with full test coverage
- 🐳 **Production Ready**: Docker containerization and CI/CD pipeline

## 🚀 Quick Start

### Option 1: Docker (Recommended)
```bash
# Clone the repository
git clone https://github.com/kipmadden/car-sales-dashboard.git
cd car-sales-dashboard

# Run with Docker
docker-compose up --build
```

### Option 2: Local Development
```bash
# Install dependencies
pip install -r requirements.txt

# Run the application
reflex run
```

Access the dashboard at `http://localhost:3000`

## 📖 Documentation

- 📋 **[Full Documentation](docs/)** - Comprehensive guides and reports
- 🏗️ **[Implementation Details](docs/implementation/)** - Technical architecture
- 🧪 **[Testing Reports](docs/testing/)** - Quality assurance and test results
- 🚀 **[CI/CD Documentation](docs/ci-cd/)** - Deployment and automation

## 🛠️ Technology Stack

- **Frontend**: Reflex (React-based UI with Python)
- **Backend**: Python, FastAPI
- **ML Models**: SARIMAX (statsmodels), scikit-learn
- **Data**: Pandas, NumPy
- **Visualization**: Plotly
- **Deployment**: Docker, Redis
- **Testing**: Pytest, comprehensive quality framework

## 🏗️ Project Architecture

```
car_sales_dashboard/
├── car_sales_dashboard/           # Main application package
│   ├── components/               # UI components (charts, controls, tables)
│   ├── models/                   # ML models and data processing
│   ├── pages/                    # Page layouts and routing
│   ├── utils/                    # Utilities (validation, performance, testing)
│   └── state.py                  # Application state management
├── docs/                         # 📖 Documentation
├── tests/                        # 🧪 Test suite
├── requirements/                 # 📦 Dependencies
└── docker-compose.yml           # 🐳 Container orchestration
```

## 🔧 Development

### Adding New Features

1. **New ML Models**: Extend `models/scenario_engine.py`
2. **New Visualizations**: Add charts in `components/charts.py`
3. **New Data Sources**: Modify `models/data.py`
4. **UI Components**: Create reusable components in `components/`

### Code Quality

- **Quality Score**: 87.1/100 (Grade B)
- **Test Coverage**: Comprehensive test suite with 100% pass rate
- **Performance**: Optimized caching and batch processing
- **Documentation**: Full API and implementation documentation

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Run tests (`pytest`)
4. Commit changes (`git commit -m 'Add amazing feature'`)
5. Push to branch (`git push origin feature/amazing-feature`)
6. Open a Pull Request

## 📞 Support

- 📖 **Documentation**: [docs/](docs/)
- 🐛 **Issues**: [GitHub Issues](https://github.com/kipmadden/car-sales-dashboard/issues)
- 💬 **Discussions**: [GitHub Discussions](https://github.com/kipmadden/car-sales-dashboard/discussions)

---

*Built with ❤️ using Python and Reflex*