

import os
import sqlite3

from flask import Flask
from flask import render_template
from flask import request
from flask import redirect
from flask import url_for

project_dir=os.path.dirname(os.path.abspath(__file__))
database_file=os.path.join(project_dir,"todo.db")
img_incomplete=os.path.join(project_dir,"check-mark_bw.png")
img_complete=os.path.join(project_dir,"check-mark_cl.png")
img_delete=os.path.join(project_dir,"delete-mark_br.png")

app=Flask(__name__)

class Todo():
    def add_record(self,item_text,item_status):
        con=sqlite3.connect(database_file)
        cur=con.cursor()
        cur.execute("INSERT INTO tbl_todo_list (item_text,item_status) VALUES (?,?)",(item_text,item_status))
        con.commit()
        con.close()
        return None
    
    def get_record(self,status):
        con=sqlite3.connect(database_file)
        cur=con.cursor()
        cur.execute("SELECT * FROM tbl_todo_list Where item_status="+str(status))
        records=cur.fetchall()
        con.close()
        return records
    
    def update_record(self,id,status):
        con=sqlite3.connect(database_file)
        cur=con.cursor()
        cur.execute("UPDATE tbl_todo_list SET item_status=" + str(status) + " WHERE item_id=" + id) 
        con.commit()
        con.close()
        return None
    
    def delete_record(self,id):
        con=sqlite3.connect(database_file)
        cur=con.cursor()
        cur.execute("DELETE FROM tbl_todo_list WHERE item_id=" + id)
        con.commit()
        con.close()
        return None

@app.route("/")
def index():
    td=Todo()
    incomp=td.get_record(False)
    comp=td.get_record(True)
    return render_template("index.html",incomplete=incomp,complete=comp,img_incomplete=img_incomplete,img_complete=img_complete,img_delete=img_delete)

@app.route("/add",methods=['POST'])
def add():
    td=Todo()
    td.add_record(request.form['todoitem'],False)
    return redirect(url_for('index'))

@app.route("/complete/<id>",methods=['GET','POST'])
def complete(id):
    td=Todo()
    td.update_record(id,True)
    return redirect(url_for('index'))

@app.route("/delete/<id>",methods=['GET','POST'])
def delete(id):
    td=Todo()
    td.delete_record(id)
    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(debug=True)
