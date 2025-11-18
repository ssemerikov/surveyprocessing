# Ukrainian Education Survey Analysis Platform

Comprehensive analysis software for the Ukrainian education survey dataset on the effectiveness of information-digital environments in general secondary education from parents' perspective.

---

## 📊 About This Repository

This repository contains **two components**:

1. **Analysis Software** - Production-ready Python platform for analyzing the survey data
2. **Survey Dataset** - Original data files from the survey (5,224 responses)

---

## 🚀 Analysis Software

### Overview
Professional data processing and analysis platform built specifically for this Ukrainian education survey, providing:
- Multi-format data loading (CSV, TSV, XLSX)
- Ukrainian language text processing
- Comprehensive statistical analysis
- Interactive visualizations
- Automated report generation

### Sample Size & Context
- **5,224 parent responses**
- **Collection Period**: October 7-18, 2024
- **Geographic Coverage**: 21 regions of Ukraine + Kyiv
- **Language**: Ukrainian
- **Context**: Wartime conditions affecting education
- **Questions**: 22 covering demographics, educational formats, digital environments, and suggestions

### Core Analysis Modules

1. **Data Loading & Preprocessing** - Multi-format support with Ukrainian text handling
2. **Descriptive Statistics** - Comprehensive frequency distributions and cross-tabulations
3. **Regional Analysis** - Region-specific insights with geographic visualization
4. **Digital Environment Analysis** - Platform usage, communication channels, technical support
5. **Student Digital Skills Assessment** - Competency analysis by grade level
6. **Text Analysis** - Ukrainian language NLP for open-ended responses
7. **Statistical Testing** - Chi-square, ANOVA, correlation, regression
8. **Visualization** - Interactive dashboards and publication-quality graphics
9. **War Impact Analysis** - Wartime education challenges and adaptations
10. **Report Generation** - Automated bilingual reports (Ukrainian/English)

### Technical Highlights
- **Multi-language Support**: Full Ukrainian text processing with English translations
- **Data Quality Framework**: Automated validation and anomaly detection
- **Interactive Dashboard**: Web-based exploration interface
- **Geographic Visualization**: Regional heatmaps and choropleth maps
- **Scalable Architecture**: Handles 5,000+ responses efficiently
- **Privacy-Preserving**: Anonymization and secure data handling

---

## 📁 Project Structure

```
surveyprocessing/
├── src/                   # Analysis software source code
│   ├── models/           # Data models (Survey, Response, Quality metrics)
│   ├── ingestion/        # Data loading (multi-format, Ukrainian text)
│   ├── validation/       # Quality checks and validation
│   ├── analysis/         # Analysis modules (stats, text, regional)
│   └── pipeline.py       # Main analysis orchestrator
├── tests/                # Comprehensive test suite (44 tests)
├── data/raw/             # Survey data files (moved from root)
│   ├── answers.csv       # Survey responses (UTF-8)
│   ├── answers.tsv       # Tab-separated format
│   └── answers.xlsx      # Excel format
├── config/               # Configuration files
├── docs/                 # Documentation
├── reports/              # Generated analysis reports
├── codebook.md           # Survey variable descriptions
├── LICENSE.txt           # License information
└── README.md             # This file
```

---

## 🎯 Quick Start

### Installation

```bash
# Clone repository
git clone <repository-url>
cd surveyprocessing

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements/base.txt
```

### Running Analysis

```python
from src.pipeline import SurveyAnalysisPipeline

# Initialize pipeline
pipeline = SurveyAnalysisPipeline(config_path='config/config.yaml')

# Load and process data
pipeline.load_data('data/raw/answers.csv')

# Run complete analysis
results = pipeline.run_analysis()

# Generate reports
pipeline.generate_reports(output_dir='reports/')

# Launch interactive dashboard
pipeline.launch_dashboard(port=8050)
```

### Quick Analysis Script

```bash
# Run complete analysis
python analyze_survey.py

# Explore data structure
python explore_data.py

# Run tests
python run_tests.py
```

---

## 📊 Survey Dataset Information

### Dataset Overview

This dataset contains survey responses from parents of students in general secondary education institutions in Ukraine regarding the effectiveness of information and digital environments in schools. The survey was conducted from **October 7 to October 18, 2024**, during the period of the ongoing war in Ukraine, which affects the educational process and creates specific challenges for schools.

The survey collected responses from **5,224 parents** from 21 regions of Ukraine and the city of Kyiv. The questionnaire aimed to understand how parents interact with digital platforms used by schools, their assessment of children's digital skills, and their suggestions for improving digital educational environments.

### Data Collection Methodology

The survey was conducted as part of research project № 0123U100497 "Methodology of monitoring research on the effectiveness of information and digital environment of general secondary education institutions in the context of Ukraine's European integration" by the **Institute for Digitalisation of Education of the National Academy of Educational Sciences of Ukraine**.

Data was collected through an online survey created with Google Forms. The survey link was distributed through Telegram groups of teachers from different regions of Ukraine who participate in educational projects of the NGO "Agency for Educational Policy Development." Participation was voluntary and anonymous.

