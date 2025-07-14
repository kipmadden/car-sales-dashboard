# Code Quality Analysis Report

Generated: 2025-07-13 19:01:07

## Executive Summary

- **Overall Quality Score**: 87.1/100
- **Total Files Analyzed**: 35
- **Total Lines of Code**: 8,848
- **Functions**: 282
- **Classes**: 41
- **Average Complexity**: 1.6

**Quality Grade**: B (Good)

## Issues Summary

- **Line Length/Style**: 16 issues
- **Documentation**: 15 issues
- **Function Arguments**: 5 issues
- **High Complexity**: 2 issues

## File Analysis

### car_sales_dashboard\models\data.py

- **Lines**: 351 (Code: 232, Comments: 43)
- **Functions**: 4, **Classes**: 0
- **Complexity**: 1
- **Docstring Coverage**: 100.0%
- **Max Line Length**: 124
- **Issues** (3):
  - Long lines: 124 chars (max: 100)
  - Function 'generate_sample_data' has high complexity: 30
  - Large file: avg 88 lines per function/class

### car_sales_dashboard\components\charts.py

- **Lines**: 689 (Code: 531, Comments: 49)
- **Functions**: 11, **Classes**: 0
- **Complexity**: 3
- **Docstring Coverage**: 90.9%
- **Max Line Length**: 134
- **Issues** (2):
  - Long lines: 134 chars (max: 100)
  - Large file: avg 63 lines per function/class

### car_sales_dashboard\models\scenario_engine.py

- **Lines**: 204 (Code: 144, Comments: 18)
- **Functions**: 12, **Classes**: 4
- **Complexity**: 1
- **Docstring Coverage**: 56.2%
- **Max Line Length**: 95
- **Issues** (2):
  - Low docstring coverage: 56.2% (min: 80.0%)
  - Function 'forecast' has too many arguments: 7

### car_sales_dashboard\models\__init__.py

- **Lines**: 6 (Code: 2, Comments: 3)
- **Functions**: 0, **Classes**: 0
- **Complexity**: 1
- **Docstring Coverage**: 0.0%
- **Max Line Length**: 111
- **Issues** (2):
  - Long lines: 111 chars (max: 100)
  - Low docstring coverage: 0.0% (min: 80.0%)

### car_sales_dashboard\utils\code_quality_analyzer.py

- **Lines**: 580 (Code: 440, Comments: 36)
- **Functions**: 21, **Classes**: 4
- **Complexity**: 2
- **Docstring Coverage**: 92.0%
- **Max Line Length**: 141
- **Issues** (2):
  - Long lines: 141 chars (max: 100)
  - Function '_detect_issues' has too many arguments: 8

### car_sales_dashboard\utils\error_handler.py

- **Lines**: 331 (Code: 265, Comments: 16)
- **Functions**: 14, **Classes**: 2
- **Complexity**: 1
- **Docstring Coverage**: 75.0%
- **Max Line Length**: 129
- **Issues** (2):
  - Long lines: 129 chars (max: 100)
  - Low docstring coverage: 75.0% (min: 80.0%)

### car_sales_dashboard\utils\logging_config.py

- **Lines**: 235 (Code: 165, Comments: 16)
- **Functions**: 16, **Classes**: 2
- **Complexity**: 1
- **Docstring Coverage**: 72.2%
- **Max Line Length**: 111
- **Issues** (2):
  - Long lines: 111 chars (max: 100)
  - Low docstring coverage: 72.2% (min: 80.0%)

### car_sales_dashboard\utils\performance.py

- **Lines**: 407 (Code: 301, Comments: 18)
- **Functions**: 21, **Classes**: 3
- **Complexity**: 1
- **Docstring Coverage**: 83.3%
- **Max Line Length**: 106
- **Issues** (2):
  - Long lines: 106 chars (max: 100)
  - Function 'optimize_dtypes' has high complexity: 16

### car_sales_dashboard\utils\performance_testing.py

- **Lines**: 600 (Code: 440, Comments: 42)
- **Functions**: 24, **Classes**: 5
- **Complexity**: 5
- **Docstring Coverage**: 62.1%
- **Max Line Length**: 119
- **Issues** (2):
  - Long lines: 119 chars (max: 100)
  - Low docstring coverage: 62.1% (min: 80.0%)

### car_sales_dashboard\utils\testing_framework.py

