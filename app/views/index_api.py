from flask import Blueprint, request, jsonify

import os

index = Blueprint("index", __name__)


@index.route('/rotation/', methods=["GET"])
def rotation_chart():

