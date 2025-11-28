from database import db
from datetime import datetime

class Registro(db.Model):
    __tablename__ = 'registros'
    id = db.Column(db.Integer, primary_key=True)
    valor = db.Column(db.Float, nullable=False)
    categoria = db.Column(db.String(80), nullable=True)
    descricao = db.Column(db.String(255), nullable=True)
    data = db.Column(db.DateTime, default=datetime.utcnow)
    tipo = db.Column(db.String(20), nullable=False)  # 'receita' or 'despesa'
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'valor': self.valor,
            'categoria': self.categoria,
            'descricao': self.descricao,
            'data': self.data.date().isoformat() if self.data else None,
            'tipo': self.tipo,
            'user_id': self.user_id
        }