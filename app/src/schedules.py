import json

from flask import render_template, url_for, redirect, request, Blueprint
from flask_login import current_user, login_required

from .db import GetData, SQL

schedules_module = Blueprint("schedules", __name__, url_prefix="/schedules")


@schedules_module.route("/")
@login_required
def schedules():
    if current_user.permission == "all_prtmissions":
        schedules = GetData.get_fetchall("SELECT schedules.schedule_id, schedules.schedule_number, schedules.schedule_name, schedules.schedule_type, MAX(teams.team_name) AS team_name, MAX(TO_CHAR(schedules.schedule_started_at, 'HH24:MI')) AS schedule_started_at, MAX(TO_CHAR(schedules.schedule_ended_at, 'HH24:MI')) AS schedule_ended_at FROM schedules LEFT JOIN scores ON schedules.schedule_id = scores.schedule_id LEFT JOIN teams ON scores.team_id = teams.team_id AND scores.score = (SELECT MAX(scores.score) FROM scores WHERE scores.schedule_id = schedules.schedule_id AND scores.team_id IS NOT NULL) GROUP BY schedules.schedule_id, schedules.schedule_number, schedules.schedule_name, schedules.schedule_type ORDER BY schedules.schedule_number")
        return render_template("pages/schedules/schedules.html", schedules=schedules)
    return redirect(url_for("app.index"))


@schedules_module.route("/add", methods=["GET", "POST"])
@login_required
def schedules_add():
    if current_user.permission == "all_prtmissions":
        if request.method == "GET":
            return render_template("pages/schedules/schedules_add.html")

        elif request.method == "POST":
            # 共通項目の取得
            schedule_name = request.form.get("ScheduleName")
            schedule_number = request.form.get("ScheduleNumber")
            schedule_type = request.form.get("ScheduleType")
            schedule_started_at = request.form.get("ScheduleStartedAt")
            schedule_ended_at = request.form.get("ScheduleEndedAt")

            # 「競技(男女)」の場合
            if schedule_type == "1":
                appearance_count = request.form.get("AppearanceCount")
                reserve_count = request.form.get("ReserveCount")
                race_number = request.form.get("RaceNumber")

                format_data = {
                    "RaceNumber": race_number,
                    "AppearanceCount": appearance_count,
                    "ReserveCount": reserve_count,
                }

                SQL.sql(f"INSERT INTO schedules (schedule_number, schedule_name, schedule_type, schedule_option, schedule_started_at, schedule_ended_at) VALUES ('{schedule_number}', '{schedule_name}', '{schedule_type}', '{json.dumps(format_data)}', '{schedule_started_at}', '{schedule_ended_at}')")
                return redirect(url_for("schedules.schedules"))

            # 「競技(男女別)」の場合
            elif schedule_type == "2":
                appearance_count_male = request.form.get("AppearanceCountMale")
                reserve_count_male = request.form.get("ReserveCountMale")
                appearance_count_female = request.form.get("AppearanceCountFemale")
                reserve_count_female = request.form.get("ReserveCountFemale")
                race_number = request.form.get("RaceNumber")

                format_data = {
                    "RaceNumber": race_number,
                    "Male": {
                        "AppearanceCount": appearance_count_male,
                        "ReserveCount": reserve_count_male
                    },
                    "Female": {
                        "AppearanceCount": appearance_count_female,
                        "ReserveCount": reserve_count_female
                    }
                }

                SQL.sql(f"INSERT INTO schedules (schedule_number, schedule_name, schedule_type, schedule_option, schedule_started_at, schedule_ended_at) VALUES ('{schedule_number}', '{schedule_name}', '{schedule_type}', '{json.dumps(format_data)}', '{schedule_started_at}', '{schedule_ended_at}')")
                return redirect(url_for("schedules.schedules"))

            SQL.sql(f"INSERT INTO schedules (schedule_number, schedule_name, schedule_type, schedule_started_at, schedule_ended_at) VALUES ('{schedule_number}', '{schedule_name}', '{schedule_type}', '{schedule_started_at}', '{schedule_ended_at}')")
            return redirect(url_for("schedules.schedules"))
    return redirect(url_for("app.index"))


