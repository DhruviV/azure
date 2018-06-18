from copy import deepcopy
import numpy as np
from flask import Flask, render_template, request,flash,url_for

import pypyodbc
import scipy
from sklearn.cluster import KMeans



app = Flask(__name__)
app.secret_key = "Secret"

connection = pypyodbc.connect("Driver={ODBC Driver 13 for SQL Server};Server=tcp:dhruvi.database.windows.net,1433;Database=Dhruvi;Uid=dhruvi@dhruvi;Pwd=Shivangi@27;")
cursor = connection.cursor()

@app.route('/')
def index():
   return render_template('index.html')

@app.route('/search', methods=['POST', 'GET'])
def search():
     k = request.args.get("k")
     cursor.execute("Select * from titanic3")
     rows=cursor.fetchall()
     pclass = []
     boat = []
     survival = []
     age = []
     for row in rows:
         pclass.append(row[0])
         survival.append(row[1])
         if row[11] == '':
             boat.append(0)
         else:
             boat.append(row[11])
         if row[4] == '':
             age.append(0)
         else:
             age.append(row[4])
     connection.close()
     print('\nPCLASS --------', pclass)
     print('\nsurvival --------', survival)
     print('\nage --------', age)

     X = np.array(list(zip(survival[:len(survival) - 1], pclass[:len(pclass) - 1])))
     print('\n\n X -------------------------------------', X)

     km = KMeans(n_clusters=int(k))
     km.fit(X)
     centroids = km.cluster_centers_
     labels = km.labels_
     print(centroids)
     print(labels)
     colors = ["g.", "r.", "b.", "y." "c.", "m.", "k.", "w."]

     # for i in range(len(X)):
     #     plt.plot(X[i][0], X[i][1], colors[labels[i]], markersize = 10)
     # plt.scatter(centroids[:,0],centroids[:,1],marker = "x", s = 150, linewidths=5, zorder = 10)
     displaylist = list(zip(pclass, survival, labels))
     print('\n\nDisplay List------------------------------------', displaylist)


     return render_template('index.html', ci=displaylist, c2=centroids)
if __name__ == '__main__':
   app.run(debug = True)
