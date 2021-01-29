from flask import Flask, request, jsonify
from modules.user.dao import UserDAO
from modules.user.service.factory import UserFactory
from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker

meta = MetaData()
app = Flask(__name__)
engine = create_engine('postgresql://api:12345@localhost:5432/api_db')
Session = sessionmaker(bind=engine)
Session = Session()
meta.create_all(engine)


@app.route('/test', methods={'GET'})
def test_route():
    return "HTTPStatus.OK"


@app.route('/user', methods={'POST'})
def create_user():
    data = request.json
    result = UserFactory.user_factory(name=data['name'], about=data['about'], nationality=data['nationality'],
                                          birth=data['birth'],
                                          study=data['study'], pic=data['pic'], email=data['email'],
                                          phone=data['phone'])

    return "OK"


@app.route('/all/users', methods={'GET'})
async def read_all_users():
    query = await UserDAO.read_all_users()
    if query is not None:
        return query
    else:
        return "query"


@app.route('/get/user', methods={'PATCH'})
def get_user():
    data = request.json
    UserDAO.read_user(data.user_id)
    return jsonify()


if __name__ == '__main__':
    app.run(debug=True, port=5000)
