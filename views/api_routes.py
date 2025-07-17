from flask import Blueprint, request, jsonify
from .models import User
from . import db

api = Blueprint('api', __name__,template_folder="../templates")

@api.route('/register', methods=['POST'])
def api_register():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({"message": "Eksik bilgi"}), 400

    if User.query.filter_by(username=username).first():
        return jsonify({"message": "⚠️ Bu kullanıcı adı zaten alınmış"}), 409

    new_user = User(username=username, password=password)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "✅ Kayıt başarılı"}), 201
