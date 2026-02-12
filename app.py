from flask import Flask, request, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///messages.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# 数据库模型
class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    content = db.Column(db.String(200), nullable=False)

    def __repr__(self):
        return f'<Message {self.id}>'

# 创建表
with app.app_context():
    db.create_all()

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        name = request.form['name']
        content = request.form['content']
        new_msg = Message(name=name, content=content)
        db.session.add(new_msg)
        db.session.commit()
        return redirect(url_for('index'))
    messages = Message.query.order_by(Message.id.desc()).all()
    return render_template('index.html', messages=messages)

if __name__ == '__main__':
    app.run(debug=True)