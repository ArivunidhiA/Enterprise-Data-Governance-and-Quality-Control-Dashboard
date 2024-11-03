# Data Quality Dashboard

A student-developed data quality monitoring dashboard that analyzes real NYC 311 Service Requests data. This project demonstrates practical implementation of data governance and quality control principles using real-world data.

## Features

- **Real-Time Data Analysis**: Fetches live data from NYC Open Data API
- **Quality Metrics**:
  - Data Completeness Scoring
  - Timeliness Analysis
  - Consistency Checking
  - Automated Report Generation
- **Professional Setup**:
  - Comprehensive Logging
  - Error Handling
  - JSON Report Export

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/data-quality-dashboard.git
cd data-quality-dashboard
```

2. Create a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install required packages:
```bash
pip install -r requirements.txt
```

## Usage

1. Basic usage:
```python
from data_quality_dashboard import DataQualityDashboard

# Initialize dashboard (automatically fetches fresh data)
dashboard = DataQualityDashboard()

# Generate comprehensive report
dashboard.generate_report()
```

2. Run the demo:
```bash
python data_quality_dashboard.py
```

## Sample Output

The dashboard generates a comprehensive report including:

```json
{
    "report_generated": "2024-03-11T14:30:00",
    "dataset_size": 1000,
    "metrics": {
        "completeness": {
            "created_date": 100.0,
            "complaint_type": 99.8,
            ...
        },
        "timeliness": {
            "average_age_days": 15.3,
            "oldest_record_days": 30,
            "newest_record_days": 1
        },
        ...
    }
}
```

## Project Structure

```
data-quality-dashboard/
├── data_quality_dashboard.py   # Main script
├── requirements.txt           # Dependencies
├── README.md                 # This file
├── .gitignore               # Git ignore file
└── data_quality.log         # Generated log file
```

## Data Source

This project uses the [NYC 311 Service Requests](https://data.cityofnewyork.us/Social-Services/311-Service-Requests-from-2010-to-Present/erm2-nwe9) dataset, which provides real-world data about public service requests in New York City.

## Educational Value

This project demonstrates:
- Working with real-world data
- Implementing data quality metrics
- Professional software development practices
- API integration
- Error handling and logging
- Report generation

## Future Improvements

Potential enhancements for contributors:
1. Add data visualization components
2. Implement more sophisticated quality metrics
3. Create a web interface
4. Add unit tests
5. Integrate with other data sources

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.
