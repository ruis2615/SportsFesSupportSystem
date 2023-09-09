"""
アカウント管理に関連するコード
 - アカウントの一覧ページ(/accounts)
 - アカウントの追加
 - アカウントの削除
 - アカウントの編集
"""
import datetime

from flask import render_template, url_for, redirect, request, Blueprint
from flask_login import current_user, login_required
from werkzeug.security import generate_password_hash

from .db import GetData, SQL

accounts_module = Blueprint("accounts", __name__, url_prefix="/accounts")


@accounts_module.route("/", methods=["GET"])
@login_required
def accounts():
    if current_user.permission == "all_prtmissions":
        users = GetData.get_fetchall("SELECT user_id, user_name, user_permission, TO_CHAR(user_created_at, 'YYYY/MM/DD HH24:MI:SS'), TO_CHAR(user_updated_at, 'YYYY/MM/DD HH24:MI:SS'), user_type FROM users WHERE user_type = 0 ORDER BY user_id")
        return render_template("pages/accounts/accounts.html", users=users)
    return redirect(url_for("app.index"))


@accounts_module.route("/add", methods=["GET", "POST"])
@login_required
def accounts_add():
    if current_user.permission == "all_prtmissions":
        if request.method == "GET":
            return render_template("pages/accounts/accounts_add.html")
        elif request.method == "POST":
            account_name = request.form.get("AccountName")
            account_password = generate_password_hash(request.form.get("AccountPassword"), method="sha256")
            account_permission = request.form.get("AccountPermission")

            SQL.sql(f"INSERT INTO users (user_name, user_password, user_permission, user_type, user_created_at) VALUES ('{account_name}', '{account_password}', '{account_permission}', 0, '{datetime.datetime.now()}')")
            return redirect(url_for("accounts.accounts"))
    return redirect(url_for("app.index"))


@accounts_module.route("/remove/<int:user_id>", methods=["GET"])
@login_required
def accounts_remove(user_id):
    if current_user.permission == "all_prtmissions":
        SQL.sql(f"DELETE FROM users WHERE user_id = {user_id} AND user_type = 0")
        return redirect(url_for("accounts.accounts"))
    return redirect(url_for("app.index"))


@accounts_module.route("/edit/<int:user_id>", methods=["GET", "POST"])
@login_required
def account_edit(user_id):
    if current_user.permission == "all_prtmissions":
        if request.method == "GET":
            user = GetData.get_fetchone(f"SELECT * FROM users WHERE user_id = {user_id}")
            if user[4] == 0:
                return render_template("pages/accounts/accounts_edit.html", user=user)
            else:
                return redirect(url_for("accounts.accounts"))
        elif request.method == "POST":
            user_name = request.form.get("AccountName")
            user_password = generate_password_hash(request.form.get("AccountPassword"), method="sha256")
            user_permission = request.form.get("AccountPermission")

            SQL.sql(f"UPDATE users SET (user_name, user_password, user_permission, user_updated_at) = ('{user_name}', '{user_password}', '{user_permission}', '{datetime.datetime.now()}') WHERE user_id = {user_id}")
            return redirect(url_for("accounts.accounts"))
    return redirect(url_for("app.index"))