The sample is non-representative. The survey was conducted during wartime conditions, with schools operating in various formats (in-person, distance learning, or mixed format) depending on the security situation in different regions.

### Data Files

- `answers.csv` - Survey responses in CSV format (UTF-8 encoded)
- `answers.tsv` - Survey responses in TSV format
- `answers.xlsx` - Survey responses in Excel format
- `codebook.md` - Description of variables and their values
- `LICENSE.txt` - License information
- `manifest.json` - Inventory of all files in the package
- `metadata.json` - Structured metadata about the dataset
- `zenodo_metadata.json` - Metadata formatted for Zenodo submission

### Dataset Content

The survey collected information about:

1. Demographic data of respondents (age, gender, region of residence)
2. Information about children's education (grade, type of educational institution, format of education)
3. Digital platforms and tools used by educational institutions
4. Communication channels between parents and teachers
5. Parents' assessment of their children's digital skills and learning independence
6. Technical support and resources available to parents and children
7. Parents' suggestions for improving the digital environment in schools

### Data Processing

The data was collected through Google Forms and exported to Excel format. It was then converted to open formats (CSV, TSV) without additional cleaning or editing. The data is provided in its original form as collected from respondents, with responses in Ukrainian language.

---

## 📖 Documentation

- **[COMPREHENSIVE_ANALYSIS_STRATEGY.md](COMPREHENSIVE_ANALYSIS_STRATEGY.md)** - 100+ page strategic framework
- **[IMPLEMENTATION_SUMMARY.md](IMPLEMENTATION_SUMMARY.md)** - Project status and deliverables
- **[TEST_REPORT.md](TEST_REPORT.md)** - Comprehensive test suite documentation
- **[codebook.md](codebook.md)** - Survey variable descriptions and values
- **config/config.yaml** - Full configuration reference

---

## 🧪 Testing

```bash
# Run all tests (requires pytest)
pytest tests/ -v

# Run with coverage
pytest tests/ --cov=src --cov-report=html

# Run simple verification (no dependencies)
python run_tests.py

# Verify code structure
python verify_code_structure.py
```

**Test Coverage**:
- 44 tests across 7 test files
- Unit tests for all core modules
- Integration tests for data flow
- >85% code coverage target

---

## 🏆 Features & Capabilities

### Data Processing
- ✅ Multi-format loading (CSV, TSV, XLSX, JSON)
- ✅ Ukrainian text encoding (UTF-8 + CP-1251 fallback)
- ✅ Column transliteration (Ukrainian → English)
- ✅ Multiple-choice question parsing
- ✅ Derived variable creation
- ✅ Missing data handling

### Quality Assurance
- ✅ 5-dimensional quality assessment
- ✅ Completeness, accuracy, consistency, validity, uniqueness checks
- ✅ Anomaly detection (outliers, bots, duplicates)
- ✅ Quality scoring (0-100) and grading (A-F)

### Analysis
- ✅ Descriptive statistics (frequencies, cross-tabs)
- ✅ Regional analysis (25 region profiles)
- ✅ Text analysis (Ukrainian NLP, 12 themes, sentiment)
- ✅ Platform analysis (usage, satisfaction, distribution)
- ✅ Student skills assessment
- ✅ Wartime impact analysis

### Outputs
- ✅ Excel reports (50+ sheets)
- ✅ PDF reports (executive + comprehensive)
- ✅ Interactive dashboard (Dash/Plotly)
- ✅ 40+ visualizations
- ✅ Data exports (processed datasets)

---

## 👥 Contributors

### Dataset
- **Data Collection**: Iryna Ivaniuk (https://orcid.org/0000-0003-2381-785X)
- **Metadata Preparation**: Olha Pinchuk (https://orcid.org/0000-0002-2770-0838), Serhiy Semerikov (https://orcid.org/0000-0003-0789-0272)

### Analysis Software
- Built for the Institute for Digitalisation of Education of the NAES of Ukraine
- Developed as part of research project № 0123U100497

---

## 📄 License

See [LICENSE.txt](LICENSE.txt) for details.

---

## 📞 Contact

For questions about this dataset or analysis software, please contact:

**Institute for Digitalisation of Education**
National Academy of Educational Sciences of Ukraine
Website: https://iitlt.gov.ua/

---

## 🔗 Data Source

Original dataset available on Zenodo:
**DOI**: 10.5281/zenodo.15231534
**URL**: https://zenodo.org/records/15231534

---

## 🌟 Citation

If you use this dataset or analysis software in your research, please cite:

```bibtex
@dataset{ukrainian_education_survey_2024,
  author = {Ivaniuk, Iryna and Pinchuk, Olha and Semerikov, Serhiy},
  title = {Survey on the Effectiveness of Information-Digital Environment in General Secondary Education from Parents' Perspective},
  year = {2024},
  publisher = {Zenodo},
  doi = {10.5281/zenodo.15231534},
  url = {https://zenodo.org/records/15231534}
}
```

---

**Status**: ✅ Production-ready analysis platform with comprehensive test coverage and documentation.
