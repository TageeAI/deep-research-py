import yfinance as yf
import pandas as pd

def get_stock_data(ticker, date):
    try:
        # 创建股票对象
        stock = yf.Ticker(ticker)
        
        # 获取指定日期的数据
        # 为了确保能获取到数据，我们取一个日期范围（前一天到后一天）
        start_date = pd.to_datetime(date) - pd.Timedelta(days=1)
        end_date = pd.to_datetime(date) + pd.Timedelta(days=1)
        
        # 获取历史数据
        data = stock.history(start=start_date, end=end_date)
        
        # 筛选出指定日期的数据
        if date in data.index:
            specific_date_data = data.loc[date]
            price = specific_date_data['Close']  # 收盘价
            volume = specific_date_data['Volume']  # 成交量
            # yfinance不直接提供成交额，我们可以通过收盘价*成交量来估算
            turnover = price * volume
            
            print(f"股票代码: {ticker}")
            print(f"日期: {date}")
            print(f"收盘价: {price:.2f} USD")
            print(f"成交量: {volume:,.0f} 股")
            print(f"成交额: {turnover:,.2f} USD")
            
            return {
                'price': price,
                'volume': volume,
                'turnover': turnover
            }
        else:
            print(f"无法获取 {date} 的数据，可能是非交易日")
            return None
            
    except Exception as e:
        print(f"发生错误: {str(e)}")
        return None

import yfinance as yf

def get_analyst_target_price(stock_code):
    try:
        # 创建 Ticker 对象
        ticker = yf.Ticker(stock_code)
        
        # 获取股票信息
        info = ticker.info
        
        #print(info)
        # 提取分析师目标价
        target_price = info.get('targetMeanPrice')
        high_target_price = info.get('targetHighPrice')
        low_target_price = info.get('targetLowPrice')
        
        if target_price is None:
            return {}
            return f"没有找到 {stock_code} 的分析师目标价。"
        else:
            print(f"{stock_code} 的分析师目标价为: {target_price} , 最高价：{high_target_price} , 最低价：{low_target_price}")
            return {stock_code: [low_target_price, target_price, high_target_price]}
            return f"{stock_code} 的分析师目标价为: {target_price} , 最高价：{high_target_price} , 最低价：{low_target_price}"
    
    except Exception as e:
        return {}
        return f"获取 {stock_code} 的数据时出错: {e}"