- **Lines**: 626 (Code: 464, Comments: 45)
- **Functions**: 23, **Classes**: 5
- **Complexity**: 9
- **Docstring Coverage**: 71.4%
- **Max Line Length**: 127
- **Issues** (2):
  - Long lines: 127 chars (max: 100)
  - Low docstring coverage: 71.4% (min: 80.0%)

### car_sales_dashboard\utils\ui_components.py

- **Lines**: 517 (Code: 469, Comments: 7)
- **Functions**: 11, **Classes**: 6
- **Complexity**: 1
- **Docstring Coverage**: 100.0%
- **Max Line Length**: 96
- **Issues** (2):
  - Function 'create_accessible_slider' has too many arguments: 8
  - Function 'create_accessible_button' has too many arguments: 8

### conftest.py

- **Lines**: 315 (Code: 209, Comments: 38)
- **Functions**: 19, **Classes**: 0
- **Complexity**: 1
- **Docstring Coverage**: 100.0%
- **Max Line Length**: 110
- **Issues** (1):
  - Long lines: 110 chars (max: 100)

### quick_test_fix5.py

- **Lines**: 40 (Code: 27, Comments: 4)
- **Functions**: 0, **Classes**: 0
- **Complexity**: 2
- **Docstring Coverage**: 0.0%
- **Max Line Length**: 70
- **Issues** (1):
  - Low docstring coverage: 0.0% (min: 80.0%)

### rxconfig.py

- **Lines**: 41 (Code: 25, Comments: 10)
- **Functions**: 0, **Classes**: 0
- **Complexity**: 1
- **Docstring Coverage**: 0.0%
- **Max Line Length**: 82
- **Issues** (1):
  - Low docstring coverage: 0.0% (min: 80.0%)

### setup.py

- **Lines**: 14 (Code: 13, Comments: 0)
- **Functions**: 0, **Classes**: 0
- **Complexity**: 1
- **Docstring Coverage**: 0.0%
- **Max Line Length**: 43
- **Issues** (1):
  - Low docstring coverage: 0.0% (min: 80.0%)

### car_sales_dashboard\exceptions.py

- **Lines**: 119 (Code: 89, Comments: 1)
- **Functions**: 5, **Classes**: 4
- **Complexity**: 1
- **Docstring Coverage**: 55.6%
- **Max Line Length**: 88
- **Issues** (1):
  - Low docstring coverage: 55.6% (min: 80.0%)

### car_sales_dashboard\state.py

- **Lines**: 743 (Code: 546, Comments: 87)
- **Functions**: 32, **Classes**: 1
- **Complexity**: 1
- **Docstring Coverage**: 97.0%
- **Max Line Length**: 125
- **Issues** (1):
  - Long lines: 125 chars (max: 100)

### car_sales_dashboard\__init__.py

- **Lines**: 1 (Code: 0, Comments: 1)
- **Functions**: 0, **Classes**: 0
- **Complexity**: 1
- **Docstring Coverage**: 0.0%
- **Max Line Length**: 50
- **Issues** (1):
  - Low docstring coverage: 0.0% (min: 80.0%)

### scripts\validate-requirements.py

- **Lines**: 87 (Code: 63, Comments: 8)
- **Functions**: 2, **Classes**: 0
- **Complexity**: 2
- **Docstring Coverage**: 100.0%
- **Max Line Length**: 111
- **Issues** (1):
  - Long lines: 111 chars (max: 100)

### tests\__init__.py

- **Lines**: 2 (Code: 0, Comments: 1)
- **Functions**: 0, **Classes**: 0
- **Complexity**: 1
- **Docstring Coverage**: 0.0%
- **Max Line Length**: 47
- **Issues** (1):
  - Low docstring coverage: 0.0% (min: 80.0%)

### car_sales_dashboard\components\controls.py

- **Lines**: 243 (Code: 215, Comments: 10)
- **Functions**: 4, **Classes**: 0
- **Complexity**: 2
- **Docstring Coverage**: 100.0%
- **Max Line Length**: 100
- **Issues** (1):
  - Function 'sidebar_filters' has too many arguments: 7

### car_sales_dashboard\components\tables.py

- **Lines**: 272 (Code: 207, Comments: 34)
- **Functions**: 5, **Classes**: 0
- **Complexity**: 1
- **Docstring Coverage**: 80.0%
- **Max Line Length**: 116
- **Issues** (1):
  - Long lines: 116 chars (max: 100)

### car_sales_dashboard\components\__init__.py

