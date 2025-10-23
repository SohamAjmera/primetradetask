#!/usr/bin/env python3
"""
Bitcoin Market Sentiment and Trader Performance Analysis
========================================================

This script analyzes the relationship between Bitcoin market sentiment (Fear/Greed Index)
and trader performance data from Hyperliquid to uncover patterns and insights for
smarter trading strategies.

Author: Data Science Analysis
Date: 2025
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

plt.style.use('seaborn-v0_8')
sns.set_palette("husl")

class BitcoinSentimentAnalyzer:
    def __init__(self, fear_greed_path, historical_data_path):
        """Initialize the analyzer with data paths."""
        self.fear_greed_path = fear_greed_path
        self.historical_data_path = historical_data_path
        self.fear_greed_data = None
        self.historical_data = None
        self.merged_data = None
        
    def load_data(self):
        """Load and preprocess the datasets."""
        print("Loading Fear/Greed Index data...")
        self.fear_greed_data = pd.read_csv(self.fear_greed_path)
        
        print("Loading Historical Trader Data...")
        self.historical_data = pd.read_csv(self.historical_data_path)
        
        print(f"Fear/Greed data shape: {self.fear_greed_data.shape}")
        print(f"Historical data shape: {self.historical_data.shape}")
        
        return self.fear_greed_data, self.historical_data
    
    def preprocess_fear_greed_data(self):
        """Preprocess the Fear/Greed Index data."""
        print("\nPreprocessing Fear/Greed Index data...")
        
        self.fear_greed_data['timestamp'] = pd.to_datetime(self.fear_greed_data['timestamp'], unit='s')
        self.fear_greed_data['date'] = pd.to_datetime(self.fear_greed_data['date'])
        
        def categorize_sentiment(value):
            if value <= 25:
                return 'Extreme Fear'
            elif value <= 45:
                return 'Fear'
            elif value <= 55:
                return 'Neutral'
            elif value <= 75:
                return 'Greed'
            else:
                return 'Extreme Greed'
        
        self.fear_greed_data['sentiment_category'] = self.fear_greed_data['value'].apply(categorize_sentiment)
        
        self.fear_greed_data['sentiment_score'] = self.fear_greed_data['value']
        
        print("Fear/Greed data preprocessing completed.")
        return self.fear_greed_data
    
    def preprocess_historical_data(self):
        """Preprocess the historical trader data."""
        print("\nPreprocessing Historical Trader Data...")
        
        self.historical_data['Timestamp IST'] = pd.to_datetime(self.historical_data['Timestamp IST'], format='%d-%m-%Y %H:%M')
        self.historical_data['Timestamp'] = pd.to_datetime(self.historical_data['Timestamp'], unit='ms')
        
        self.historical_data['date'] = self.historical_data['Timestamp IST'].dt.date
        
        numeric_columns = ['Execution Price', 'Size Tokens', 'Size USD', 'Closed PnL', 'Fee']
        for col in numeric_columns:
            self.historical_data[col] = pd.to_numeric(self.historical_data[col], errors='coerce')
        
        daily_metrics = self.historical_data.groupby('date').agg({
            'Closed PnL': ['sum', 'mean', 'count'],
            'Size USD': ['sum', 'mean'],
            'Fee': 'sum',
            'Account': 'nunique'
        }).round(2)
        
        daily_metrics.columns = ['total_pnl', 'avg_pnl', 'trade_count', 'total_volume', 'avg_trade_size', 'total_fees', 'unique_traders']
        
        daily_metrics['profitability'] = daily_metrics['total_pnl'] > 0
        daily_metrics['win_rate'] = self.historical_data.groupby('date')['Closed PnL'].apply(lambda x: (x > 0).mean())
        
        self.daily_metrics = daily_metrics.reset_index()
        self.daily_metrics['date'] = pd.to_datetime(self.daily_metrics['date'])
        
        print("Historical data preprocessing completed.")
        return self.daily_metrics
    
    def merge_datasets(self):
        """Merge Fear/Greed data with historical trader data."""
        print("\nMerging datasets...")
        
        self.merged_data = pd.merge(
            self.fear_greed_data,
            self.daily_metrics,
            on='date',
            how='inner'
        )
        
        print(f"Merged data shape: {self.merged_data.shape}")
        print("Data merging completed.")
        return self.merged_data
    
    def analyze_sentiment_performance_correlation(self):
        """Analyze correlation between sentiment and trader performance."""
        print("\nAnalyzing sentiment-performance correlation...")
        
        numeric_cols = ['sentiment_score', 'total_pnl', 'avg_pnl', 'trade_count', 
                       'total_volume', 'win_rate', 'unique_traders']
        
        correlation_matrix = self.merged_data[numeric_cols].corr()
        
        sentiment_correlations = correlation_matrix['sentiment_score'].drop('sentiment_score').sort_values(ascending=False)
        
        print("\nSentiment Score Correlations:")
        for metric, corr in sentiment_correlations.items():
            print(f"{metric}: {corr:.3f}")
        
        return correlation_matrix, sentiment_correlations
    
    def analyze_performance_by_sentiment_category(self):
        """Analyze trader performance by sentiment category."""
        print("\nAnalyzing performance by sentiment category...")
        
        sentiment_performance = self.merged_data.groupby('sentiment_category').agg({
            'total_pnl': ['mean', 'median', 'std'],
            'avg_pnl': ['mean', 'median'],
            'win_rate': ['mean', 'median'],
            'trade_count': 'mean',
            'total_volume': 'mean',
            'unique_traders': 'mean'
        }).round(2)
        
        print("\nPerformance by Sentiment Category:")
        print(sentiment_performance)
        
        return sentiment_performance
    
    def create_visualizations(self):
        """Create comprehensive visualizations."""
        print("\nCreating visualizations...")
        
        fig = plt.figure(figsize=(20, 15))
        
        plt.subplot(3, 3, 1)
        plt.plot(self.merged_data['date'], self.merged_data['sentiment_score'], 
                color='blue', alpha=0.7, linewidth=1)
        plt.title('Bitcoin Fear/Greed Index Over Time', fontsize=12, fontweight='bold')
        plt.xlabel('Date')
        plt.ylabel('Sentiment Score')
        plt.xticks(rotation=45)
        plt.grid(True, alpha=0.3)
        
        plt.subplot(3, 3, 2)
        plt.plot(self.merged_data['date'], self.merged_data['total_pnl'], 
                color='green', alpha=0.7, linewidth=1)
        plt.title('Daily Total PnL Over Time', fontsize=12, fontweight='bold')
        plt.xlabel('Date')
        plt.ylabel('Total PnL (USD)')
        plt.xticks(rotation=45)
        plt.grid(True, alpha=0.3)
        
        plt.subplot(3, 3, 3)
        scatter = plt.scatter(self.merged_data['sentiment_score'], 
                            self.merged_data['total_pnl'], 
                            c=self.merged_data['total_pnl'], 
                            cmap='RdYlGn', alpha=0.6)
        plt.title('Sentiment Score vs Total PnL', fontsize=12, fontweight='bold')
        plt.xlabel('Sentiment Score')
        plt.ylabel('Total PnL (USD)')
        plt.colorbar(scatter)
        plt.grid(True, alpha=0.3)
        
        plt.subplot(3, 3, 4)
        sentiment_avg_pnl = self.merged_data.groupby('sentiment_category')['avg_pnl'].mean()
        sentiment_avg_pnl.plot(kind='bar', color=['red', 'orange', 'yellow', 'lightgreen', 'green'])
        plt.title('Average PnL by Sentiment Category', fontsize=12, fontweight='bold')
        plt.xlabel('Sentiment Category')
        plt.ylabel('Average PnL (USD)')
        plt.xticks(rotation=45)
        plt.grid(True, alpha=0.3)
        
        plt.subplot(3, 3, 5)
        sentiment_winrate = self.merged_data.groupby('sentiment_category')['win_rate'].mean()
        sentiment_winrate.plot(kind='bar', color=['red', 'orange', 'yellow', 'lightgreen', 'green'])
        plt.title('Win Rate by Sentiment Category', fontsize=12, fontweight='bold')
        plt.xlabel('Sentiment Category')
        plt.ylabel('Win Rate')
        plt.xticks(rotation=45)
        plt.grid(True, alpha=0.3)
        
        plt.subplot(3, 3, 6)
        sentiment_volume = self.merged_data.groupby('sentiment_category')['total_volume'].mean()
        sentiment_volume.plot(kind='bar', color=['red', 'orange', 'yellow', 'lightgreen', 'green'])
        plt.title('Average Trading Volume by Sentiment', fontsize=12, fontweight='bold')
        plt.xlabel('Sentiment Category')
        plt.ylabel('Total Volume (USD)')
        plt.xticks(rotation=45)
        plt.grid(True, alpha=0.3)
        
        plt.subplot(3, 3, 7)
        numeric_cols = ['sentiment_score', 'total_pnl', 'avg_pnl', 'win_rate', 'trade_count']
        corr_matrix = self.merged_data[numeric_cols].corr()
        sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', center=0, 
                   square=True, fmt='.2f')
        plt.title('Correlation Matrix', fontsize=12, fontweight='bold')
        
        plt.subplot(3, 3, 8)
        self.merged_data['sentiment_category'].value_counts().plot(kind='pie', autopct='%1.1f%%')
        plt.title('Distribution of Sentiment Categories', fontsize=12, fontweight='bold')
        plt.ylabel('')
        
        plt.subplot(3, 3, 9)
        for sentiment in self.merged_data['sentiment_category'].unique():
            data = self.merged_data[self.merged_data['sentiment_category'] == sentiment]['total_pnl']
            plt.hist(data, alpha=0.5, label=sentiment, bins=20)
        plt.title('PnL Distribution by Sentiment', fontsize=12, fontweight='bold')
        plt.xlabel('Total PnL (USD)')
        plt.ylabel('Frequency')
        plt.legend()
        plt.grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.savefig('/Users/sohamajmera/Desktop/primetradetask/bitcoin_sentiment_analysis.png', 
                   dpi=300, bbox_inches='tight')
        plt.show()
        
        print("Visualizations saved as 'bitcoin_sentiment_analysis.png'")
    
    def generate_insights(self):
        """Generate key insights and recommendations."""
        print("\n" + "="*60)
        print("KEY INSIGHTS AND RECOMMENDATIONS")
        print("="*60)
        
        total_trades = self.merged_data['trade_count'].sum()
        total_volume = self.merged_data['total_volume'].sum()
        avg_daily_pnl = self.merged_data['total_pnl'].mean()
        profitable_days = (self.merged_data['total_pnl'] > 0).sum()
        total_days = len(self.merged_data)
        
        print(f"\n📊 OVERALL PERFORMANCE METRICS:")
        print(f"   • Total Trades Analyzed: {total_trades:,.0f}")
        print(f"   • Total Trading Volume: ${total_volume:,.2f}")
        print(f"   • Average Daily PnL: ${avg_daily_pnl:,.2f}")
        print(f"   • Profitable Days: {profitable_days}/{total_days} ({profitable_days/total_days*100:.1f}%)")
        
        sentiment_performance = self.merged_data.groupby('sentiment_category').agg({
            'total_pnl': ['mean', 'count'],
            'win_rate': 'mean',
            'avg_pnl': 'mean'
        }).round(2)
        
        print(f"\n📈 PERFORMANCE BY SENTIMENT:")
        for sentiment in ['Extreme Fear', 'Fear', 'Neutral', 'Greed', 'Extreme Greed']:
            if sentiment in sentiment_performance.index:
                data = sentiment_performance.loc[sentiment]
                avg_pnl = data[('total_pnl', 'mean')]
                win_rate = data[('win_rate', 'mean')] * 100
                days = data[('total_pnl', 'count')]
                print(f"   • {sentiment:12}: Avg PnL: ${avg_pnl:8.2f}, Win Rate: {win_rate:5.1f}%, Days: {days:3.0f}")
        
        sentiment_corr = self.merged_data['sentiment_score'].corr(self.merged_data['total_pnl'])
        winrate_corr = self.merged_data['sentiment_score'].corr(self.merged_data['win_rate'])
        
        print(f"\n🔍 CORRELATION INSIGHTS:")
        print(f"   • Sentiment vs Total PnL: {sentiment_corr:.3f}")
        print(f"   • Sentiment vs Win Rate: {winrate_corr:.3f}")
        
        best_sentiment = sentiment_performance[('total_pnl', 'mean')].idxmax()
        best_avg_pnl = sentiment_performance.loc[best_sentiment, ('total_pnl', 'mean')]
        
        print(f"\n🎯 KEY FINDINGS:")
        print(f"   • Best performing sentiment: {best_sentiment} (Avg PnL: ${best_avg_pnl:.2f})")
        
        if sentiment_corr > 0.1:
            print(f"   • Positive correlation between sentiment and performance")
        elif sentiment_corr < -0.1:
            print(f"   • Negative correlation between sentiment and performance")
        else:
            print(f"   • Weak correlation between sentiment and performance")

        print(f"\n💡 TRADING RECOMMENDATIONS:")
        
        sentiment_ranges = []
        for sentiment in ['Extreme Fear', 'Fear', 'Neutral', 'Greed', 'Extreme Greed']:
            if sentiment in sentiment_performance.index:
                avg_pnl = sentiment_performance.loc[sentiment, ('total_pnl', 'mean')]
                sentiment_ranges.append((sentiment, avg_pnl))
        
        sentiment_ranges.sort(key=lambda x: x[1], reverse=True)
        
        print(f"   • Optimal sentiment for trading: {sentiment_ranges[0][0]}")
        print(f"   • Consider reducing activity during: {sentiment_ranges[-1][0]}")
        
        fear_days = len(self.merged_data[self.merged_data['sentiment_category'].isin(['Fear', 'Extreme Fear'])])
        greed_days = len(self.merged_data[self.merged_data['sentiment_category'].isin(['Greed', 'Extreme Greed'])])
        
        print(f"\n RISK MANAGEMENT INSIGHTS:")
        print(f"   • Fear periods: {fear_days} days - Consider contrarian strategies")
        print(f"   • Greed periods: {greed_days} days - Consider profit-taking")
        
        return {
            'total_trades': total_trades,
            'total_volume': total_volume,
            'avg_daily_pnl': avg_daily_pnl,
            'profitable_days_ratio': profitable_days/total_days,
            'sentiment_correlation': sentiment_corr,
            'best_sentiment': best_sentiment,
            'sentiment_performance': sentiment_performance
        }
    
    def run_complete_analysis(self):
        """Run the complete analysis pipeline."""
        print("🚀 Starting Bitcoin Sentiment and Trader Performance Analysis")
        print("="*70)
        
        self.load_data()
        
        self.preprocess_fear_greed_data()
        self.preprocess_historical_data()
        
        self.merge_datasets()
        
        correlation_matrix, sentiment_correlations = self.analyze_sentiment_performance_correlation()
        sentiment_performance = self.analyze_performance_by_sentiment_category()
        
        self.create_visualizations()
        
        insights = self.generate_insights()
        
        print("\nAnalysis completed successfully!")
        print("Results saved as 'bitcoin_sentiment_analysis.png'")
        
        return insights

def main():
    """Main execution function."""
    analyzer = BitcoinSentimentAnalyzer(
        fear_greed_path='/Users/sohamajmera/Desktop/primetradetask/fear_greed_index.csv',
        historical_data_path='/Users/sohamajmera/Desktop/primetradetask/historical_data.csv'
    )

    insights = analyzer.run_complete_analysis()
    
    return insights

if __name__ == "__main__":
    insights = main()
