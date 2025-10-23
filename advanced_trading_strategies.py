#!/usr/bin/env python3
"""
Advanced Trading Strategies Based on Bitcoin Sentiment Analysis
================================================================

This script implements and backtests various trading strategies based on
the sentiment analysis findings to demonstrate practical applications.

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

class AdvancedTradingStrategies:
    def __init__(self, merged_data):
        """Initialize with merged sentiment and trading data."""
        self.data = merged_data.copy()
        self.strategies = {}
        self.results = {}
        
    def contrarian_strategy(self, initial_capital=100000):
        """
        Implement contrarian strategy based on sentiment analysis.
        Buy during fear, sell during greed.
        """
        print("Implementing Contrarian Strategy...")
        
        # Initialize portfolio
        portfolio_value = initial_capital
        position_size = 0
        trades = []
        
        for idx, row in self.data.iterrows():
            sentiment = row['sentiment_score']
            daily_pnl = row['total_pnl']
            
            # Contrarian logic
            if sentiment <= 30:  # Fear territory
                # Increase position (buy more)
                if position_size < 0.8:  # Max 80% allocation
                    position_size += 0.1
                    action = "BUY"
            elif sentiment >= 70:  # Greed territory
                # Decrease position (sell)
                if position_size > 0.2:  # Min 20% allocation
                    position_size -= 0.1
                    action = "SELL"
            else:
                action = "HOLD"
            
            # Calculate portfolio performance
            portfolio_return = (daily_pnl / 1000000) * position_size  # Normalized
            portfolio_value += portfolio_return
            
            trades.append({
                'date': row['date'],
                'sentiment': sentiment,
                'action': action,
                'position_size': position_size,
                'daily_pnl': daily_pnl,
                'portfolio_value': portfolio_value,
                'portfolio_return': portfolio_return
            })
        
        strategy_df = pd.DataFrame(trades)
        self.strategies['contrarian'] = strategy_df
        
        # Calculate performance metrics
        total_return = (portfolio_value - initial_capital) / initial_capital * 100
        volatility = strategy_df['portfolio_return'].std() * np.sqrt(252)
        sharpe_ratio = (strategy_df['portfolio_return'].mean() * 252) / volatility if volatility > 0 else 0
        
        self.results['contrarian'] = {
            'total_return': total_return,
            'volatility': volatility,
            'sharpe_ratio': sharpe_ratio,
            'final_value': portfolio_value,
            'max_drawdown': self._calculate_max_drawdown(strategy_df['portfolio_value'])
        }
        
        print(f"Contrarian Strategy Results:")
        print(f"  Total Return: {total_return:.2f}%")
        print(f"  Volatility: {volatility:.2f}%")
        print(f"  Sharpe Ratio: {sharpe_ratio:.2f}")
        print(f"  Max Drawdown: {self.results['contrarian']['max_drawdown']:.2f}%")
        
        return strategy_df
    
    def sentiment_momentum_strategy(self, initial_capital=100000):
        """
        Implement momentum strategy based on sentiment trends.
        """
        print("Implementing Sentiment Momentum Strategy...")
        
        # Calculate sentiment momentum (5-day moving average)
        self.data['sentiment_ma5'] = self.data['sentiment_score'].rolling(window=5).mean()
        self.data['sentiment_momentum'] = self.data['sentiment_score'] - self.data['sentiment_ma5']
        
        portfolio_value = initial_capital
        position_size = 0.5  # Start with 50% allocation
        trades = []
        
        for idx, row in self.data.iterrows():
            if pd.isna(row['sentiment_momentum']):
                continue
                
            momentum = row['sentiment_momentum']
            daily_pnl = row['total_pnl']
            
            # Momentum logic
            if momentum < -5:  # Sentiment declining (fear increasing)
                position_size = min(0.8, position_size + 0.1)
                action = "BUY"
            elif momentum > 5:  # Sentiment rising (greed increasing)
                position_size = max(0.2, position_size - 0.1)
                action = "SELL"
            else:
                action = "HOLD"
            
            # Calculate performance
            portfolio_return = (daily_pnl / 1000000) * position_size
            portfolio_value += portfolio_return
            
            trades.append({
                'date': row['date'],
                'sentiment': row['sentiment_score'],
                'momentum': momentum,
                'action': action,
                'position_size': position_size,
                'daily_pnl': daily_pnl,
                'portfolio_value': portfolio_value,
                'portfolio_return': portfolio_return
            })
        
        strategy_df = pd.DataFrame(trades)
        self.strategies['momentum'] = strategy_df
        
        # Calculate performance metrics
        total_return = (portfolio_value - initial_capital) / initial_capital * 100
        volatility = strategy_df['portfolio_return'].std() * np.sqrt(252)
        sharpe_ratio = (strategy_df['portfolio_return'].mean() * 252) / volatility if volatility > 0 else 0
        
        self.results['momentum'] = {
            'total_return': total_return,
            'volatility': volatility,
            'sharpe_ratio': sharpe_ratio,
            'final_value': portfolio_value,
            'max_drawdown': self._calculate_max_drawdown(strategy_df['portfolio_value'])
        }
        
        print(f"Sentiment Momentum Strategy Results:")
        print(f"  Total Return: {total_return:.2f}%")
        print(f"  Volatility: {volatility:.2f}%")
        print(f"  Sharpe Ratio: {sharpe_ratio:.2f}")
        print(f"  Max Drawdown: {self.results['momentum']['max_drawdown']:.2f}%")
        
        return strategy_df
    
    def risk_parity_strategy(self, initial_capital=100000):
        """
        Implement risk parity strategy based on sentiment volatility.
        """
        print("Implementing Risk Parity Strategy...")
        
        # Calculate sentiment volatility
        self.data['sentiment_volatility'] = self.data['sentiment_score'].rolling(window=10).std()
        
        portfolio_value = initial_capital
        trades = []
        
        for idx, row in self.data.iterrows():
            if pd.isna(row['sentiment_volatility']):
                continue
                
            volatility = row['sentiment_volatility']
            daily_pnl = row['total_pnl']
            sentiment = row['sentiment_score']
            
            # Risk parity logic - adjust position based on volatility
            if volatility > 15:  # High volatility (uncertainty)
                position_size = 0.3  # Conservative
            elif volatility < 5:  # Low volatility (certainty)
                position_size = 0.7  # Aggressive
            else:
                position_size = 0.5  # Neutral
            
            # Adjust for sentiment
            if sentiment <= 30:  # Fear
                position_size *= 1.2  # Increase allocation
            elif sentiment >= 70:  # Greed
                position_size *= 0.8  # Decrease allocation
            
            position_size = max(0.1, min(0.9, position_size))  # Clamp between 10-90%
            
            # Calculate performance
            portfolio_return = (daily_pnl / 1000000) * position_size
            portfolio_value += portfolio_return
            
            trades.append({
                'date': row['date'],
                'sentiment': sentiment,
                'volatility': volatility,
                'position_size': position_size,
                'daily_pnl': daily_pnl,
                'portfolio_value': portfolio_value,
                'portfolio_return': portfolio_return
            })
        
        strategy_df = pd.DataFrame(trades)
        self.strategies['risk_parity'] = strategy_df
        
        # Calculate performance metrics
        total_return = (portfolio_value - initial_capital) / initial_capital * 100
        volatility = strategy_df['portfolio_return'].std() * np.sqrt(252)
        sharpe_ratio = (strategy_df['portfolio_return'].mean() * 252) / volatility if volatility > 0 else 0
        
        self.results['risk_parity'] = {
            'total_return': total_return,
            'volatility': volatility,
            'sharpe_ratio': sharpe_ratio,
            'final_value': portfolio_value,
            'max_drawdown': self._calculate_max_drawdown(strategy_df['portfolio_value'])
        }
        
        print(f"Risk Parity Strategy Results:")
        print(f"  Total Return: {total_return:.2f}%")
        print(f"  Volatility: {volatility:.2f}%")
        print(f"  Sharpe Ratio: {sharpe_ratio:.2f}")
        print(f"  Max Drawdown: {self.results['risk_parity']['max_drawdown']:.2f}%")
        
        return strategy_df
    
    def _calculate_max_drawdown(self, portfolio_values):
        """Calculate maximum drawdown."""
        peak = portfolio_values.expanding().max()
        drawdown = (portfolio_values - peak) / peak * 100
        return drawdown.min()
    
    def compare_strategies(self):
        """Compare all implemented strategies."""
        print("\n" + "="*60)
        print("STRATEGY COMPARISON RESULTS")
        print("="*60)
        
        comparison_df = pd.DataFrame(self.results).T
        comparison_df = comparison_df.sort_values('sharpe_ratio', ascending=False)
        
        print("\nStrategy Performance Ranking:")
        print(comparison_df.round(2))
        
        # Find best strategy
        best_strategy = comparison_df.index[0]
        print(f"\n🏆 Best Performing Strategy: {best_strategy}")
        print(f"   Sharpe Ratio: {comparison_df.loc[best_strategy, 'sharpe_ratio']:.2f}")
        print(f"   Total Return: {comparison_df.loc[best_strategy, 'total_return']:.2f}%")
        print(f"   Max Drawdown: {comparison_df.loc[best_strategy, 'max_drawdown']:.2f}%")
        
        return comparison_df
    
    def create_strategy_visualizations(self):
        """Create visualizations for all strategies."""
        print("\nCreating strategy visualizations...")
        
        fig, axes = plt.subplots(2, 2, figsize=(16, 12))
        
        # 1. Portfolio Value Comparison
        ax1 = axes[0, 0]
        for strategy_name, strategy_df in self.strategies.items():
            ax1.plot(strategy_df['date'], strategy_df['portfolio_value'], 
                    label=strategy_name, linewidth=2)
        ax1.set_title('Portfolio Value Comparison', fontsize=14, fontweight='bold')
        ax1.set_xlabel('Date')
        ax1.set_ylabel('Portfolio Value ($)')
        ax1.legend()
        ax1.grid(True, alpha=0.3)
        
        # 2. Position Size Over Time
        ax2 = axes[0, 1]
        for strategy_name, strategy_df in self.strategies.items():
            ax2.plot(strategy_df['date'], strategy_df['position_size'], 
                    label=strategy_name, linewidth=2)
        ax2.set_title('Position Size Over Time', fontsize=14, fontweight='bold')
        ax2.set_xlabel('Date')
        ax2.set_ylabel('Position Size')
        ax2.legend()
        ax2.grid(True, alpha=0.3)
        
        # 3. Performance Metrics Bar Chart
        ax3 = axes[1, 0]
        strategies = list(self.results.keys())
        returns = [self.results[s]['total_return'] for s in strategies]
        sharpe_ratios = [self.results[s]['sharpe_ratio'] for s in strategies]
        
        x = np.arange(len(strategies))
        width = 0.35
        
        ax3.bar(x - width/2, returns, width, label='Total Return (%)', alpha=0.8)
        ax3_twin = ax3.twinx()
        ax3_twin.bar(x + width/2, sharpe_ratios, width, label='Sharpe Ratio', alpha=0.8, color='orange')
        
        ax3.set_title('Strategy Performance Metrics', fontsize=14, fontweight='bold')
        ax3.set_xlabel('Strategy')
        ax3.set_ylabel('Total Return (%)')
        ax3_twin.set_ylabel('Sharpe Ratio')
        ax3.set_xticks(x)
        ax3.set_xticklabels(strategies)
        ax3.legend(loc='upper left')
        ax3_twin.legend(loc='upper right')
        ax3.grid(True, alpha=0.3)
        
        # 4. Risk-Return Scatter
        ax4 = axes[1, 1]
        for strategy_name in strategies:
            volatility = self.results[strategy_name]['volatility']
            total_return = self.results[strategy_name]['total_return']
            ax4.scatter(volatility, total_return, s=200, label=strategy_name, alpha=0.7)
        
        ax4.set_title('Risk-Return Profile', fontsize=14, fontweight='bold')
        ax4.set_xlabel('Volatility (%)')
        ax4.set_ylabel('Total Return (%)')
        ax4.legend()
        ax4.grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.savefig('/Users/sohamajmera/Desktop/primetradetask/advanced_trading_strategies.png', 
                   dpi=300, bbox_inches='tight')
        plt.show()
        
        print("Strategy visualizations saved as 'advanced_trading_strategies.png'")
    
    def generate_trading_signals(self):
        """Generate actionable trading signals based on analysis."""
        print("\n" + "="*60)
        print("TRADING SIGNALS GENERATION")
        print("="*60)
        
        # Current sentiment analysis
        latest_data = self.data.iloc[-1]
        current_sentiment = latest_data['sentiment_score']
        current_category = latest_data['sentiment_category']
        
        print(f"\n📊 CURRENT MARKET CONDITIONS:")
        print(f"   • Sentiment Score: {current_sentiment:.1f}")
        print(f"   • Sentiment Category: {current_category}")
        print(f"   • Recent Performance: ${latest_data['total_pnl']:,.2f}")
        
        # Generate signals
        signals = {}
        
        if current_sentiment <= 30:
            signals['action'] = "STRONG BUY"
            signals['confidence'] = "HIGH"
            signals['reason'] = "Extreme Fear - Contrarian Opportunity"
            signals['position_size'] = "80-100%"
        elif current_sentiment <= 45:
            signals['action'] = "BUY"
            signals['confidence'] = "MEDIUM"
            signals['reason'] = "Fear - Good Entry Point"
            signals['position_size'] = "60-80%"
        elif current_sentiment <= 55:
            signals['action'] = "HOLD"
            signals['confidence'] = "LOW"
            signals['reason'] = "Neutral - Wait for Clear Direction"
            signals['position_size'] = "40-60%"
        elif current_sentiment <= 75:
            signals['action'] = "SELL"
            signals['confidence'] = "MEDIUM"
            signals['reason'] = "Greed - Take Profits"
            signals['position_size'] = "20-40%"
        else:
            signals['action'] = "STRONG SELL"
            signals['confidence'] = "HIGH"
            signals['reason'] = "Extreme Greed - Risk Management"
            signals['position_size'] = "10-20%"
        
        print(f"\n🎯 TRADING SIGNAL:")
        print(f"   • Action: {signals['action']}")
        print(f"   • Confidence: {signals['confidence']}")
        print(f"   • Reason: {signals['reason']}")
        print(f"   • Recommended Position Size: {signals['position_size']}")
        
        # Risk management recommendations
        print(f"\n⚠️  RISK MANAGEMENT:")
        if current_sentiment <= 30:
            print(f"   • Stop Loss: 15% (Fear periods allow wider stops)")
            print(f"   • Take Profit: 50% (High profit potential)")
        elif current_sentiment >= 70:
            print(f"   • Stop Loss: 6% (Tight risk control)")
            print(f"   • Take Profit: 20% (Quick profit taking)")
        else:
            print(f"   • Stop Loss: 10% (Standard risk management)")
            print(f"   • Take Profit: 30% (Balanced approach)")
        
        return signals
    
    def run_complete_analysis(self):
        """Run complete advanced trading strategy analysis."""
        print("🚀 Starting Advanced Trading Strategy Analysis")
        print("="*60)
        
        # Implement strategies
        self.contrarian_strategy()
        self.sentiment_momentum_strategy()
        self.risk_parity_strategy()
        
        # Compare strategies
        comparison = self.compare_strategies()
        
        # Create visualizations
        self.create_strategy_visualizations()
        
        # Generate trading signals
        signals = self.generate_trading_signals()
        
        print("\n✅ Advanced trading strategy analysis completed!")
        
        return {
            'strategies': self.strategies,
            'results': self.results,
            'comparison': comparison,
            'signals': signals
        }

def main():
    """Main execution function."""
    # Load the merged data from previous analysis
    try:
        # Try to load pre-processed data
        merged_data = pd.read_csv('/Users/sohamajmera/Desktop/primetradetask/merged_data.csv')
        merged_data['date'] = pd.to_datetime(merged_data['date'])
    except FileNotFoundError:
        print("Merged data not found. Please run the main analysis first.")
        return None
    
    # Initialize advanced strategies
    strategies = AdvancedTradingStrategies(merged_data)
    
    # Run complete analysis
    results = strategies.run_complete_analysis()
    
    return results

if __name__ == "__main__":
    results = main()
