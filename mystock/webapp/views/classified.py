# -*- coding: utf-8 -*-
'''
Created on 2016-12-14

@author: Wan
'''
from flask import Blueprint, render_template, request

from webapp.extensions import cache
from webapp.models.stock import (ConceptClassified, GemClassified, Hs300,
                                 SmeClassified, StClassified, StockBasic, Sz50,
                                 Terminated, Zz500)


classified = Blueprint('classified', __name__)


@classified.route("/industries")
def industries():
    industries = cache.get("industries")
    if industries is None:
        industries = StockBasic.objects\
            .only("industry").distinct(field="industry")

    return render_template('classified/industries.html', industries=industries)


@classified.route("/concepts")
def concepts():
    concepts = cache.get("concepts")
    if concepts is None:
        concepts = ConceptClassified.objects\
            .only("c_name").distinct(field="c_name")
    return render_template('classified/concepts.html', concepts=concepts)


@classified.route("/area")
def area():
    area = cache.get("area")
    if area is None:
        area = StockBasic.objects\
            .only("area").distinct(field="area")
    return render_template('classified/area.html', area=area)


@classified.route("/sme")
def sme():
    page = request.args.get('p', type=int, default=1)
    page_obj = SmeClassified.objects.paginate(page=page, per_page=50)
    return render_template('classified/list.html',
                           page=page_obj,
                           endpoint="classified.sme")


@classified.route("/gem")
def gem():
    page = request.args.get('p', type=int, default=1)
    page_obj = GemClassified.objects.paginate(page=page, per_page=50)
    return render_template('classified/list.html',
                           page=page_obj,
                           endpoint="classified.gem")


@classified.route("/hs300")
def hs300():
    page = request.args.get('p', type=int, default=1)
    page_obj = Hs300.objects.paginate(page=page, per_page=50)
    return render_template('classified/list.html',
                           page=page_obj,
                           endpoint="classified.hs300")


@classified.route("/sz50")
def sz50():
    page = request.args.get('p', type=int, default=1)
    page_obj = Sz50.objects.paginate(page=page, per_page=50)
    return render_template('classified/list.html',
                           page=page_obj,
                           endpoint="classified.sz50")


@classified.route("/zz500")
def zz500():
    page = request.args.get('p', type=int, default=1)
    page_obj = Zz500.objects.paginate(page=page, per_page=50)
    return render_template('classified/list.html',
                           page=page_obj,
                           endpoint="classified.zz500")


@classified.route("/st")
def st():
    page = request.args.get('p', type=int, default=1)
    page_obj = StClassified.objects.paginate(page=page, per_page=50)
    return render_template('classified/list.html',
                           page=page_obj,
                           endpoint="classified.st")


@classified.route("/terminated")
def terminated():
    page = request.args.get('p', type=int, default=1)
    page_obj = Terminated.objects.paginate(page=page, per_page=50)
    return render_template('classified/list.html',
                           page=page_obj,
                           endpoint="classified.terminated")
