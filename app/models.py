
import datetime
from types import ClassMethodDescriptorType
from typing import Text

from slugify import slugify
from sqlalchemy.exc import IntegrityError
from werkzeug.security import generate_password_hash, check_password_hash

from app import db

class Base(db.Model):
    __abstract__ = True

    id = db.Column(db.Integer, primary_key=True)
    created = db.Column(db.DateTime, default=db.func.current_timestamp())
    modified = db.Column(db.DateTime, default=db.func.current_timestamp(),\
                     onupdate=db.func.current_timestamp())

class Post(Base):
    user_id = db.Column(db.Integer, db.ForeignKey('blog_user.id', ondelete='CASCADE'), nullable=False)
    title = db.Column(db.String(256), nullable=False)
    title_slug = db.Column(db.String(256), unique=True, nullable=False)
    content = db.Column(db.Text)
    created = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    image_name = db.Column(db.String)
    comments = db.relationship('Comment', backref='post', lazy=True, cascade='all, delete-orphan',
                               order_by='asc(Comment.created)')

    def __repr__(self):
        return f'<Post {self.title}>'

    def save(self):
        if not self.id:
            db.session.add(self)
        if not self.title_slug:
            self.title_slug = slugify(self.title)

        saved = False
        count = 0
        while not saved:
            try:
                db.session.commit()
                saved = True
            except IntegrityError:
                db.session.rollback()
                db.session.add(self)
                count += 1
                self.title_slug = f'{slugify(self.title)}-{count}'

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    @staticmethod
    def get_by_slug(slug):
        return Post.query.filter_by(title_slug=slug).first()

    @staticmethod
    def get_by_id(id):
        return Post.query.get(id)

    @staticmethod
    def get_all():
        return Post.query.all()

    @staticmethod
    def all_paginated(page=1, per_page=20):
        return Post.query.order_by(Post.created.asc()). \
            paginate(page=page, per_page=per_page, error_out=False)


class Comment(Base):
    user_id = db.Column(db.Integer, db.ForeignKey('blog_user.id', ondelete='SET NULL'))
    user_name = db.Column(db.String)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)
    content = db.Column(db.Text)
    created = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    def __init__(self, content, user_id=None, user_name=user_name, post_id=None):
        self.content = content
        self.user_id = user_id
        self.user_name = user_name
        self.post_id = post_id

    def __repr__(self):
        return f'<Comment {self.content}>'

    def save(self):
        if not self.id:
            db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    @staticmethod
    def get_by_post_id(post_id):
        return Comment.query.filter_by(post_id=post_id).all()

class Ofrecimientos (Base):
    __tablename__ = "ofrecimientos"
    correo_electronico = db.Column(db.String(256))
    importe_ofertado = db.Column(db.String(128))
    compulsa_id = db.Column(db.Integer, db.ForeignKey('compulsas.id'), nullable=False)
    fecha_confirmacion = db.Column(db.DateTime)
    fecha_envio = db.Column(db.DateTime)
    fecha_reenvio = db.Column(db.DateTime)
    status = db.Column(db.String(20))
    pin = db.Column(db.String(128))

    def __init__(self, importe_ofertado, pin):
        self.importe_ofertado = importe_ofertado
        self.pin=pin

    def set_importe_ofertado(self, importe_ofertado):
        self.importe_ofertado = generate_password_hash(importe_ofertado)

    def check_importe_ofertado(self, importe_ofertado):
        return check_password_hash(self.importe_ofertado, importe_ofertado)

    def set_pin(self, pin):
        self.pin = generate_password_hash(pin)

    def check_pin(self, pin):
        return check_password_hash(self.pin, pin)

class Compulsas (Base):
    __tablename__ = "compulsas"
    bien = db.Column(db.String(256), nullable = False)
    fecha_inicio = db.Column(db.DateTime, nullable = False)
    fecha_vencimiento = db.Column(db.DateTime, nullable = False)
    usuario_creador = db.Column(db.Integer)
    usuario_aprobador = db.Column(db.Integer)
    ubicacion = db.Column(db.String(150), nullable = False)
    condiciones_generales = db.Column(db.Text, nullable = False)
    importe_base = db.Column(db.Integer, nullable = False)
    para_empleados = db.Column(db.Boolean, default=False)
    tipo_bien = db.Column(db.Integer, nullable=False)
    imagenes = db.Column(db.Integer, db.ForeignKey('imagenes.id'), nullable=False)
    ofrecimiento = db.relationship('Ofrecimientos', backref='compulsa', lazy=True, cascade='all, delete-orphan',
                               order_by='asc(Ofrecimientos.created)')
   
class Imagenes(Base):
    __tablename__ = "imagenes"
    imagen = db.Column(db.String(256), nullable = False)
    compulsa = db.relationship('Compulsas', backref='compulsa', lazy=True,cascade='all, delete-orphan',
                               order_by='asc(Compulsas.created)')

class TipoBienes(Base):
    __tablename__ = "tipobienes"
    tipo_bien = db.Column(db.String(50), nullable = False)

class CorreosElectronicos (Base):
    __tablename__ = "correoselectronicos"
    correo = db.Column(db.String(256), unique=True, nullable=False)
    nombre = db.Column(db.String(256), nullable=False)
    empleado = db.Column(db.Boolean, default=False)
    desarmadero = db.Column(db.Boolean, default=False)
    status = db.Column(db.Boolean, default=False)
    fecha_baja = db.Column(db.DateTime)
    quien_baja = db.Column(db.String(256))