- **Lines**: 73 (Code: 42, Comments: 20)
- **Functions**: 0, **Classes**: 0
- **Complexity**: 1
- **Docstring Coverage**: 0.0%
- **Max Line Length**: 92
- **Issues** (1):
  - Low docstring coverage: 0.0% (min: 80.0%)

### car_sales_dashboard\pages\__init__.py

- **Lines**: 9 (Code: 2, Comments: 4)
- **Functions**: 0, **Classes**: 0
- **Complexity**: 1
- **Docstring Coverage**: 0.0%
- **Max Line Length**: 66
- **Issues** (1):
  - Low docstring coverage: 0.0% (min: 80.0%)

### car_sales_dashboard\utils\validation.py

- **Lines**: 275 (Code: 187, Comments: 24)
- **Functions**: 9, **Classes**: 3
- **Complexity**: 1
- **Docstring Coverage**: 100.0%
- **Max Line Length**: 117
- **Issues** (1):
  - Long lines: 117 chars (max: 100)

### car_sales_dashboard\utils\__init__.py

- **Lines**: 31 (Code: 27, Comments: 0)
- **Functions**: 0, **Classes**: 0
- **Complexity**: 1
- **Docstring Coverage**: 0.0%
- **Max Line Length**: 54
- **Issues** (1):
  - Low docstring coverage: 0.0% (min: 80.0%)

### car_sales_dashboard\car_sales_dashboard.py

- **Lines**: 30 (Code: 20, Comments: 5)
- **Functions**: 1, **Classes**: 0
- **Complexity**: 2
- **Docstring Coverage**: 100.0%
- **Max Line Length**: 72
- **Issues**: None ✅

### car_sales_dashboard\components\feedback.py

- **Lines**: 279 (Code: 244, Comments: 0)
- **Functions**: 7, **Classes**: 0
- **Complexity**: 1
- **Docstring Coverage**: 100.0%
- **Max Line Length**: 97
- **Issues**: None ✅

### car_sales_dashboard\components\performance.py

- **Lines**: 238 (Code: 200, Comments: 5)
- **Functions**: 8, **Classes**: 0
- **Complexity**: 1
- **Docstring Coverage**: 100.0%
- **Max Line Length**: 97
- **Issues**: None ✅

### car_sales_dashboard\pages\fixed_tabs.py

- **Lines**: 159 (Code: 148, Comments: 8)
- **Functions**: 1, **Classes**: 0
- **Complexity**: 1
- **Docstring Coverage**: 100.0%
- **Max Line Length**: 93
- **Issues**: None ✅

### car_sales_dashboard\pages\fixed_tabs_new.py

- **Lines**: 159 (Code: 148, Comments: 8)
- **Functions**: 1, **Classes**: 0
- **Complexity**: 1
- **Docstring Coverage**: 100.0%
- **Max Line Length**: 93
- **Issues**: None ✅

### car_sales_dashboard\pages\index.py

- **Lines**: 45 (Code: 42, Comments: 1)
- **Functions**: 1, **Classes**: 0
- **Complexity**: 1
- **Docstring Coverage**: 100.0%
- **Max Line Length**: 89
- **Issues**: None ✅

### car_sales_dashboard\utils\dashboard_layout.py

- **Lines**: 559 (Code: 488, Comments: 20)
- **Functions**: 12, **Classes**: 1
- **Complexity**: 1
- **Docstring Coverage**: 100.0%
- **Max Line Length**: 97
- **Issues**: None ✅

### car_sales_dashboard\utils\simple_test_runner.py

- **Lines**: 450 (Code: 305, Comments: 46)
- **Functions**: 16, **Classes**: 1
- **Complexity**: 2
- **Docstring Coverage**: 82.4%
- **Max Line Length**: 94
- **Issues**: None ✅

### car_sales_dashboard\utils\ui_utils.py

- **Lines**: 118 (Code: 106, Comments: 1)
- **Functions**: 2, **Classes**: 0
- **Complexity**: 1
- **Docstring Coverage**: 100.0%
- **Max Line Length**: 96
- **Issues**: None ✅

## Recommendations

### General Improvements
- Add comprehensive docstrings to all public functions and classes
- Ensure consistent code formatting (consider using black or autopep8)
- Add type hints for better code clarity and IDE support
- Consider using linting tools (pylint, flake8) in CI/CD pipeline

## Quality Thresholds Used

- **Max Complexity**: 15
- **Max Line Length**: 100
- **Min Docstring Coverage**: 0.8
- **Max Function Length**: 50
- **Max Class Length**: 300
- **Max Function Args**: 6
