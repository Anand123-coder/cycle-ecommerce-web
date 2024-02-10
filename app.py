from flask import Flask,request, redirect, url_for,send_from_directory
from flask import render_template
from flask_sqlalchemy import SQLAlchemy
import os
from werkzeug.utils import secure_filename




app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://username:password@localhost/cycles'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
app.config['UPLOAD_FOLDER'] = 'uploads'

class Cycle(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cycle_name = db.Column(db.String(255), nullable=False)
    cycle_description = db.Column(db.String(255))
    cycle_price = db.Column(db.Integer)
    cycle_image = db.Column(db.String(255))


@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/about")
def about():
    return render_template('about.html')

@app.route("/ourcycle")
def cycle():
    return render_template('index.html')


@app.route("/shop", methods=['GET'])
def shop():
    cycles = Cycle.query.all()
    return render_template('shop.html',cycles=cycles)



@app.route("/adminpanel")
def panel():
    cycles = Cycle.query.all()
    return render_template('admin_panel.html',cycles=cycles)

@app.route('/delete/<int:cycle_id>')
def delete(cycle_id):
    cycledelete = Cycle.query.filter_by(id=cycle_id).first()
    db.session.delete(cycledelete)
    db.session.commit()
    return redirect(url_for('panel'))


@app.route("/admin",methods=['GET','POST'])
def admin():
    if request.method == 'POST':

        cycle_name = request.form.get('cycle_name')
        cycle_description = request.form.get('cycle_description')
        cycle_price = request.form.get('cycle_price')


        cycle_image = request.files['cycle_image']
        image_filename = secure_filename(cycle_image.filename)
        image_path = os.path.join(app.config['UPLOAD_FOLDER'], image_filename)
        cycle_image.save(image_path)

        
        new_cycle = Cycle(cycle_name=cycle_name, cycle_description=cycle_description,
                          cycle_price=cycle_price, cycle_image=image_filename)
        db.session.add(new_cycle)
        db.session.commit()
        return redirect(url_for('admin'))

    return render_template('admin.html')


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
