import random
import string
import datetime

from flask import render_template, url_for, redirect, request, Blueprint
from flask_login import current_user, login_required
from werkzeug.security import generate_password_hash

from .db import GetData, SQL

teams_module = Blueprint("teams", __name__, url_prefix="/teams")


def CreateTeamPassword(n):
   return ''.join(random.choices(string.ascii_letters + string.digits, k=n))


@teams_module.route("/")
@login_required
def teams():
    if current_user.permission == "all_prtmissions":
        teams = GetData.get_fetchall("SELECT teams.team_id, teams.team_name, COALESCE(SUM(scores.score), 0) as total_score, RANK() OVER (ORDER BY SUM(scores.score) DESC) as rank, teams.team_leader, teams.team_sub_leader, team_login_id, team_login_password FROM teams LEFT JOIN scores ON teams.team_id = scores.team_id GROUP BY teams.team_id, teams.team_name, teams.team_leader, teams.team_sub_leader, team_login_id, team_login_password ORDER BY teams.team_name")
        return render_template("pages/teams/teams.html", teams=teams)

    return redirect(url_for("app.index"))


@teams_module.route("/add", methods=["GET", "POST"])
@login_required
def teams_add():
    if current_user.permission == "all_prtmissions":
        if request.method == "GET":
            return render_template("pages/teams/teams_add.html")

        elif request.method == "POST":
            team_name = request.form.get("TeamName")
            team_leader = request.form.get("TeamLeader")
            team_sub_leader = request.form.get("TeamSubLeader")
            team_login_id = datetime.datetime.now().strftime('%Y%m%d')
            team_login_password = CreateTeamPassword(n=12)
            SQL.sql(f"INSERT INTO teams (team_name, team_leader, team_sub_leader, team_login_id, team_login_password) VALUES ('{team_name}', '{team_leader}', '{team_sub_leader}', '{team_login_id}-'||currval('teams_team_id_seq'), '{team_login_password}')")
            SQL.sql(f"INSERT INTO users (user_name, user_password, user_permission, user_created_at, user_type) VALUES ('{team_login_id}-'||(SELECT last_value FROM teams_team_id_seq), '{generate_password_hash(team_login_password, method='sha256')}', 'only_my_team_entry', '{datetime.datetime.now()}', '1')")
            return redirect(url_for("teams.teams"))
    return redirect(url_for("app.index"))


@teams_module.route("/remove/<int:team_id>", methods=["GET"])
@login_required
def teams_remove(team_id):
    if current_user.permission == "all_prtmissions":
        SQL.sql(f"DELETE FROM users WHERE user_name = (SELECT team_login_id FROM teams WHERE team_id = {team_id})")
        SQL.sql(f"DELETE FROM teams WHERE team_id = {team_id}")
        return redirect(url_for("teams.teams"))
    return redirect(url_for("app.index"))


@teams_module.route("/edit/<int:team_id>", methods=["GET", "POST"])
@login_required
def teams_edit(team_id):
    if current_user.permission == "all_prtmissions":
        if request.method == "GET":
            team = GetData.get_fetchone(f"SELECT team_id, team_name, team_leader, team_sub_leader FROM teams WHERE team_id = {team_id}")
            return render_template("pages/teams/teams_edit.html", team=team)

        elif request.method == "POST":
            team_name = request.form.get("TeamName")
            team_leader = request.form.get("TeamLeader")
            team_sub_leader = request.form.get("TeamSubLeader")
            SQL.sql(f"UPDATE teams SET (team_name, team_leader, team_sub_leader) = ('{team_name}', '{team_leader}', '{team_sub_leader}') WHERE team_id = {team_id}")
            return redirect(url_for("teams.teams"))
    return redirect(url_for("app.index"))