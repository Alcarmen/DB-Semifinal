from flask import Flask, render_template,request,url_for,redirect,session,flash
from dbhelper import *

app = Flask(__name__)
app.secret_key= '696969BRANDON696969'

app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    return response
	
@app.route("/logout")
def logout()->None:
	if "username" in session:
		session.pop("username")
		flash("Logged Out")
	return render_template("indexs.html",title="Welcome to Brandon's Book Store")

@app.route("/")
def main()->None:
	return render_template("indexs.html",title="Welcome to Brandon's Book Store")


@app.route('/home')
def home()->None:
    if "username" in session:
        return render_template("Home.html")
    else:
        flash("Login Properly")
        return render_template("index.html")


@app.route("/login", methods=['POST', 'GET'])
def login() -> None:
    if request.method == "POST":
        uname = request.form['username']
        pword = request.form['password']
        
        # Set a static user validation
        if uname == "admin" and pword == "123":
            session['username'] = uname
            return redirect(url_for("home"))
        else:
            flash("Invalid User")
            return render_template("login.html", title="Login Page")
    else:
        return render_template("login.html", title="Login Page")
    
@app.route('/Custom',methods=['GET','POST'])
def Custom():
    data = getall("customers")
    head:list= ['C_id','C_name','c_email','c_address', 'actions']       
      
    return render_template("index.html", student=data, header=head)
    
@app.route('/Item')
def Item():
    it= getall("items")
    head:list= ['id','ISBN','Title','Author','Genre', 'Price','I_Type', 'Action']

    return render_template("itemindex.html",item=it, header=head)
 
@app.route('/create', methods=['GET','POST'])
def create():
    if request.method == 'POST':
        c_name,c_email,c_address=dict(request.form).values()
        addrecord('customers',c_name=c_name, c_email=c_email, c_address=c_address)
        return redirect(url_for('Custom'))
    return render_template("Create.html")

@app.route('/createitem', methods=['GET','POST'])
def createitem():
    if request.method == 'POST':

        ISBN,title,author,genre,price,i_type=dict(request.form).values()
        addrecord('items',ISBN=ISBN,title=title,author=author,genre=genre,price=price,i_type=i_type)
        return redirect(url_for('Item'))
    return render_template("Item-Create.html")

@app.route('/update/<c_id>', methods=['GET','POST'])
def update(c_id):
    if request.method == 'POST':
        c_name,c_email,c_address=dict(request.form).values()
        updaterecord('customers',c_id=c_id,c_name=c_name, c_email=c_email, c_address=c_address)
        return redirect(url_for('Custom'))
       
    customer = None
    customers = getrecord('customers',c_id=c_id)
    if len(customers) > 0:
        customer = customers[0]
    return render_template("Update.html",customer=customer)

@app.route('/delete_cust/<c_id>',methods=['GET'])
def delete_cust(c_id):
    if request.method == 'GET':
        deleterecord('customers',c_id=c_id)
        return redirect(url_for("Custom"))

#-------ITEMS---------
@app.route('/update_item/<i_id>', methods=['GET','POST'])
def update_item(i_id):
    if request.method == 'POST':
        ISBN,title,author,genre,price,i_type=dict(request.form).values()
        updaterecord('items',ISBN=ISBN,title=title,author=author,genre=genre,price=price,i_type=i_type)
        return redirect(url_for('Item'))
       
    item = None
    items = getrecord('items',i_id=i_id)
    if len(items) > 0:
        item = items[0]
    return render_template("Item-Update.html",item=item)

@app.route('/delete_item/<i_id>',methods=['GET'])
def delete_item(i_id):
    if request.method == 'GET':
        deleterecord('items',i_id=i_id)
        return redirect(url_for("Item"))
        
@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        search_query = request.form.get('search_query')
        print("Search Query:", search_query)  # Check if the query is captured correctly

        results = searchrecord('customers', search_query)
        print("Results:", results)  # Check the results obtained

        if not results:
            # Implement an appropriate message or action when no results are found
            return render_template("NoResults.html")  # Create a NoResults.html template

        return render_template("Searched.html", results=results)

    return redirect(url_for("Custom"))

@app.route('/search_item', methods=['GET', 'POST'])
def search_item():
    if request.method == 'POST':
        item_searched = request.form.get('item_searched')
        print("Search Query:", item_searched)  # Check if the query is captured correctly

        output = itemrecord('items', item_searched)
        print("Results:", output)  # Check the results obtained

        if not output:
            # Implement an appropriate message or action when no results are found
            return render_template("NoResults.html")  # Create a NoResults.html template

        return render_template("Item-Search.html", output=output)

    return redirect(url_for("Item"))


        
if __name__=='__main__':
    
    app.run(debug=True)