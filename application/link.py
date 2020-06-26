#-*- coding=utf-8 -*-
from flask import Blueprint, render_template, abort, jsonify, session, request, redirect
from models.links import Links

link = Blueprint("link", __name__)
@link.route('/link')
def f_link():
    result = Links().find_by_links()
    context = {}
    context['result'] = result
    return render_template('link.html', context=context)