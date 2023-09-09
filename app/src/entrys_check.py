import datetime
import itertools
import json

import psycopg2
from flask import render_template, url_for, redirect, request, Blueprint
from flask_login import current_user, login_required

from .db import GetData, SQL

entrys_check_module = Blueprint("entrys_check", __name__, url_prefix="/entrys-check")


@entrys_check_module.route("/")
@login_required
def entrys_check():
    if current_user.permission == "all_prtmissions":
        entrys = GetData.get_fetchall(f"SELECT entrys.entry_id, schedules.schedule_id, schedules.schedule_name, teams.team_id, teams.team_name, CASE WHEN entrys.schedule_id IS NOT NULL THEN 'エントリー済' ELSE '未エントリー' END AS has_entry, TO_CHAR(entrys.entry_created_at, 'YYYY/MM/DD HH24:MI'), TO_CHAR(entrys.entry_updated_at, 'YYYY/MM/DD HH24:MI') FROM schedules CROSS JOIN teams LEFT JOIN entrys ON teams.team_id = entrys.team_id AND schedules.schedule_id = entrys.schedule_id WHERE schedules.schedule_type != 0 ORDER BY schedules.schedule_number, teams.team_name")
        return render_template("pages/entrys_check/entrys_check.html", entrys=entrys)
    else:
        entrys = GetData.get_fetchall(f"SELECT entrys.entry_id, schedules.schedule_id, schedules.schedule_number, schedules.schedule_name, teams.team_id, CASE WHEN entrys.schedule_id IS NOT NULL THEN 'エントリー済' ELSE '未エントリー' END AS has_entry, TO_CHAR(entrys.entry_created_at, 'YYYY/MM/DD HH24:MI'), TO_CHAR(entrys.entry_updated_at, 'YYYY/MM/DD HH24:MI') FROM schedules LEFT JOIN teams ON teams.team_login_id = '{current_user.name}' LEFT JOIN entrys ON schedules.schedule_id = entrys.schedule_id AND entrys.team_id = (SELECT teams.team_id FROM teams WHERE teams.team_login_id = '{current_user.name}') WHERE schedules.schedule_type != 0 ORDER BY schedules.schedule_id")
        entrys_status = GetData.get_fetchone(f"SELECT option_value FROM options WHERE option_name = 'master_options'")[0]["entry_status"]
        return render_template("pages/entrys_check/entrys_check.html", entrys=entrys, entrys_status=entrys_status)


@entrys_check_module.route("/preview/<int:schedule_id>/<int:team_id>")
@login_required
def entry_preview(schedule_id, team_id):
    entry_data = GetData.get_fetchone(f"SELECT schedules.schedule_name, schedules.schedule_type, schedules.schedule_option, entrys.entry FROM entrys JOIN schedules ON entrys.schedule_id = schedules.schedule_id WHERE entrys.schedule_id = '{schedule_id}' AND entrys.team_id = '{team_id}' ORDER BY schedules.schedule_number")
    absence_report_list = GetData.get_fetchall(f"SELECT list_of_name.number FROM list_of_name INNER JOIN absence_report ON absence_report.primary_id = list_of_name.id ")
    for key, value in entry_data[3].items():
        try:
            entry_info = GetData.get_fetchone(
                f"SELECT list_of_name.number, list_of_name.name, list_of_name.gender FROM list_of_name WHERE id = '{value}'")
        except psycopg2.Error:
            entry_info = (None, None)

        entry_data[3][key] = {
            "number": f"{entry_info[0]}",
            "name": f"{entry_info[1]}"
        }
    if current_user.permission == "all_prtmissions":
        return render_template("pages/entrys_check/entry_check.html", entry_data=entry_data, absence_report_list=list(itertools.chain.from_iterable(absence_report_list)))
    elif int(team_id) == int(current_user.name.split("-")[1]):
        return render_template("pages/entrys_check/entry_check.html", entry_data=entry_data, absence_report_list=list(itertools.chain.from_iterable(absence_report_list)))
    else:
        return redirect(url_for("entrys_check.entrys_check"))
