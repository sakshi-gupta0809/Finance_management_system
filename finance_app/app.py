from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, date
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'your-secret-key-here')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///finance.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Database Models
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(120), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    incomes = db.relationship('Income', backref='user', lazy=True, cascade='all, delete-orphan')
    expenses = db.relationship('Expense', backref='user', lazy=True, cascade='all, delete-orphan')
    budgets = db.relationship('Budget', backref='user', lazy=True, cascade='all, delete-orphan')
    goals = db.relationship('Goal', backref='user', lazy=True, cascade='all, delete-orphan')

class Income(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    description = db.Column(db.String(200), nullable=False)
    amount = db.Column(db.Numeric(10, 2), nullable=False)
    category = db.Column(db.String(50), nullable=False)
    income_date = db.Column(db.Date, nullable=False, default=date.today)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Expense(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    description = db.Column(db.String(200), nullable=False)
    amount = db.Column(db.Numeric(10, 2), nullable=False)
    category = db.Column(db.String(50), nullable=False)
    expense_date = db.Column(db.Date, nullable=False, default=date.today)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Budget(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    category = db.Column(db.String(50), nullable=False)
    amount = db.Column(db.Numeric(10, 2), nullable=False)
    period = db.Column(db.String(20), nullable=False, default='monthly')  # monthly, yearly
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Goal(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    target_amount = db.Column(db.Numeric(10, 2), nullable=False)
    current_amount = db.Column(db.Numeric(10, 2), default=0)
    target_date = db.Column(db.Date, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Routes
@app.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        
        if User.query.filter_by(username=username).first():
            flash('Username already exists')
            return redirect(url_for('register'))
        
        if User.query.filter_by(email=email).first():
            flash('Email already registered')
            return redirect(url_for('register'))
        
        user = User(
            username=username,
            email=email,
            password_hash=generate_password_hash(password)
        )
        db.session.add(user)
        db.session.commit()
        
        flash('Registration successful! Please login.')
        return redirect(url_for('login'))
    
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        
        if user and check_password_hash(user.password_hash, password):
            login_user(user)
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid username or password')
    
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/dashboard')
@login_required
def dashboard():
    # Get current month's data
    current_month = date.today().replace(day=1)
    
    # Monthly income and expenses
    monthly_income = db.session.query(db.func.sum(Income.amount)).filter(
        Income.user_id == current_user.id,
        Income.income_date >= current_month
    ).scalar() or 0
    
    monthly_expenses = db.session.query(db.func.sum(Expense.amount)).filter(
        Expense.user_id == current_user.id,
        Expense.expense_date >= current_month
    ).scalar() or 0
    
    # Recent transactions
    recent_income = Income.query.filter_by(user_id=current_user.id).order_by(Income.created_at.desc()).limit(5).all()
    recent_expenses = Expense.query.filter_by(user_id=current_user.id).order_by(Expense.created_at.desc()).limit(5).all()
    
    # Budget status
    budgets = Budget.query.filter_by(user_id=current_user.id).all()
    budget_status = []
    
    for budget in budgets:
        spent = db.session.query(db.func.sum(Expense.amount)).filter(
            Expense.user_id == current_user.id,
            Expense.category == budget.category,
            Expense.expense_date >= current_month
        ).scalar() or 0
        
        budget_status.append({
            'category': budget.category,
            'budget': float(budget.amount),
            'spent': float(spent),
            'remaining': float(budget.amount) - float(spent)
        })
    
    return render_template('dashboard.html',
                         monthly_income=monthly_income,
                         monthly_expenses=monthly_expenses,
                         recent_income=recent_income,
                         recent_expenses=recent_expenses,
                         budget_status=budget_status)

@app.route('/income', methods=['GET', 'POST'])
@login_required
def income():
    if request.method == 'POST':
        description = request.form['description']
        amount = request.form['amount']
        category = request.form['category']
        income_date = datetime.strptime(request.form['income_date'], '%Y-%m-%d').date()
        
        income = Income(
            user_id=current_user.id,
            description=description,
            amount=amount,
            category=category,
            income_date=income_date
        )
        db.session.add(income)
        db.session.commit()
        
        flash('Income added successfully!')
        return redirect(url_for('income'))
    
    incomes = Income.query.filter_by(user_id=current_user.id).order_by(Income.income_date.desc()).all()
    return render_template('income.html', incomes=incomes)

@app.route('/expense', methods=['GET', 'POST'])
@login_required
def expense():
    if request.method == 'POST':
        description = request.form['description']
        amount = request.form['amount']
        category = request.form['category']
        expense_date = datetime.strptime(request.form['expense_date'], '%Y-%m-%d').date()
        
        expense = Expense(
            user_id=current_user.id,
            description=description,
            amount=amount,
            category=category,
            expense_date=expense_date
        )
        db.session.add(expense)
        db.session.commit()
        
        flash('Expense added successfully!')
        return redirect(url_for('expense'))
    
    expenses = Expense.query.filter_by(user_id=current_user.id).order_by(Expense.expense_date.desc()).all()
    return render_template('expense.html', expenses=expenses)

@app.route('/budget', methods=['GET', 'POST'])
@login_required
def budget():
    if request.method == 'POST':
        category = request.form['category']
        amount = request.form['amount']
        period = request.form['period']
        
        # Check if budget already exists for this category
        existing_budget = Budget.query.filter_by(
            user_id=current_user.id,
            category=category
        ).first()
        
        if existing_budget:
            existing_budget.amount = amount
            existing_budget.period = period
        else:
            budget = Budget(
                user_id=current_user.id,
                category=category,
                amount=amount,
                period=period
            )
            db.session.add(budget)
        
        db.session.commit()
        flash('Budget updated successfully!')
        return redirect(url_for('budget'))
    
    budgets = Budget.query.filter_by(user_id=current_user.id).all()
    return render_template('budget.html', budgets=budgets)

@app.route('/reports')
@login_required
def reports():
    # Get data for charts
    current_month = date.today().replace(day=1)
    
    # Category-wise expenses
    category_expenses = db.session.query(
        Expense.category,
        db.func.sum(Expense.amount)
    ).filter(
        Expense.user_id == current_user.id,
        Expense.expense_date >= current_month
    ).group_by(Expense.category).all()
    
    # Monthly trend (last 6 months)
    monthly_trend = []
    for i in range(6):
        month_start = date.today().replace(day=1)
        for _ in range(i):
            if month_start.month == 1:
                month_start = month_start.replace(year=month_start.year-1, month=12)
            else:
                month_start = month_start.replace(month=month_start.month-1)
        
        income = db.session.query(db.func.sum(Income.amount)).filter(
            Income.user_id == current_user.id,
            Income.income_date >= month_start
        ).scalar() or 0
        
        expense = db.session.query(db.func.sum(Expense.amount)).filter(
            Expense.user_id == current_user.id,
            Expense.expense_date >= month_start
        ).scalar() or 0
        
        monthly_trend.append({
            'month': month_start.strftime('%B %Y'),
            'income': float(income),
            'expense': float(expense)
        })
    
    return render_template('reports.html',
                         category_expenses=category_expenses,
                         monthly_trend=monthly_trend)

@app.route('/goals', methods=['GET', 'POST'])
@login_required
def goals():
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        target_amount = request.form['target_amount']
        target_date = datetime.strptime(request.form['target_date'], '%Y-%m-%d').date()
        
        goal = Goal(
            user_id=current_user.id,
            title=title,
            description=description,
            target_amount=target_amount,
            target_date=target_date
        )
        db.session.add(goal)
        db.session.commit()
        
        flash('Goal created successfully!')
        return redirect(url_for('goals'))
    
    goals = Goal.query.filter_by(user_id=current_user.id).all()
    return render_template('goals.html', goals=goals)

@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    if request.method == 'POST':
        current_user.username = request.form['username']
        current_user.email = request.form['email']
        
        if request.form['new_password']:
            current_user.password_hash = generate_password_hash(request.form['new_password'])
        
        db.session.commit()
        flash('Profile updated successfully!')
        return redirect(url_for('profile'))
    
    return render_template('profile.html')

# API Routes for AJAX
@app.route('/api/delete_income/<int:income_id>', methods=['DELETE'])
@login_required
def delete_income(income_id):
    income = Income.query.get_or_404(income_id)
    if income.user_id != current_user.id:
        return jsonify({'error': 'Unauthorized'}), 403
    
    db.session.delete(income)
    db.session.commit()
    return jsonify({'message': 'Income deleted successfully'})

@app.route('/api/delete_expense/<int:expense_id>', methods=['DELETE'])
@login_required
def delete_expense(expense_id):
    expense = Expense.query.get_or_404(expense_id)
    if expense.user_id != current_user.id:
        return jsonify({'error': 'Unauthorized'}), 403
    
    db.session.delete(expense)
    db.session.commit()
    return jsonify({'message': 'Expense deleted successfully'})

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True) 