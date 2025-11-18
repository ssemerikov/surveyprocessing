"""Pytest configuration and shared fixtures."""

import sys
from pathlib import Path
from io import StringIO
import tempfile

import pytest

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))


@pytest.fixture
def sample_csv_data():
    """Sample CSV data for testing."""
    return """Отметка времени,1. Ваш вік ,2. Ваша стать,3.  В якому класі навчається Ваша дитина або Ваші діти (можна обрати кілька варіантів відповідей)? ,4. Зазначте свою область проживання
10/18/2024 8:20:17,від 45 та старше,Жінка,9 клас,Харківська область
10/7/2024 18:26:43,від 35 до 44,Жінка,10 клас,Київська область
10/8/2024 10:15:30,від 25 до 34,Чоловік,5 клас,Львівська область"""


@pytest.fixture
def sample_csv_file(tmp_path, sample_csv_data):
    """Create a temporary CSV file for testing."""
    csv_file = tmp_path / "test_survey.csv"
    csv_file.write_text(sample_csv_data, encoding='utf-8')
    return csv_file


@pytest.fixture
def sample_text_data():
    """Sample Ukrainian text for testing."""
    return [
        "Потрібно покращити якість інтернету в школі",
        "Технічна підтримка дуже погано працює",
        "Добре що є електронний журнал",
        "Платформа Google Classroom зручна для використання",
        "Не вистачає обладнання для дистанційного навчання"
    ]


@pytest.fixture
def config_dict():
    """Sample configuration dictionary."""
    return {
        'data': {
            'input': {
                'encoding': 'utf-8',
                'language': 'uk'
            },
            'validation': {
                'min_response_completeness': 0.7
            }
        },
        'analysis': {
            'text_analysis': {
                'min_word_length': 3,
                'n_topics': 10
            }
        }
    }
