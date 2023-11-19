from flask import Blueprint, render_template, request, flash, redirect, url_for, Flask


Customer = Blueprint('Customer',__name__)


@Customer.route('/')
def home():
    return render_template("Home.html")
@Customer.route('/Custom')
def Custom():
    return render_template("Customer.html")
@Customer.route('/Item')
def Item():
    return render_template("Item.html")
    
    