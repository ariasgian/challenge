# -*- coding: utf-8 -*-
"""
Created on Tue Feb  1 18:33:48 2022
Modulo de conexion con base de datos Postgresql
@author: arias
"""

import sqlalchemy as db
from sqlalchemy.ext.declarative import declarative_base

from datetime import datetime
model = declarative_base()


class MyTable(model):
    __tablename__ = 'tbl_data'
     
    cod_localidad = db.Column(db.Integer, primary_key=True)
    id_provincia = db.Column(db.Integer)
    id_departamento = db.Column(db.Integer)
    categoría = db.Column(db.String())
    provincia = db.Column(db.String())
    localidad = db.Column(db.String())
    nombre = db.Column(db.String())
    domicilio = db.Column(db.String())
    cp= db.Column(db.String())
    telefono=db.Column(db.Integer)
    mail=db.Column(db.String())
    web=db.Column(db.String())
    fecha= db.Column(db.DateTime, default=datetime.utcnow)



path="postgresql://user_test:test1234@localhost/db_test"
engine = db.create_engine(path, echo=True)
# 
#model.metadata.create_all(engine)