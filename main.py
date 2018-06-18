from flask import Flask, render_template, request
import time
import pypyodbc

app = Flask(__name__)
app.secret_key = "Secret"

connection = pypyodbc.connect("Driver={ODBC Driver 13 for SQL Server};Server=tcp:dhruvi.database.windows.net,1433;Database=Dhruvi;Uid=dhruvi@dhruvi;Pwd=Shivangi@27;")
cursor = connection.cursor()


@app.route('/')
def index():

    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)
