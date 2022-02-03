from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_restful import Api, Resource

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
ma = Marshmallow(app)
api = Api(app)

class Publicacion(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    nombre = db.Column( db.String(50) )
    lugar = db.Column( db.String(255) )
    direccion = db.Column( db.String(255) )
    inicio = db.Column( db.String(255) )
    fin = db.Column( db.String(255) )
    modalidad = db.Column( db.String(255) )
    
class Publicacion_Schema(ma.Schema):
    class Meta:
        fields = ("id", "nombre", "lugar", "direccion", "inicio", "fin", "modalidad")
    
post_schema = Publicacion_Schema()
posts_schema = Publicacion_Schema(many = True)

class RecursoListarPublicaciones(Resource):
    def get(self):
        publicaciones = Publicacion.query.all()
        return posts_schema.dump(publicaciones)
    
    def post(self):
            nueva_publicacion = Publicacion(
                nombre = request.json['nombre'],
                lugar=request.json['lugar'],
                direccion=request.json['direccion'],
                inicio=request.json['inicio'],
                fin=request.json['fin'],
                modalidad=request.json['modalidad']
            )
            db.session.add(nueva_publicacion)
            db.session.commit()
            return post_schema.dump(nueva_publicacion)
     
class RecursoUnaPublicacion(Resource):
    def get(self, id_publicacion):
        publicacion = Publicacion.query.get_or_404(id_publicacion)
        return post_schema.dump(publicacion)
    
    def put(self, id_publicacion):
        publicacion = Publicacion.query.get_or_404(id_publicacion)
        if 'nombre' in request.json:
            publicacion.nombre = request.json['nombre']
        if 'lugar' in request.json:
            publicacion.lugar = request.json['lugar']
        if 'direccion' in request.json:
            publicacion.direccion = request.json['direccion']
        if 'inicio' in request.json:
            publicacion.inicio = request.json['inicio']
        if 'fin' in request.json:
            publicacion.fin = request.json['fin']
        if 'modalidad' in request.json:
            publicacion.modalidad = request.json['modalidad']  

        db.session.commit()
        return post_schema.dump(publicacion)

    def delete(self, id_publicacion):
        publicacion = Publicacion.query.get_or_404(id_publicacion)
        db.session.delete(publicacion)
        db.session.commit()
        return '', 204

api.add_resource(RecursoListarPublicaciones, '/publicaciones')     
api.add_resource(RecursoUnaPublicacion, '/publicaciones/<int:id_publicacion>')

if __name__ == '__main__':
    app.run(debug=True)