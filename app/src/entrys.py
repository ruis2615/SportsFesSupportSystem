import datetime
import json

from flask import render_template, url_for, redirect, request, Blueprint
from flask_login import current_user, login_required

from .db import GetData, SQL

entrys_module = Blueprint("entrys", __name__, url_prefix="/entrys")


@entrys_module.route("/", methods=["GET"])
@login_required
def entrys():
    if current_user.permission == "all_prtmissions":
        entrys = GetData.get_fetchall(f"SELECT entrys.entry_id, schedules.schedule_id, schedules.schedule_name, teams.team_id, teams.team_name, CASE WHEN entrys.schedule_id IS NOT NULL THEN 'エントリー済' ELSE '未エントリー' END AS has_entry, TO_CHAR(entrys.entry_created_at, 'YYYY/MM/DD HH24:MI'), TO_CHAR(entrys.entry_updated_at, 'YYYY/MM/DD HH24:MI') FROM schedules CROSS JOIN teams LEFT JOIN entrys ON teams.team_id = entrys.team_id AND schedules.schedule_id = entrys.schedule_id WHERE schedules.schedule_type != 0 ORDER BY schedules.schedule_number, teams.team_name")
        return render_template("pages/entry/entry.html", entrys=entrys)
    else:
        entrys = GetData.get_fetchall(f"SELECT entrys.entry_id, schedules.schedule_id, schedules.schedule_number, schedules.schedule_name, teams.team_id, CASE WHEN entrys.schedule_id IS NOT NULL THEN 'エントリー済' ELSE '未エントリー' END AS has_entry, TO_CHAR(entrys.entry_created_at, 'YYYY/MM/DD HH24:MI'), TO_CHAR(entrys.entry_updated_at, 'YYYY/MM/DD HH24:MI') FROM schedules LEFT JOIN teams ON teams.team_login_id = '{current_user.name}' LEFT JOIN entrys ON schedules.schedule_id = entrys.schedule_id AND entrys.team_id = (SELECT teams.team_id FROM teams WHERE teams.team_login_id = '{current_user.name}') WHERE schedules.schedule_type != 0 ORDER BY schedules.schedule_id")
        entrys_status = GetData.get_fetchone(f"SELECT option_value FROM options WHERE option_name = 'master_options'")[0]["entry_status"]
        return render_template("pages/entry/entry.html", entrys=entrys, entrys_status=entrys_status)


@entrys_module.route("/add/<int:schedule_id>/<int:team_id>", methods=["GET", "POST"])
@login_required
def entry_add(schedule_id, team_id):
    if request.method == "GET":
        entrys_status = GetData.get_fetchone(f"SELECT option_value FROM options WHERE option_name = 'master_options'")[0]["entry_status"]
        entry_option = GetData.get_fetchone(f"SELECT schedule_name, schedule_type, schedule_option FROM schedules WHERE schedule_id = {schedule_id}")
        list_of_name = GetData.get_fetchall(f"SELECT id, number, name, gender, team_id FROM list_of_name WHERE team_id = {team_id}")
        if current_user.permission == "all_prtmissions":
            return render_template("pages/entry/entry_add.html", schedule_id=schedule_id, team_id=team_id, entry_option=entry_option, list_of_name=list_of_name)
        elif int(team_id) == int(current_user.name.split("-")[1]):
            if int(entrys_status) == 0:
                return render_template("pages/entry/entry_add.html", schedule_id=schedule_id, team_id=team_id, entry_option=entry_option, list_of_name=list_of_name)
        return redirect(url_for("entrys.entrys"))
    elif request.method == "POST":
        fetch_data = request.form.to_dict()
        SQL.sql(f"INSERT INTO entrys (team_id, schedule_id, entry, entry_created_at) VALUES ({team_id}, {schedule_id}, '{json.dumps(fetch_data)}', '{datetime.datetime.now()}')")
        return redirect(url_for("entrys.entrys"))


@entrys_module.route("/remove/<int:entry_id>")
@login_required
def entry_remove(entry_id):
    if current_user.permission == "all_prtmissions":
        SQL.sql(f"DELETE FROM entrys WHERE entry_id = {entry_id}")
        return redirect(url_for("entrys.entrys"))
    else:
        entrys_status = GetData.get_fetchone(f"SELECT option_value FROM options WHERE option_name = 'master_options'")[0]["entry_status"]
        if int(entrys_status) == 0:
            SQL.sql(f"DELETE FROM entrys WHERE entry_id = {entry_id} AND entrys.team_id = '{current_user.name.split('-')[1]}'")
        return redirect(url_for("entrys.entrys"))


@entrys_module.route("/edit/<int:entry_id>", methods=["GET", "POST"])
@login_required
def entry_edit(entry_id):
    if request.method == "GET":
        entrys_status = GetData.get_fetchone(f"SELECT option_value FROM options WHERE option_name = 'master_options'")[0]["entry_status"]
        entryed_team_id = GetData.get_fetchone(f"SELECT team_id FROM entrys WHERE entry_id = {entry_id}")
        entry = GetData.get_fetchone(f"SELECT entrys.entry_id, entrys.team_id, entrys.schedule_id, schedules.schedule_name, schedules.schedule_type, schedules.schedule_option, entrys.entry FROM entrys INNER JOIN schedules ON schedules.schedule_id = entrys.schedule_id WHERE entry_id = {entry_id}")
        list_of_name = GetData.get_fetchall(f"SELECT id, number, name, gender, team_id FROM list_of_name WHERE team_id = {entry[1]}")
        if current_user.permission == "all_prtmissions":
            return render_template("pages/entry/entry_edit.html", entry=entry, list_of_name=list_of_name)
        elif int(entryed_team_id[0]) == int(current_user.name.split("-")[1]):
            if int(entrys_status) == 0:
                return render_template("pages/entry/entry_edit.html", entry=entry, list_of_name=list_of_name)
        return redirect(url_for("entrys.entrys"))
    elif request.method == "POST":
        fetch_data = request.form.to_dict()
        SQL.sql(f"UPDATE entrys SET (entry, entry_updated_at) = ('{json.dumps(fetch_data)}', '{datetime.datetime.now()}') WHERE entry_id = {entry_id}")
        return redirect(url_for("entrys.entrys"))

