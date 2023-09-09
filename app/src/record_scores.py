import collections
import datetime

from flask import render_template, url_for, redirect, request, Blueprint
from flask_login import login_required

from .db import GetData, SQL


record_scores_module = Blueprint("record_scores", __name__, url_prefix="/record_scores")


@record_scores_module.route("/")
@login_required
def record_scores():
    scores = GetData.get_fetchall("SELECT schedules.schedule_id, schedules.schedule_number, schedules.schedule_name, schedules.schedule_option, CASE WHEN scores.schedule_id IS NULL THEN NULL ELSE 1 END AS match_flag, MAX(TO_CHAR(scores.score_created_at, 'HH24:MI')) AS score_created_at, MAX(TO_CHAR(scores.score_updated_at, 'HH24:MI')) AS score_updated_at FROM schedules LEFT JOIN scores ON schedules.schedule_id = scores.schedule_id WHERE schedules.schedule_type = 1 OR schedules.schedule_type = 2 GROUP BY schedules.schedule_id, scores.schedule_id, schedules.schedule_number, schedules.schedule_name, schedules.schedule_option, match_flag ORDER BY schedules.schedule_number")
    return render_template("pages/record_scores/record_scores.html", scores=scores)


@record_scores_module.route("/add/<int:schedule_id>", methods=["GET", "POST"])
@login_required
def record_scores_add(schedule_id):
    schedule = GetData.get_fetchone(f"SELECT schedules.schedule_id, schedules.schedule_name, schedules.schedule_type, schedules.schedule_option FROM schedules WHERE schedule_id = {schedule_id}")
    teams = GetData.get_fetchall(f"SELECT teams.team_id, teams.team_name FROM teams ORDER BY teams.team_name ASC")
    if request.method == "GET":
        return render_template("pages/record_scores/record_scores_add.html", schedule=schedule, teams=teams)

    elif request.method == "POST":
        fetch_data = request.form.to_dict()

        for key, value in fetch_data.items():
            if len(key.split("-")) == 2:
                gender = 0  # 全て

            elif len(key.split("-")) == 3:
                if key.split("-")[2] == "Male":
                    gender = 1  # 男性
                elif key.split("-")[2] == "Female":
                    gender = 2  # 女性

            team_id = key.replace("Team", "").split("-")[0]
            race_number = key.replace("Team", "").split("-")[1]
            SQL.sql(f"INSERT INTO scores (schedule_id, team_id, race_number, race_gender, score, score_created_at) VALUES ({schedule_id}, {team_id}, {race_number}, {gender}, {value}, '{datetime.datetime.now()}')")

        return redirect(url_for("record_scores.record_scores"))


@record_scores_module.route("/remove/<int:schedule_id>")
@login_required
def record_score_remove(schedule_id):
    SQL.sql(f"DELETE FROM scores WHERE schedule_id = {schedule_id}")
    return redirect(url_for("record_scores.record_scores"))


@record_scores_module.route("/edit/<int:schedule_id>", methods=["GET", "POST"])
@login_required
def record_score_edit(schedule_id):
    schedule = GetData.get_fetchone(f"SELECT schedules.schedule_id, schedules.schedule_name, schedules.schedule_type, schedules.schedule_option FROM schedules WHERE schedule_id = {schedule_id}")
    scores = GetData.get_fetchall(f"SELECT scores.score_id, scores.team_id, teams.team_name, race_number, race_gender, scores.score FROM scores JOIN teams ON scores.team_id = teams.team_id WHERE schedule_id = {schedule_id} ORDER BY scores.score_id")

    format_score_data = collections.defaultdict(lambda: collections.defaultdict(list))

    for score in scores:
        format_score_data[f"{score[3]}"][f"{score[4]}"].append(list(score))

    if request.method == "GET":
        return render_template("pages/record_scores/record_scores_edit.html", schedule=schedule, scores=dict(format_score_data))

    elif request.method == "POST":
        fetch_data = request.form.to_dict()

        for key, value in fetch_data.items():
            score_id = key.split("-")[1]
            SQL.sql(f"UPDATE scores SET (score, score_updated_at) = ({value}, '{datetime.datetime.now()}') WHERE score_id = {score_id}")

        return redirect(url_for("record_scores.record_scores"))