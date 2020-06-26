from flask import Blueprint, render_template, abort, jsonify, session, request, redirect
import math, re
import hashlib
from models.users import Users

index = Blueprint("index", __name__)
@index.route('/')
def red():
    return redirect('/login')