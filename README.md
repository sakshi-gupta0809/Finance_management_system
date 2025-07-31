# Finance Management App

A comprehensive web-based finance management application built with Python Flask that helps users track income, expenses, set budgets, and achieve financial goals.

## Features

### 🏠 Dashboard
- **Financial Overview**: Monthly income, expenses, net savings, and savings rate
- **Budget Status**: Visual progress bars showing budget vs actual spending
- **Recent Transactions**: Latest income and expense entries
- **Quick Actions**: Easy access to add income, expenses, set budgets, and view reports

### 💰 Income Management
- Add, edit, and delete income entries
- Categorize income (Salary, Freelance, Investment, Business, Other)
- Track income by date
- View income history with search and filter options

### 💸 Expense Management
- Add, edit, and delete expense entries
- Categorize expenses (Food, Transport, Utilities, Entertainment, Shopping, Healthcare, Education, Other)
- Track expenses by date
- View expense history with detailed breakdown

### 📊 Budget Management
- Set monthly/yearly budgets by category
- Visual progress tracking with color-coded indicators
- Budget alerts when approaching or exceeding limits
- Easy budget updates and modifications

### 📈 Reports & Analytics
- **Category-wise Analysis**: Pie charts showing expense distribution
- **Monthly Trends**: Line charts tracking income vs expenses over time
- **Detailed Breakdown**: Tables with percentages and totals
- **Interactive Charts**: Responsive and interactive data visualization

### 🎯 Financial Goals
- Set financial goals with target amounts and dates
- Track progress with visual progress bars
- Goal management and updates
- Motivation through progress tracking

### 👤 User Management
- User registration and authentication
- Profile management
- Password updates
- Secure login/logout system

## Technology Stack

- **Backend**: Python Flask
- **Database**: SQLite (with SQLAlchemy ORM)
- **Frontend**: HTML5, CSS3, JavaScript, Bootstrap 5
- **Charts**: Chart.js for data visualization
- **Authentication**: Flask-Login with password hashing
- **Icons**: Font Awesome

## Installation & Setup

### Prerequisites
- Python 3.7 or higher
- pip (Python package installer)

### Installation Steps

1. **Clone or download the project**
   ```bash
   cd finance_app
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**
   ```bash
   python app.py
   ```

4. **Access the application**
   - Open your web browser
   - Go to: `http://localhost:5000`
   - Register a new account or login if you already have one

## Usage Guide

### Getting Started
1. **Register**: Create a new account with username, email, and password
2. **Login**: Sign in with your credentials
3. **Dashboard**: View your financial overview and recent transactions

### Adding Transactions
1. **Income**: Go to Income page → Fill form → Submit
2. **Expenses**: Go to Expenses page → Fill form → Submit
3. **Categories**: Select appropriate categories for better organization

### Setting Budgets
1. Go to Budget page
2. Select category and set amount
3. Choose period (monthly/yearly)
4. Save budget

### Viewing Reports
1. Go to Reports page
2. View interactive charts and analytics
3. Analyze spending patterns and trends

### Managing Goals
1. Go to Goals page
2. Create new financial goals
3. Set target amount and date
4. Track progress over time

## Database Schema

### Users Table
- `id`: Primary key
- `username`: Unique username
- `email`: Unique email address
- `password_hash`: Encrypted password
- `created_at`: Account creation timestamp
- `updated_at`: Last update timestamp

### Income Table
- `id`: Primary key
- `user_id`: Foreign key to Users
- `description`: Income description
- `amount`: Income amount
- `category`: Income category
- `income_date`: Date of income
- `created_at`: Entry creation timestamp

### Expenses Table
- `id`: Primary key
- `user_id`: Foreign key to Users
- `description`: Expense description
- `amount`: Expense amount
- `category`: Expense category
- `expense_date`: Date of expense
- `created_at`: Entry creation timestamp

### Budgets Table
- `id`: Primary key
- `user_id`: Foreign key to Users
- `category`: Budget category
- `amount`: Budget amount
- `period`: Budget period (monthly/yearly)
- `created_at`: Budget creation timestamp

### Goals Table
- `id`: Primary key
- `user_id`: Foreign key to Users
- `title`: Goal title
- `description`: Goal description
- `target_amount`: Target amount
- `current_amount`: Current progress amount
- `target_date`: Target completion date
- `created_at`: Goal creation timestamp

## Security Features

- **Password Hashing**: Passwords are encrypted using bcrypt
- **Session Management**: Secure user sessions with Flask-Login
- **Input Validation**: Form validation and sanitization
- **SQL Injection Protection**: Using SQLAlchemy ORM
- **CSRF Protection**: Built-in CSRF protection with Flask-WTF

## File Structure

```
finance_app/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── flow_diagram.md       # Application flow diagrams
├── README.md             # This file
├── templates/            # HTML templates
│   ├── base.html         # Base template with navigation
│   ├── index.html        # Landing page
│   ├── login.html        # Login page
│   ├── register.html     # Registration page
│   ├── dashboard.html    # Main dashboard
│   ├── income.html       # Income management
│   ├── expense.html      # Expense management
│   ├── budget.html       # Budget management
│   ├── reports.html      # Reports and analytics
│   ├── goals.html        # Financial goals
│   └── profile.html      # User profile
└── finance.db           # SQLite database (created automatically)
```

## Customization

### Adding New Categories
1. Edit the category options in the respective HTML templates
2. Update the database models if needed
3. Restart the application

### Styling Changes
1. Modify the CSS in `templates/base.html`
2. Update Bootstrap classes or add custom styles
3. Refresh the browser to see changes

### Database Changes
1. Modify the models in `app.py`
2. Delete the existing `finance.db` file
3. Restart the application to recreate the database

## Troubleshooting

### Common Issues

1. **Port already in use**
   - Change the port in `app.py`: `app.run(debug=True, port=5001)`

2. **Database errors**
   - Delete `finance.db` and restart the application

3. **Import errors**
   - Ensure all dependencies are installed: `pip install -r requirements.txt`

4. **Template errors**
   - Check that all template files are in the `templates/` directory
   - Verify template syntax and Jinja2 syntax

### Performance Tips

1. **Database Optimization**
   - Add indexes for frequently queried columns
   - Use database migrations for schema changes

2. **Caching**
   - Implement Redis caching for frequently accessed data
   - Cache chart data and reports

3. **Security Enhancements**
   - Use environment variables for sensitive data
   - Implement rate limiting
   - Add two-factor authentication

## Future Enhancements

- **Export Features**: Export data to CSV/PDF
- **Email Notifications**: Budget alerts and reminders
- **Mobile App**: React Native or Flutter mobile application
- **Multi-currency Support**: Support for different currencies
- **Recurring Transactions**: Automatic recurring income/expense entries
- **Bill Reminders**: Payment due date notifications
- **Investment Tracking**: Stock and investment portfolio management
- **Tax Reports**: Annual tax summary and reports

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is open source and available under the MIT License.

## Support

For support or questions, please create an issue in the repository or contact the development team.

---

**Happy Financial Management! 💰📊