@schedules_module.route("/remove/<int:schedule_id>", methods=["GET"])
@login_required
def schedules_remove(schedule_id):
    if current_user.permission == "all_prtmissions":
        SQL.sql(f"DELETE FROM schedules WHERE schedule_id = {schedule_id}")
        SQL.sql(f"DELETE FROM scores WHERE schedule_id = {schedule_id}")
        return redirect(url_for("schedules.schedules"))
    return redirect(url_for("app.index"))


@schedules_module.route("/edit/<int:schedule_id>", methods=["GET", "POST"])
@login_required
def schedules_edit(schedule_id):
    if current_user.permission == "all_prtmissions":
        if request.method == "GET":
            schedule = GetData.get_fetchone(f"SELECT schedule_id, schedule_name, schedule_number, schedule_type, schedule_option, schedule_started_at, schedule_ended_at FROM schedules WHERE schedule_id = {schedule_id}")
            return render_template("pages/schedules/schedules_edit.html", schedule=schedule)

        elif request.method == "POST":
            schedule_name = request.form.get("ScheduleName")
            schedule_number = request.form.get("ScheduleNumber")
            schedule_type = request.form.get("ScheduleType")
            schedule_started_at = request.form.get("ScheduleStartedAt")
            schedule_ended_at = request.form.get("ScheduleEndedAt")

            # 「競技(男女)」の場合
            if schedule_type == "1":
                appearance_count = request.form.get("AppearanceCount")
                reserve_count = request.form.get("ReserveCount")
                race_number = request.form.get("RaceNumber")

                format_data = {
                    "RaceNumber": race_number,
                    "AppearanceCount": appearance_count,
                    "ReserveCount": reserve_count,
                }

                SQL.sql(f"UPDATE schedules SET (schedule_name, schedule_number, schedule_type, schedule_option, schedule_started_at, schedule_ended_at) = ('{schedule_name}', '{schedule_number}', '{schedule_type}', '{json.dumps(format_data)}', '{schedule_started_at}', '{schedule_ended_at}') WHERE schedule_id = {schedule_id}")
                return redirect(url_for("schedules.schedules"))

            # 「競技(男女別)」の場合
            elif schedule_type == "2":
                appearance_count_male = request.form.get("AppearanceCountMale")
                reserve_count_male = request.form.get("ReserveCountMale")
                appearance_count_female = request.form.get("AppearanceCountFemale")
                reserve_count_female = request.form.get("ReserveCountFemale")
                race_number = request.form.get("RaceNumber")

                format_data = {
                    "RaceNumber": race_number,
                    "Male": {
                        "AppearanceCount": appearance_count_male,
                        "ReserveCount": reserve_count_male
                    },
                    "Female": {
                        "AppearanceCount": appearance_count_female,
                        "ReserveCount": reserve_count_female
                    }
                }

                SQL.sql(f"UPDATE schedules SET (schedule_name, schedule_number, schedule_type, schedule_option, schedule_started_at, schedule_ended_at) = ('{schedule_name}', '{schedule_number}', '{schedule_type}', '{json.dumps(format_data)}', '{schedule_started_at}', '{schedule_ended_at}') WHERE schedule_id = {schedule_id}")
                return redirect(url_for("schedules.schedules"))

            SQL.sql(f"UPDATE schedules SET (schedule_name, schedule_number, schedule_type, schedule_started_at, schedule_ended_at) = ('{schedule_name}', '{schedule_number}', '{schedule_type}', '{schedule_started_at}', '{schedule_ended_at}') WHERE schedule_id = {schedule_id}")
            return redirect(url_for("schedules.schedules"))
    return redirect(url_for("app.index"))