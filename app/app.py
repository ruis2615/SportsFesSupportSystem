import json
import os
import configparser

import requests
from werkzeug.security import check_password_hash
from flask import Flask, render_template, request, redirect, url_for
from flask_login import LoginManager, login_user, logout_user, login_required, UserMixin, current_user

from src.db import db_connect

from src.accounts import accounts_module
from src.schedules import schedules_module
from src.record_scores import record_scores_module
from src.teams import teams_module
from src.entrys import entrys_module
from src.entrys_check import entrys_check_module
from src.absence_report import absence_report_module

app = Flask(__name__)

config_ini = configparser.ConfigParser()
config_ini.read('config/config.ini', encoding='utf-8')
app.config["RUN_MODE"] = int(config_ini['Common']['RUN_MODE'])

with app.app_context():
    db_connector = db_connect()
    db_cursor = db_connector.cursor()

if app.config.get("RUN_MODE") == 1:
    app.config["SECRET_KEY"] = "develop"
else:
    app.config["SECRET_KEY"] = os.urandom(24)

login_manager = LoginManager()
login_manager.init_app(app)

app.register_blueprint(accounts_module)
app.register_blueprint(schedules_module)
app.register_blueprint(record_scores_module)
app.register_blueprint(teams_module)
app.register_blueprint(entrys_module)
app.register_blueprint(entrys_check_module)
app.register_blueprint(absence_report_module)


class GetData:
    @staticmethod
    def get_fetchone(sql, *args):
        db_cursor.execute(sql, args)
        fetch_data = db_cursor.fetchone()
        return fetch_data

    @staticmethod
    def get_fetchall(sql, *args):
        db_cursor.execute(sql, args)
        fetch_data = db_cursor.fetchall()
        return fetch_data

    @staticmethod
    def get_fetchmany(sql, *args):
        db_cursor.execute(sql, args)
        fetch_data = db_cursor.fetchmany()
        return fetch_data


class SQL:
    @staticmethod
    def sql(sql):
        db_cursor.execute(sql)
        db_connector.commit()
        return


def GetWeatherForecast():
    response = requests.get("https://api.open-meteo.com/v1/forecast?latitude=35.08&longitude=136.62&daily=weathercode,apparent_temperature_max,apparent_temperature_min,precipitation_probability_max&forecast_days=1&timezone=Asia%2FTokyo")
    weather_data = json.loads(json.dumps(response.json(), indent=4))
    return weather_data["daily"]


class User(UserMixin):
    def __init__(self, user_id, user_name, user_permission):
        self.id = user_id
        self.name = user_name
        self.permission = user_permission

    @staticmethod
    def get(user_id):
        user = GetData.get_fetchone(f"SELECT * FROM users WHERE user_id = '{user_id}'")

        if user is None:
            return None

        return User(user_id=user[0], user_name=user[1], user_permission=user[3])


@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)


@login_manager.unauthorized_handler
def unauthorized():
    return redirect(url_for("index"))


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        if current_user.is_authenticated:
            return redirect(url_for("index"))
        return render_template("pages/login.html", error=None)

    elif request.method == "POST":
        user_name = request.form.get("UserName")
        user_password = request.form.get("UserPassword")
        remember_me = request.form.get("RememberMe")

        user = GetData.get_fetchone(f"SELECT * FROM users WHERE user_name = '{user_name}'")

        if user is None:
            return render_template("pages/login.html", error="ユーザーが存在しません。")

        elif check_password_hash(user[2], user_password):
            if remember_me == "on":
                login_user(User(user_id=user[0], user_name=user[1], user_permission=user[3]), remember=True)
            login_user(User(user_id=user[0], user_name=user[1], user_permission=user[3]))
            return redirect(url_for("index"))

        else:
            return render_template("pages/login.html", error="ユーザー名またはパスワードが間違っている可能性があります。")


@app.route("/logout", methods=["GET"])
@login_required
def logout():
    logout_user()
    return redirect(url_for("index"))


@app.route("/")
def index():
    master_options = GetData.get_fetchone("SELECT * FROM options WHERE option_name = 'master_options'")[1]
    top_team = GetData.get_fetchone("SELECT teams.team_name, COALESCE(SUM(scores.score), 0) FROM teams INNER JOIN scores ON teams.team_id = scores.team_id GROUP BY teams.team_name ORDER BY SUM(scores.score) DESC LIMIT 1")
    now_sport = GetData.get_fetchone("SELECT schedule_number, schedule_name, TO_CHAR(schedule_started_at, 'HH24:MI'), TO_CHAR(schedule_ended_at, 'HH24:MI') FROM schedules WHERE TO_CHAR(schedule_started_at, 'HH24:MI') <= TO_CHAR(timezone('Asia/Tokyo', now()), 'HH24:MI') AND TO_CHAR(schedule_ended_at, 'HH24:MI') >= TO_CHAR(timezone('Asia/Tokyo', now()), 'HH24:MI')")
    next_sports = GetData.get_fetchall("SELECT schedule_number, schedule_name, TO_CHAR(schedule_started_at, 'HH24:MI'), TO_CHAR(schedule_ended_at, 'HH24:MI') FROM schedules WHERE TO_CHAR(schedule_started_at, 'HH24:MI') >= TO_CHAR(timezone('Asia/Tokyo', now()), 'HH24:MI') ORDER BY schedule_number")
    weather_forecast = GetWeatherForecast()

    if len(next_sports) == 0:
        next_sports = None

    return render_template("index.html", master_options=master_options, top_team=top_team, now_sport=now_sport, next_sports=next_sports, weather_forecast=weather_forecast)


@app.route("/update-info")
def update_info():
    return render_template("pages/update_info.html")


@app.route("/settings", methods=["GET", "POST"])
@login_required
def settings():
    if current_user.permission == "all_prtmissions":
        if request.method == "GET":
            master_options = GetData.get_fetchone("SELECT * FROM options WHERE option_name = 'master_options'")[1]
            return render_template("pages/settings/settings.html", master_options=master_options)

        elif request.method == "POST":
            if request.form.get("ScoreOption") == "on":
                score_option = 0
            else:
                score_option = 1

            if request.form.get("EntryStatus") == "on":
                entry_status = 0
            else:
                entry_status = 1

            option_value = {
                "dashboard_top_team_data": score_option,
                "entry_status": entry_status
            }

            SQL.sql(f"UPDATE options SET option_value = '{json.dumps(option_value)}' WHERE option_name = 'master_options'")
            return redirect(url_for("index"))

    return redirect(url_for("index"))


if __name__ == '__main__':
    if app.config.get("RUN_MODE") == 1:
        app.run(debug=True)
    else:
        app.run()
