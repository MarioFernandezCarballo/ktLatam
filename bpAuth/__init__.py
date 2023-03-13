from datetime import timedelta
from flask import Blueprint, make_response, redirect, url_for, request, flash, render_template, current_app
from flask_jwt_extended import create_access_token, JWTManager, set_access_cookies, unset_jwt_cookies
from flask_login import LoginManager, login_user, login_required, logout_user

from utils.user import userLogin, userSignup, getUserOnly


authBP = Blueprint('authBluePrint', __name__)

loginManager = LoginManager()
jwt = JWTManager()


@loginManager.user_loader
def loadUser(user_id):
    return getUserOnly(user_id)


@jwt.expired_token_loader
def refreshToken(jwt_header, jwt_data):
    response = make_response(redirect(url_for('authBluePrint.login')))
    unset_jwt_cookies(response)
    return response


@authBP.route('/signup/only-collaborator', methods=['GET', 'POST'])
def signupEndPoint():
    if request.method == 'POST':
        status, new_user = userSignup(current_app.config['database'], request.form)
        if status == 401:
            flash("Your password must have 8 characters, 1 uppercase and 1 digit")
            return redirect(url_for('authBluePrint.signupEndPoint'))
        if status == 402:
            flash("The username already exists")
            return redirect(url_for('authBluePrint.signupEndPoint'))
        if status == 200:
            response = redirect(url_for('genericBluePrint.generalEndPoint'))
            set_access_cookies(response, create_access_token(identity=new_user.bcpId,
                                                             expires_delta=timedelta(days=365)))
            response.set_cookie("preferred_update", "1")
            response.set_cookie("preferred_gameType", "1")
            response.set_cookie("preferred_language", "en")
            login_user(new_user)
            flash("Registered successfully")
            return response
        if status == 403:
            flash("Password fields must coincide")
            return redirect(url_for('authBluePrint.signupEndPoint'))
        if status == 405:
            flash("Username must not have special characters")
            return redirect(url_for('authBluePrint.signupEndPoint'))
    return render_template('signup.html', title="Signup")


@authBP.route('/login/only-collaborator', methods=['GET', 'POST'])
def loginEndPoint():
    if request.method == 'POST':
        status, user = userLogin(request.form)
        if status == 200:
            flash("Login successful")
            response = redirect(url_for('genericBluePrint.generalEndPoint'))
            set_access_cookies(response, create_access_token(identity=user.bcpId))
            response.set_cookie("preferred_update", "1")
            response.set_cookie("preferred_gameType", "1")
            response.set_cookie("preferred_language", "en")
            login_user(user)
            return response
        if status == 401:
            flash("Could not verify")
            return make_response(render_template('login.html', title="Login"), 401, {'Authentication': '"login required"'})
    return render_template('login.html', title="Login")


@authBP.route('/logout', methods=['GET', 'POST'])
@login_required
def logoutEndPoint():
    response = redirect(url_for('genericBluePrint.generalEndPoint'))
    unset_jwt_cookies(response)
    logout_user()
    flash("Logout successfully")
    return response
