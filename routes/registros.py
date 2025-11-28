from flask import Blueprint, request, jsonify
from functools import wraps
from database import db
from models.user import User
from models.registro import Registro
import jwt
from datetime import datetime

registros_bp = Blueprint('registros', __name__)
SECRET = 'super-secret-key-change-me'

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.headers.get('Authorization', None)
        if not auth:
            return jsonify({'message': 'Token is missing'}), 401
        parts = auth.split()
        if parts[0].lower() != 'bearer' or len(parts) != 2:
            return jsonify({'message': 'Authorization header must be Bearer token'}), 401
        token = parts[1]
        try:
            data = jwt.decode(token, SECRET, algorithms=['HS256'])
            user = User.query.get(data['user_id'])
            if not user:
                return jsonify({'message': 'user not found'}), 401
            request.user = user
        except jwt.ExpiredSignatureError:
            return jsonify({'message': 'token expired'}), 401
        except Exception as e:
            return jsonify({'message': 'token invalid', 'error': str(e)}), 401
        return f(*args, **kwargs)
    return decorated

@registros_bp.route('/transacoes', methods=['POST'])
@token_required
def create_transacao():
    data = request.get_json() or {}
    valor = data.get('valor')
    categoria = data.get('categoria')
    descricao = data.get('descricao')
    data_str = data.get('data')
    tipo = data.get('tipo')
    if valor is None or tipo not in ('receita', 'despesa'):
        return jsonify({'message': 'valor and tipo (receita/despesa) required'}), 400
    if data_str:
        try:
            data_dt = datetime.fromisoformat(data_str)
        except:
            return jsonify({'message': 'data must be ISO format YYYY-MM-DD or YYYY-MM-DDTHH:MM:SS'}), 400
    else:
        data_dt = datetime.utcnow()
    reg = Registro(valor=float(valor), categoria=categoria, descricao=descricao, data=data_dt, tipo=tipo, user_id=request.user.id)
    db.session.add(reg)
    db.session.commit()
    return jsonify({'message': 'created', 'registro': reg.to_dict()}), 201

@registros_bp.route('/transacoes', methods=['GET'])
@token_required
def list_transacoes():
    # Optional filters: tipo, categoria, date_from, date_to
    q = Registro.query.filter_by(user_id=request.user.id)
    tipo = request.args.get('tipo')
    categoria = request.args.get('categoria')
    date_from = request.args.get('date_from')
    date_to = request.args.get('date_to')
    if tipo in ('receita', 'despesa'):
        q = q.filter_by(tipo=tipo)
    if categoria:
        q = q.filter(Registro.categoria.ilike(f'%{categoria}%'))
    if date_from:
        try:
            df = datetime.fromisoformat(date_from)
            q = q.filter(Registro.data >= df)
        except:
            pass
    if date_to:
        try:
            dt = datetime.fromisoformat(date_to)
            q = q.filter(Registro.data <= dt)
        except:
            pass
    registros = [r.to_dict() for r in q.order_by(Registro.data.desc()).all()]
    return jsonify(registros)

@registros_bp.route('/transacoes/<int:reg_id>', methods=['GET'])
@token_required
def get_transacao(reg_id):
    reg = Registro.query.get_or_404(reg_id)
    if reg.user_id != request.user.id:
        return jsonify({'message': 'forbidden'}), 403
    return jsonify(reg.to_dict())

@registros_bp.route('/transacoes/<int:reg_id>', methods=['PUT'])
@token_required
def update_transacao(reg_id):
    reg = Registro.query.get_or_404(reg_id)
    if reg.user_id != request.user.id:
        return jsonify({'message': 'forbidden'}), 403
    data = request.get_json() or {}
    if 'valor' in data:
        reg.valor = float(data['valor'])
    if 'categoria' in data:
        reg.categoria = data['categoria']
    if 'descricao' in data:
        reg.descricao = data['descricao']
    if 'data' in data:
        try:
            reg.data = datetime.fromisoformat(data['data'])
        except:
            pass
    if 'tipo' in data and data['tipo'] in ('receita','despesa'):
        reg.tipo = data['tipo']
    db.session.commit()
    return jsonify({'message': 'updated', 'registro': reg.to_dict()})

@registros_bp.route('/transacoes/<int:reg_id>', methods=['DELETE'])
@token_required
def delete_transacao(reg_id):
    reg = Registro.query.get_or_404(reg_id)
    if reg.user_id != request.user.id:
        return jsonify({'message': 'forbidden'}), 403
    db.session.delete(reg)
    db.session.commit()
    return jsonify({'message': 'deleted'})