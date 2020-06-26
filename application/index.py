#-*- coding=utf-8 -*-
from flask import Blueprint, render_template, abort, jsonify, session, request, redirect
import math, re
import hashlib
from models.users import Users

index = Blueprint("index", __name__)
@index.route('/')
def f_index():
    return render_template('overview.html')

@index.route('/login')
def f_login():
    return render_template('login.html')