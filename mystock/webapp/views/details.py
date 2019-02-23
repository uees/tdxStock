# -*- coding: utf-8 -*-
from flask import Blueprint, render_template, request
from mongoengine import Q

from webapp.collection import current_year
from webapp.common import mongo_to_dataframe
from webapp.models.stock import (CashflowData, ConceptClassified,
                                 DebtpayingData, Distribution, Forecast,
                                 FundHolding, OperationData, ProfitData,
                                 ReportData, StockBasic, Xsg)

details = Blueprint('details', __name__)


@details.route("/stocks")
def stocks():
    page = request.args.get('p', type=int, default=1)
    q = Q()

    keyworld = request.args.get('q', '')
    if keyworld:
        for key in keyworld.split(" "):
            q &= (Q(name__icontains=key) or Q(code__contains=key) or
                  Q(area__icontains=key) or Q(industry__icontains=key))

    industry = request.args.get('industry')
    if industry:
        q &= Q(industry=industry)

    area = request.args.get('area')
    if area:
        q &= Q(area=area)

    page_obj = StockBasic.objects(q).paginate(page=page, per_page=50)

    concept = request.args.get('concept')
    if concept:
        page_obj = ConceptClassified.objects(
            c_name=concept).paginate(page=page, per_page=50)

    return render_template('details/stocks.html', page=page_obj)


@details.route("/stocks/<code>")
def stock(code):
    stock = StockBasic.objects(code=code).first_or_404()
    report_data = mongo_to_dataframe(ReportData.objects(code=code))
    profit_data = mongo_to_dataframe(ProfitData.objects(code=code))
    operation_data = mongo_to_dataframe(OperationData.objects(code=code))
    debtpaying_data = mongo_to_dataframe(DebtpayingData.objects(code=code))
    cashflow_data = mongo_to_dataframe(CashflowData.objects(code=code))

    distributions = Distribution.objects(code=code).all()
    forecasts = Forecast.objects(code=code).all()
    xsg_unban = Xsg.objects(code=code).all()
    funds = FundHolding.objects(code=code).all()

    return render_template('details/stock.html',
                           current_year=current_year,
                           stock=stock,
                           report_data=report_data,
                           profit_data=profit_data,
                           operation_data=operation_data,
                           debtpaying_data=debtpaying_data,
                           cashflow_data=cashflow_data,
                           distributions=distributions,
                           forecasts=forecasts,
                           xsg_unban=xsg_unban,
                           funds=funds)
