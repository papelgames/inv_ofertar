import logging
import os

from flask import render_template, redirect, url_for, abort, current_app
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename

from app.auth.decorators import admin_required
from app.auth.models import User
from app.models import Compulsas
from . import compulsa_bp
from .forms import PostForm, UserAdminForm

logger = logging.getLogger(__name__)


@compulsa_bp.route("/compulsas/")
@login_required
#@admin_required
def index():
    return render_template("compulsa/index.html")

@compulsa_bp.route("/compulsas/alta")
@login_required
#@admin_required
def compulsas_alta():
    return render_template("compulsa/abm_compulsa.html")

@compulsa_bp.route("/compulsas/modificacion")
@login_required
#@admin_required
def compulsas_modificacion():
    return render_template("compulsa/abm_compulsa.html")

@compulsa_bp.route("/compulsas/activas")
@login_required
#@admin_required
def activas():
    return render_template("compulsa/listado.html")

@compulsa_bp.route("/compulsas/historicas")
@login_required
#@admin_required
def historicas():
    return render_template("compulsa/listado.html")