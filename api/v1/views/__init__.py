#!/usr/bin/python3
""" blueprint """
from flask import Blueprint, render_template, abort
app_views = Blueprint("app_views", __name__, template_folder="../../web_flask/templates")
from api.v1.views.index import *
