import datetime
import json
import re
import itertools

import psycopg2
from flask import render_template, url_for, redirect, request, Blueprint
from flask_login import current_user, login_required

from .db import GetData, SQL

absence_report_module = Blueprint("absence_report", __name__, url_prefix="/absence_report")


@absence_report_module.route("/")
@login_required
def absence_report():
    list_of_name = GetData.get_fetchall("SELECT id, number, name FROM list_of_name WHERE number SIMILAR TO '[0-9][a-zA-Z][0-9]{2}' ORDER BY number")
    absence_report_list = GetData.get_fetchall("SELECT primary_id FROM absence_report")

    return render_template("pages/absence_report/absence_report.html", list_of_name=list_of_name, absence_report_list=list(itertools.chain.from_iterable(absence_report_list)))


@absence_report_module.route("/add/<int:primary_id>", methods=["POST"])
@login_required
def absence_report_add(primary_id):
    SQL.sql(f"INSERT INTO absence_report (primary_id) VALUES ('{primary_id}')")
    return redirect(url_for("absence_report.absence_report"))


@absence_report_module.route("/delete/<int:primary_id>", methods=["POST"])
@login_required
def absence_report_delete(primary_id):
    SQL.sql(f"DELETE FROM absence_report WHERE primary_id = '{primary_id}'")
    return redirect(url_for("absence_report.absence_report"))
