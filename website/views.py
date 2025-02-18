from flask import Blueprint, render_template, request, flash, jsonify, redirect, url_for
from flask_login import login_required, current_user
from .models import Expenses, Revenues, User
from datetime import datetime
from . import db

# Create the blueprint to create a sort of standard view
views = Blueprint('views', __name__)

# route home page
@views.route('/', methods=['GET','POST'])
@login_required
def home():
    if request.method == 'GET':
        date_today = datetime.now().date()
        date_today = date_today.strftime("%Y-%m")
        expenses = Expenses.query.filter_by(date_month_ex=date_today)
        revenues = Revenues.query.filter_by(date_month_re=date_today)
        
        # Calculate the available amount
        Tot_revenues = 0
        for revenue in revenues:
            Tot_revenues = Tot_revenues + revenue.amount_revenue
        
        Tot_expenses = 0
        for expense in expenses:
            Tot_expenses = Tot_expenses + expense.amount_expense
        
        Tot_amount_available = Tot_revenues - Tot_expenses
        if Tot_amount_available < 0:
            flash("Tha amount available is negative", category='error')

        # return the month in letter
        month = date_today[5:] 
        match month:
            case "01":
                date_today = "January"
            case "02":
                date_today = "February"
            case "03":
                date_today = "March"
            case "04":
                date_today = "April"
            case "05":
                date_today = "May"
            case "06":
                date_today = "June"
            case "07":
                date_today = "July"
            case "08":
                date_today = "August"
            case "09":
                date_today = "September"
            case "10":
                date_today = "October"
            case "11":
                date_today = "November"
            case "12":
                date_today = "December"
            
        
        return render_template("accounting.html", expenses=expenses, user=current_user, revenues=revenues, date_today=date_today, Tot_amount_available=Tot_amount_available)
    
    if request.method == 'POST':
        date_month_filter = request.form.get('date_month_filter')
        if date_month_filter == "":
            date_month_filter = datetime.now().date()
            date_month_filter = date_month_filter.strftime("%Y-%m")
        
        expenses = Expenses.query.filter_by(date_month_ex=date_month_filter)
        revenues = Revenues.query.filter_by(date_month_re=date_month_filter)
        
        # Calculate the available amount
        Tot_revenues = 0
        for revenue in revenues:
            Tot_revenues = Tot_revenues + revenue.amount_revenue
        
        Tot_expenses = 0
        for expense in expenses:
            Tot_expenses = Tot_expenses + expense.amount_expense
        
        Tot_amount_available = Tot_revenues - Tot_expenses
        if Tot_amount_available < 0:
            flash("Tha amount available is negative", category='error')
            
        # return the month in letter
        month = date_month_filter[5:] 
        match month:
            case "01":
                date_month_filter = "January"
            case "02":
                date_month_filter = "February"
            case "03":
                date_month_filter = "March"
            case "04":
                date_month_filter = "April"
            case "05":
                date_month_filter = "May"
            case "06":
                date_month_filter = "June"
            case "07":
                date_month_filter = "July"
            case "08":
                date_month_filter = "August"
            case "09":
                date_month_filter = "September"
            case "10":
                date_month_filter = "October"
            case "11":
                date_month_filter = "November"
            case "12":
                date_month_filter = "December"
        
        return render_template("accounting.html", expenses=expenses, user=current_user, revenues=revenues, date_month_filter=date_month_filter, Tot_amount_available=Tot_amount_available)
        
        
# route to add data on the DB Revenues and Expenses
@views.route('/adddata', methods=['GET','POST'])
@login_required
def accounting():
    
    # Check for the method and fild to process the insert Expenses
    if request.method == 'POST' and request.form.get('company_name') != None:
        company_name = request.form.get('company_name')
        amount_expense = request.form.get('amount_expense')
        date_paid = request.form.get('date_paid')
        date_paid = datetime.strptime(date_paid, "%Y-%m-%d")
        date_month_ex = request.form.get('date_month_filter') 
        if date_month_ex == "":
            date_month_ex = datetime.now().date()
            date_month_ex = date_month_ex.strftime("%Y-%m")
        switch = request.form.get('switch')
        
        # checks before inseting the expense
        if company_name == "":
            flash("Please fill in the company", category='error')
        elif amount_expense == "":
            flash("Please fill in the amount", category='error')
        elif date_paid == "":
            flash("Please fill in the date", category='error')
        elif date_month_ex == "":
            flash("Please fill in the period date", category='error')
        elif switch == "":
            flash("Please fill in the switch", category='error')
        else:
            new_expenses = Expenses(company_name=company_name, amount_expense=amount_expense, date_paid=date_paid, date_month_ex=date_month_ex, switch_paid=switch)
            db.session.add(new_expenses)
            db.session.commit()
            flash('Expense added!', category='success')
    
    # Check for the method and fild to process the insert Revenues
    elif request.method == 'POST' and request.form.get('name') != None:
        name = request.form.get('name')
        amount_revenue = request.form.get('amount_revenue')
        date_received = request.form.get('date_received')
        date_received = datetime.strptime(date_received, "%Y-%m-%d")
        date_month_re = request.form.get('date_month_filter')
        if date_month_re == "":
            date_month_re = datetime.now().date()
            date_month_re = date_month_re.strftime("%Y-%m")
        switch = request.form.get('switch')
        
        # Checks before inserting the revenue
        if name == "":
            flash("Please fill the name of person", category='error')
        elif amount_revenue == "":
            flash("Please fill in the amount revenue", category='error')
        elif date_received == "":
            flash("Please fill in the date", category='error')
        elif date_month_re == "":
            flash("Please fill in the period date", category='error')
        elif switch == "":
            flash("Please fill in the switch", category='error')
        else:
            new_revenue = Revenues(name=name, amount_revenue=amount_revenue, date_received=date_received, date_month_re=date_month_re)   
            db.session.add(new_revenue)
            db.session.commit()
            flash('Revenue added!', category='success')
    
    # retourn a the template
    return render_template("adddata.html", user=current_user) 

