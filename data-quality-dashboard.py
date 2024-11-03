import pandas as pd
import numpy as np
from datetime import datetime
import requests
import json
from pathlib import Path
import logging

class DataQualityDashboard:
    """
    A data quality monitoring dashboard for analyzing NYC Open Data.
    Uses real 311 Service Requests data to demonstrate data quality principles.
    """
    
    def __init__(self, data_path=None):
        """Initialize the dashboard with data path or download fresh data."""
        self.logger = self._setup_logging()
        
        if data_path:
            self.df = pd.read_csv(data_path)
        else:
            self.df = self._fetch_nyc_311_data()
            
        self.metrics = {}
        self.logger.info(f"Initialized dashboard with {len(self.df)} records")

    def _setup_logging(self):
        """Set up logging configuration."""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('data_quality.log'),
                logging.StreamHandler()
            ]
        )
        return logging.getLogger(__name__)

    def _fetch_nyc_311_data(self):
        """
        Fetch real NYC 311 Service Requests data using Socrata Open Data API.
        Limited to last 1000 records for demo purposes.
        """
        url = "https://data.cityofnewyork.us/resource/erm2-nwe9.json"
        params = {
            "$limit": 1000,
            "$order": "created_date DESC"
        }
        
        self.logger.info("Fetching NYC 311 data...")
        response = requests.get(url, params=params)
        
        if response.status_code == 200:
            data = pd.DataFrame(response.json())
            self.logger.info("Data fetched successfully")
            return data
        else:
            self.logger.error(f"Failed to fetch data: {response.status_code}")
            raise Exception("Failed to fetch NYC 311 data")

    def calculate_completeness(self, columns=None):
        """Calculate the completeness score for specified columns."""
        if not columns:
            columns = self.df.columns
            
        completeness_scores = {}
        for col in columns:
            non_null_count = self.df[col].count()
            total_count = len(self.df)
            completeness_scores[col] = (non_null_count / total_count) * 100
            
        self.metrics['completeness'] = completeness_scores
        return completeness_scores

    def calculate_timeliness(self, date_column='created_date'):
        """Calculate timeliness metrics for the dataset."""
        if date_column not in self.df.columns:
            self.logger.warning(f"Date column {date_column} not found in dataset")
            return None
            
        self.df[date_column] = pd.to_datetime(self.df[date_column])
        current_time = pd.Timestamp.now()
        
        time_differences = current_time - self.df[date_column]
        
        timeliness_metrics = {
            'average_age_days': time_differences.mean().days,
            'oldest_record_days': time_differences.max().days,
            'newest_record_days': time_differences.min().days
        }
        
        self.metrics['timeliness'] = timeliness_metrics
        return timeliness_metrics

    def calculate_consistency(self, categorical_columns=None):
        """
        Calculate consistency metrics for categorical columns.
        Identifies potential data quality issues in categorical fields.
        """
        if not categorical_columns:
            categorical_columns = self.df.select_dtypes(include=['object']).columns
            
        consistency_metrics = {}
        for col in categorical_columns:
            value_counts = self.df[col].value_counts()
            unique_ratio = (len(value_counts) / len(self.df)) * 100
            
            consistency_metrics[col] = {
                'unique_values': len(value_counts),
                'unique_ratio': unique_ratio,
                'most_common': value_counts.head(3).to_dict()
            }
            
        self.metrics['consistency'] = consistency_metrics
        return consistency_metrics

    def generate_report(self, output_path='data_quality_report.json'):
        """Generate a comprehensive data quality report."""
        if not self.metrics:
            self.calculate_completeness()
            self.calculate_timeliness()
            self.calculate_consistency()
            
        report = {
            'report_generated': datetime.now().isoformat(),
            'dataset_size': len(self.df),
            'metrics': self.metrics
        }
        
        # Save report to file
        with open(output_path, 'w') as f:
            json.dump(report, f, indent=4)
            
        self.logger.info(f"Report generated and saved to {output_path}")
        return report

def main():
    """
    Main function to demonstrate the dashboard's capabilities.
    """
    # Initialize dashboard
    dashboard = DataQualityDashboard()
    
    # Calculate all metrics
    completeness = dashboard.calculate_completeness()
    timeliness = dashboard.calculate_timeliness()
    consistency = dashboard.calculate_consistency()
    
    # Generate and save report
    report = dashboard.generate_report()
    
    # Print summary
    print("\n=== Data Quality Dashboard Summary ===")
    print(f"Dataset Size: {len(dashboard.df)} records")
    print("\nCompleteness Scores (Top 5):")
    for col, score in sorted(completeness.items(), key=lambda x: x[1], reverse=True)[:5]:
        print(f"{col}: {score:.2f}%")
        
    print("\nTimeliness Metrics:")
    for metric, value in timeliness.items():
        print(f"{metric}: {value}")
        
    print("\nConsistency Issues:")
    for col, metrics in consistency.items():
        if metrics['unique_ratio'] > 80:  # Flag high cardinality
            print(f"High cardinality in {col}: {metrics['unique_ratio']:.2f}% unique values")

if __name__ == "__main__":
    main()
