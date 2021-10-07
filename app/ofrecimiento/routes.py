import logging
import os

from flask import render_template, redirect, url_for, abort, current_app
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename

from app.auth.decorators import admin_required
from app.auth.models import User
from app.models import Compulsas
from . import ofrecimiento_bp
from .forms import PostForm, UserAdminForm

logger = logging.getLogger(__name__)


@ofrecimiento_bp.route("/ofrecimiento/iniciar/")
def iniciar():
    return render_template("ofrecimiento/iniciar.html")

@ofrecimiento_bp.route("/ofrecimiento/ofertar/")
def ofertar():
    return render_template("ofrecimiento/ofertar.html")

@ofrecimiento_bp.route("/ofrecimiento/borrar_oferta/")
def borrar_oferta():
    return render_template("ofrecimiento/borrar_oferta.html")

@ofrecimiento_bp.route("/ofrecimientos/resultados")
@login_required
def resultados():
    return render_template("ofrecimiento/resultados.html")

@ofrecimiento_bp.route("/ofrecimiento/ganador")
def ganador():
    return render_template("ofrecimiento/ganador.html")