# Handling the update of the Revenue
@views.route('/revenues_update/<int:id>', methods=['GET','POST'])
@login_required
def update_revenues(id):
    if request.method == 'GET':
        revenue_to_update = Revenues.query.get_or_404(id)
        revenue_id=revenue_to_update.id
        revenue_name=revenue_to_update.name
        revenue_amount=revenue_to_update.amount_revenue
        revenue_date=revenue_to_update.date_received
        revenue_date_period=revenue_to_update.date_month_re
        
        # return template to send all the information at the adddata.html
        return render_template("revenues_update.html", revenue_id=revenue_id, revenue_name=revenue_name, revenue_amount=revenue_amount, revenue_date_period=revenue_date_period, user=current_user)

# Handling the update of the Expense
@views.route('/expenses_update/<int:id>', methods=['GET','POST'])
@login_required
def update_expense(id):
    if request.method == 'GET':
        expense_to_update = Expenses.query.get_or_404(id)
        expense_id=expense_to_update.id
        expense_company_name=expense_to_update.company_name
        expense_amount=expense_to_update.amount_expense
        expense_date=expense_to_update.date_paid
        expense_date_period=expense_to_update.date_month_ex
        expense_switch=expense_to_update.switch_paid
        
        # return template to send all the information at the adddata.html
        return render_template("expenses_update.html", expense_id=expense_id, expense_company_name=expense_company_name, expense_amount=expense_amount, expense_date=expense_date, expense_date_period=expense_date_period, expense_switch=expense_switch, user=current_user)
    
# confirm the modification of the revenue
@views.route('/revenues_update/confirm', methods=['GET','POST'])
@login_required
def update_revenues_confirm():
    if request.method == 'POST':
        name = request.form.get('name')
        amount = request.form.get('amount_expense')
        id = request.form.get('id')
        date = request.form.get('date')
        
        # check if something has been changed to update the table Revenue
        revenue = Revenues.query.filter_by(id=id).first()
        if name != revenue.name:
            revenue.name = name
        if amount != revenue.amount_revenue:
            revenue.amount_revenue = amount
        if date != revenue.date_received:
            date_received = datetime.strptime(date, "%Y-%m-%d")
            revenue.date_received = date_received
        db.session.commit()
        
        # redirect at the view home
        return redirect(url_for('views.home'))
 
 # confirm the modification of the expense   
@views.route('/expenses_update/confirm', methods=['GET','POST'])
@login_required
def update_expense_confirm():
    if request.method == 'POST':
        name = request.form.get('name')
        amount = request.form.get('amount_expense')
        id = request.form.get('id')
        date = request.form.get('date')
        switch = request.form.get('switch')
        
        # check if something has been changed to update the table expense
        expense = Expenses.query.filter_by(id=id).first()
        if name != expense.company_name:
            expense.company_name = name
        if amount != expense.amount_expense:
            expense.amount_expense = amount
        if date != expense.date_paid:
            date_paid = datetime.strptime(date, "%Y-%m-%d")
            expense.date_paid = date_paid
        if switch != expense.switch_paid:
            expense.switch_paid = switch
        db.session.commit()
        
        # redirect at the view home
        return redirect(url_for('views.home'))

# delete button expense
@views.route('<int:id>/delete_expense',  methods=['POST'])
@login_required
def delete_expense_item(id):
    print("inside")
    expense = Expenses.query.filter_by(id=id).first()
    db.session.delete(expense)
    db.session.commit()
    flash('The expense has been deleted!', 'success')
    
    # redirect at the view home
    return redirect(url_for('views.home'))

# delete button revenue
@views.route('/<int:id>/delete_revenue',  methods=('POST',))
@login_required
def delete_revenue_item(id):
    revenue = Revenues.query.filter_by(id=id).first()
    db.session.delete(revenue)
    db.session.commit()
    flash('The expense has been deleted!', 'success')
    
    # redirect at the view home
    return redirect(url_for('views.home'))