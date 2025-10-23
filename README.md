# Bitcoin Market Sentiment & Trader Performance Analysis

##  Project Overview

This comprehensive analysis explores the relationship between Bitcoin market sentiment (Fear/Greed Index) and trader performance data from Hyperliquid to uncover patterns and deliver actionable insights for smarter trading strategies in the Web3 space.

##  Key Findings

- **Contrarian Opportunity**: Extreme Fear periods show highest average PnL ($49,496)
- **Volume Correlation**: Higher sentiment correlates with lower trading volume (-0.264)
- **Win Rate Insight**: Extreme Greed has highest win rate (47%) but lower total PnL
- **Market Efficiency**: 75.4% of trading days are profitable

##  Quick Start

### 1. Run Main Analysis
```bash
python bitcoin_sentiment_analysis.py
```

### 2. Run Advanced Strategies
```bash
python advanced_trading_strategies.py
```

### 3. View Results
- **Main Analysis**: `bitcoin_sentiment_analysis.png`
- **Strategy Comparison**: `advanced_trading_strategies.png`
- **Detailed Report**: `Bitcoin_Sentiment_Trading_Analysis_Report.md`

##  Project Structure

```
primetradetask/
├──  Data Files
│   ├── fear_greed_index.csv          # Bitcoin Fear/Greed Index (2018-2025)
│   ├── historical_data.csv           # Hyperliquid trading data (211K+ trades)
│   └── merged_data.csv               # Processed analysis dataset
│
├──  Analysis Scripts
│   ├── bitcoin_sentiment_analysis.py # Main analysis pipeline
│   └── advanced_trading_strategies.py # Strategy implementation & backtesting
│
├──  Visualizations
│   ├── bitcoin_sentiment_analysis.png # Comprehensive sentiment charts
│   └── advanced_trading_strategies.png # Strategy performance comparison
│
└──  Documentation
    ├── Bitcoin_Sentiment_Trading_Analysis_Report.md # Detailed analysis report
    ├── ANALYSIS_SUMMARY.md           # Executive summary
    └── README.md                     # This file
```

##  Trading Strategies Implemented

### 1. **Contrarian Strategy** (Best for High Returns)
- **Entry**: Sentiment ≤ 30 (Fear territory)
- **Position Size**: 80-100% allocation
- **Exit**: Sentiment ≥ 70 (Greed territory)
- **Performance**: Highest average PnL during fear periods

### 2. **Sentiment Momentum Strategy** (Best for Trend Following)
- **Entry**: 5-day sentiment decline
- **Position Size**: Dynamic based on momentum
- **Performance**: Sharpe Ratio 4.64

### 3. **Risk Parity Strategy** (Best Risk-Adjusted Returns)
- **Position Sizing**: Based on sentiment volatility
- **Performance**: Highest Sharpe Ratio (4.95)
- **Risk Management**: Adaptive based on market conditions

##  Key Metrics

| Metric | Value |
|--------|-------|
| **Total Trades Analyzed** | 211,218 |
| **Total Volume** | $1.19 billion |
| **Profitable Days** | 75.4% (361/479) |
| **Average Daily PnL** | $21,408 |
| **Best Strategy Sharpe Ratio** | 4.95 (Risk Parity) |

##  Sentiment-Performance Correlation

| Sentiment Category | Avg Daily PnL | Win Rate | Days | Strategy |
|-------------------|---------------|----------|------|----------|
| **Extreme Fear** | $49,496 | 34.0% | 22 | 🎯 **Strong Buy** |
| **Fear** | $36,519 | 33.0% | 87 | 📈 **Buy** |
| **Neutral** | $18,059 | 33.0% | 69 | ⏸️ **Hold** |
| **Greed** | $11,150 | 35.0% | 208 | 📉 **Sell** |
| **Extreme Greed** | $26,057 | 47.0% | 93 | ⚠️ **Strong Sell** |

##  Key Insights

### **Contrarian Opportunities**
- **Fear periods** offer the highest profit potential
- **Volume spikes** during fear indicate buying opportunities
- **Greed periods** show lowest performance - time to take profits

### **Risk Management**
- **Fear periods**: Wider stops (15%), higher profit targets (50%)
- **Greed periods**: Tighter stops (6%), quick profit taking (20%)
- **Neutral periods**: Standard risk management (10% stops, 30% targets)

### **Market Behavior**
- **Higher sentiment** = Lower trading volume (-0.264 correlation)
- **Fear periods** attract more traders (6.92-10.55 avg)
- **Greed periods** show reduced participation (3.44-4.68 avg)

##  Implementation Guide

### **Daily Trading Routine**
1. **Morning**: Check sentiment score
2. **Intraday**: Monitor volume patterns  
3. **Position Sizing**: Adjust based on sentiment
4. **Risk Management**: Continuous monitoring

### **Key Metrics to Track**
- Sentiment score trends (5-day moving average)
- Volume patterns during different sentiment periods
- Win rates by sentiment category
- Risk-adjusted returns

##  Current Market Signal

**Latest Analysis Results:**
- **Sentiment Score**: 53.0 (Neutral)
- **Recommended Action**: HOLD
- **Position Size**: 40-60%
- **Risk Management**: 10% stop-loss, 30% take-profit

##  Technical Requirements

- **Python 3.7+**
- **Pandas, NumPy, Matplotlib, Seaborn**
- **Jupyter Notebook** (optional for interactive analysis)

##  Documentation

- **[Detailed Analysis Report](Bitcoin_Sentiment_Trading_Analysis_Report.md)** - Comprehensive findings and recommendations
- **[Analysis Summary](ANALYSIS_SUMMARY.md)** - Executive summary and key insights
- **[Main Analysis Script](bitcoin_sentiment_analysis.py)** - Core analysis pipeline
- **[Advanced Strategies](advanced_trading_strategies.py)** - Strategy implementation and backtesting

##  Results

This analysis successfully demonstrates the power of combining market sentiment data with trader performance metrics to develop sophisticated trading strategies. The key insight that **Extreme Fear periods offer the highest profit potential** while **Greed periods show the lowest performance** provides a clear contrarian framework for Web3 trading.

**The Risk Parity strategy achieving the highest Sharpe ratio of 4.95** showcases the practical application of sentiment-based trading in the cryptocurrency markets.

---

*Analysis completed for the Junior Data Scientist position at PrimeTrade.ai*

**Contact**: For questions about this analysis, please refer to the detailed documentation or review the analysis scripts.
