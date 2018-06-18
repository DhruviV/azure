from flask import Flask, render_template, request
import time
import pypyodbc

app = Flask(__name__)
app.secret_key = "Secret"

connection = pypyodbc.connect("Driver={ODBC Driver 13 for SQL Server};Server=tcp:cloudtestdb.database.windows.net,1433;Database=cloudtest;Uid=shashank@cloudtestdb;Pwd=Cloud@6331;")
cursor = connection.cursor()


@app.route('/')
def index():
    cursor.execute("insert into Producer values ('Producer',GETDATE())")
    connection.commit()
    results = cursor.execute("Select * from Producer")
    return render_template('index.html',results=results)


if __name__ == '__main__':
    app.run(debug=True)
