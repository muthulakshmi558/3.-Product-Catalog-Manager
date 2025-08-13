from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# MySQL connection string
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://username:password@hostname:port/dbname'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'mysecretkey123456789'

db = SQLAlchemy(app)

# Model
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    price = db.Column(db.Float, nullable=False)
    in_stock = db.Column(db.Boolean, default=True)
    description = db.Column(db.Text, nullable=True)

    def __repr__(self):
        return f'<Product {self.name}>'

# Create tables
with app.app_context():
    db.create_all()

# View all products
@app.route('/')
def index():
    products = Product.query.all()
    in_stock_products = Product.query.filter_by(in_stock=True).all()
    return render_template('index.html', products=products, in_stock_products=in_stock_products)

# Add product
@app.route('/add', methods=['GET', 'POST'])
def add_product():
    if request.method == 'POST':
        name = request.form['name']
        price = request.form['price']
        in_stock = 'in_stock' in request.form
        description = request.form['description']

        new_product = Product(name=name, price=price, in_stock=in_stock, description=description)
        db.session.add(new_product)
        db.session.commit()
        flash('Product added successfully!', 'success')
        return redirect(url_for('index'))

    return render_template('add_product.html')

# Edit product
@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_product(id):
    product = Product.query.get_or_404(id)

    if request.method == 'POST':
        product.name = request.form['name']
        product.price = request.form['price']
        product.in_stock = 'in_stock' in request.form
        product.description = request.form['description']

        db.session.commit()
        flash('Product updated successfully!', 'success')
        return redirect(url_for('index'))

    return render_template('edit_product.html', product=product)

# Delete product
@app.route('/delete/<int:id>')
def delete_product(id):
    product = Product.query.get_or_404(id)
    db.session.delete(product)
    db.session.commit()
    flash('Product deleted successfully!', 'danger')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
