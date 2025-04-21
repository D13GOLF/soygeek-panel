# core/auth.py
from flask import Blueprint, render_template, redirect, url_for, request, flash

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login')
def login():
    return render_template('auth/login.html')
