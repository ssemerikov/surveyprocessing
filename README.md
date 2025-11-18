# Ukrainian Education Survey Analysis Platform

Comprehensive analysis software for analyzing survey data about the effectiveness of information-digital environments in Ukrainian general secondary education from parents' perspective.

## Dataset Overview
- **Sample Size**: 5,224 parent responses
- **Collection Period**: October 7-18, 2024 (wartime conditions)
- **Geographic Coverage**: 21 regions of Ukraine + Kyiv
- **Language**: Ukrainian
- **Variables**: 22 questions covering demographics, educational formats, digital environments, and improvement suggestions

## Features

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

## Project Structure

```
education_survey_analysis/
├── data/
│   ├── raw/              # Original survey data
│   ├── processed/        # Cleaned and transformed data
│   └── outputs/          # Analysis results
├── src/
│   ├── models/           # Data models and schemas
│   ├── ingestion/        # Data loading modules
│   ├── transformation/   # Data transformation logic
│   ├── validation/       # Validation rules
│   ├── analysis/         # Analysis modules
│   ├── visualization/    # Visualization components
│   └── utils/            # Utilities and helpers
├── notebooks/            # Jupyter notebooks for exploration
├── reports/              # Generated reports
├── tests/                # Unit and integration tests
├── config/               # Configuration files
└── docs/                 # Documentation
```

## Installation

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements/base.txt

# For development
pip install -r requirements/dev.txt
```

## Quick Start

```python
from src.pipeline import SurveyAnalysisPipeline

# Initialize pipeline
pipeline = SurveyAnalysisPipeline(config_path='config/config.yaml')

# Load and process data
pipeline.load_data('data/raw/survey_data.csv')

# Run analysis
results = pipeline.run_analysis()

# Generate reports
pipeline.generate_reports(output_dir='reports/')

# Launch dashboard
pipeline.launch_dashboard(port=8050)
```

## Usage Examples

### Load and Explore Data
```python
from src.ingestion.data_loader import DataLoader

loader = DataLoader(encoding='utf-8', language='uk')
df = loader.load_csv('data/raw/survey_data.csv')
print(loader.get_data_summary())
```

### Regional Analysis
```python
from src.analysis.regional_analysis import RegionalAnalyzer

regional = RegionalAnalyzer(df)
regional.analyze_by_region()
regional.create_choropleth_map(metric='digital_platform_usage')
```

### Text Analysis
```python
from src.analysis.text_analysis import UkrainianTextAnalyzer

text_analyzer = UkrainianTextAnalyzer(df['improvement_suggestions'])
themes = text_analyzer.extract_topics(n_topics=10)
text_analyzer.generate_wordcloud(save_path='reports/wordcloud.png')
```

### Generate Report
```python
from src.report_generator import ReportGenerator

report_gen = ReportGenerator(results, language='uk')
report_gen.generate_executive_summary('reports/executive_summary.pdf')
report_gen.generate_regional_reports('reports/regional_reports/')
```

## Configuration

Edit `config/config.yaml` to customize:
- Data paths and formats
- Analysis parameters
- Visualization settings
- Report templates
- Dashboard configuration

## Output Deliverables

1. **Statistical Summary Report** (PDF, 20-30 pages)
2. **Interactive Dashboard** (Web application)
3. **Regional Fact Sheets** (One-page summaries per region)
4. **Visualization Portfolio** (High-resolution charts/graphs)
5. **Raw Analysis Tables** (Excel workbook)
6. **Text Analysis Report** (Themes from open-ended responses)
7. **Policy Recommendations** (Data-driven insights)

## Development

### Running Tests
```bash
pytest tests/ -v --cov=src
```

### Code Quality
```bash
# Linting
flake8 src/
pylint src/

# Type checking
mypy src/

# Formatting
black src/
```

## Data Privacy & Security

- All personally identifiable information is removed
- Data encryption at rest
- Secure access controls
- Audit logging enabled
- GDPR-compliant data handling

## Performance

- Processes 5,000+ responses in <2 minutes
- Report generation in <5 minutes
- Dashboard supports concurrent users
- Optimized for memory efficiency

## Contributing

This project follows PEP 8 coding standards and includes:
- Type hints for all functions
- Comprehensive docstrings
- Unit tests with >80% coverage
- Integration tests for pipelines

## License

[Specify License]

## Citation

If you use this software in your research, please cite:

```bibtex
@software{ukrainian_education_survey_2024,
  title={Ukrainian Education Survey Analysis Platform},
  author={[Authors]},
  year={2024},
  url={[Repository URL]}
}
```

## Contact

[Contact Information]

## Acknowledgments

This software was developed to analyze data collected during wartime conditions in Ukraine, documenting the resilience and adaptation of the Ukrainian education system.
