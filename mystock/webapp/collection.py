# -*- coding:utf-8 -*-
'''
Created on 2015年10月4日

@author: Wan
'''
import time
from datetime import datetime, timedelta

import tushare as ts
from flask import current_app

from webapp.models.option import Option
from webapp.models.stock import (AreaClassified, CashflowData,
                                 ConceptClassified, Cpi, DebtpayingData,
                                 DepositRate, Distribution, Forecast,
                                 FundHolding, GdpContrib, GdpFor, GdpPull,
                                 GdpQuarter, GdpYear, GemClassified,
                                 GrowthData, Hs300, IndustryClassified,
                                 LoanRate, MoneySupply, MoneySupplyBal,
                                 OperationData, Ppi, ProfitData, ReportData,
                                 Rrr, ShMargin, ShMarginDetail, SmeClassified,
                                 StClassified, StockBasic, Suspended, Sz50,
                                 SzMargin, SzMarginDetail, Terminated, Xsg,
                                 Zz500)

current_year = time.localtime().tm_year
current_month = time.localtime().tm_mon
current_day = time.localtime().tm_mday


def collect_no_args():
    '''无参数采集
    yes = []'''
    models = [IndustryClassified, ConceptClassified, AreaClassified,
              SmeClassified, GemClassified, StClassified, Hs300,
              Sz50, Zz500, Terminated, Suspended, StockBasic,
              DepositRate, LoanRate, Rrr, MoneySupply,
              MoneySupplyBal, GdpYear, GdpQuarter, GdpFor,
              GdpPull, GdpContrib, Cpi, Ppi]

    for model in models:
        model.objects.delete()
        fetch_api(model, {})


def collect_with_quarter(start_year, stop_year):
    """按季度采集 yes=[]"""
    models = [ReportData, ProfitData, OperationData,
              GrowthData, DebtpayingData, CashflowData,
              Forecast, FundHolding]
    for model in models:
        if model is GrowthData and start_year < 2002:  # 2002年前的数据采集不到
            start_year = 2002
        for year in range(start_year, stop_year + 1):
            for quarter in range(1, 5):
                fetch_by_quarter(model, year, quarter)


'''
def forecast_data():
    fetch_by_quarter(Forecast, year=2009, quarter=4)
    for year in range(2010, 2017):
        for quarter in range(1, 5):
            fetch_by_quarter(Forecast, year, quarter)'''


def collect_with_month(start_year, stop_year):
    """按月采集"""
    models = [Xsg]
    for model in models:
        for year in range(start_year, stop_year + 1):
            for month in range(1, 13):
                fetch_by_month(model, year, month)


def collect_margins():
    """融资融券汇总数据"""
    kwrds = {"start": "2010-01-01", "end": "2017-02-22"}
    fetch_api(ShMargin, kwrds)

    for year in range(2010, 2017):
        start = '{}-01-01'.format(year)
        end = '{}-12-31'.format(year)
        kwrds = dict(start=start, end=end)
        fetch_api(SzMargin, kwrds)

    kwrds = dict(start='2017-01-01',
                 end="2017-02-22")
    fetch_api(SzMargin, kwrds)


def collect_sh_margin_details():
    """融资融券沪市明细"""
    for year in range(2010, 2017):
        start = '{}-01-01'.format(year)
        end = '{}-12-31'.format(year)
        kwrds = dict(start=start, end=end)
        fetch_api(ShMarginDetail, kwrds)

    kwrds = dict(start='2017-01-01',
                 end="2017-02-22")
    fetch_api(ShMarginDetail, kwrds)


def collect_sz_margin_details():
    """融资融券深市明细"""
    start = datetime(2010, 1, 1)
    end = datetime(2017, 2, 22)
    for day in date_range(start, end):
        kwrds = dict(date=day.strftime("%Y-%m-%d"))
        fetch_api(SzMarginDetail, kwrds)


def collect_profit_data(year, top):
    '''采集分配预案数据到数据库'''
    kwrds = {"year": year, "top": top}
    fetch_api(Distribution, kwrds)


'''
def fix_stock_basics_code():
    for stock in StockBasic.objects.all():
        rs = AreaClassified.objects(name=stock.name).first()
        stock.code = rs.code
        stock.save()'''


def set_last_date(api_name):
    '''设置 tushare api 最后调用的时间'''
    op = Option.objects(name="last_date({})".format(api_name)).first()
    if op:
        op.value = datetime.utcnow()
    else:
        op = Option(name="last_date({})".format(api_name),
                    value=datetime.utcnow(),
                    note="上次调用'{}'的日期".format(api_name))
    op.save()


def fetch_by_month(model, year, month):
    tsfunc = model.__tsfunc__
    kwrds = {"year": year, "month": month}

    if year > current_year or (year == current_year
                               and month >= current_month):
        return print("sorry, wo bu neng yu ce wei lai.")

    df = ts_request(tsfunc, kwrds=kwrds)
    if df is not None:
        df['month'] = month
        df['year'] = year
        for ix, row in df.iterrows():
            model(**dict(row)).save()

        current_app.logger.info('ts.{func}({kwrds}) done.'.format(
            func=tsfunc, kwrds=repr(kwrds)))


def fetch_by_quarter(model, year, quarter):
    tsfunc = model.__tsfunc__
    kwrds = {"year": year, "quarter": quarter}
    current_year = time.localtime().tm_year
    current_quarter = time.localtime().tm_mon // 3 + 1

    if year > current_year or (year == current_year
                               and quarter >= current_quarter):
        return print("sorry, wo bu neng yu ce wei lai.")

    df = ts_request(tsfunc, kwrds=kwrds)
    if df is not None:
        df['quarter'] = quarter
        df['year'] = year
        # df.to_sql(table.name, db.engine, if_exists="append", index=False)

        # for ix, row in df.iterrows():
        #     model(**dict(row)).save()
        # df = df.reset_index()
        records = model.objects.from_json(df.to_json(orient='records'))
        model.objects.insert(records)

        current_app.logger.info('ts.{func}({kwrds}) done.'.format(
            func=tsfunc, kwrds=repr(kwrds)))


def fetch_api(model, kwrds):
    '''调用api存入数据库'''
    df = ts_request(model.__tsfunc__, kwrds=kwrds)
    if df is not None:
        for ix, row in df.iterrows():
            model(**dict(row)).save()
        # df = df.reset_index()
        # records = model.objects.from_json(df.to_json(orient='records'))
        # model.objects.insert(records)

        current_app.logger.info('ts.{func}({kwrds}) done.'.format(
            func=model.__tsfunc__, kwrds=repr(kwrds)))


def ts_request(tsfunc, kwrds={}, retry_count=4, pause=5):
    '''发起 tushare api 请求'''
    _times = 1
    df = None
    while True:
        df = getattr(ts, tsfunc)(**kwrds)
        if df is not None:
            break
        else:  # time out
            if _times > retry_count:
                current_app.logger.error(
                    'ts.{func}() time out {times} times! kwgs: {kwrds}'.format(
                        func=tsfunc, times=retry_count, kwrds=repr(kwrds)))
                break
            _times += 1
            time.sleep(pause)
    return df


def date_range(start_date, end_date):
    for n in range(int((end_date - start_date).days)):
        yield start_date + timedelta(n)
