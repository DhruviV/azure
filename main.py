from copy import deepcopy

from flask import Flask, render_template, request
import pypyodbc
import numpy as np
import scipy
import math
import itertools
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
     fare = []
     for row in rows:
         pclass.append(row[0])
         survival.append(row[1])
         if row[11] == '':
             boat.append(0)
         else:
             boat.append(row[11])
         if row[4] == '' or row[4]== None:
             age.append(0)
         else:
             age.append(row[4])
         if row[8] == '' or row[8]== None:
             fare.append(0)
         else:
             fare.append(row[8])

     connection.close()
     print('\nPCLASS --------', pclass)
     print('\nsurvival --------', survival)
     print('\nage --------', age)
     print('\nfare --------', fare)

     X = np.array(list(zip(age[:len(age) - 1], fare[:len(fare) - 1])))
     print(X)


     km = KMeans(n_clusters=int(k))
     km.fit(X)
     centroids = km.cluster_centers_
     labels = km.labels_
     dhruvi={i: X[np.where(km.labels_ == i)] for i in range(km.n_clusters)}
     print(dhruvi)

     colors = ["g.", "r.", "b.", "y." "c.", "m.", "k.", "w."]

     # for i in range(len(X)):
     #     plt.plot(X[i][0], X[i][1], colors[labels[i]], markersize = 10)
     # plt.scatter(centroids[:,0],centroids[:,1],marker = "x", s = 150, linewidths=5, zorder = 10)
     displaylist = list(zip(age,fare,labels))
     print('\n\nDisplay List------------------------------------', displaylist)
     dist_list = []
     for i in range(0, len(centroids) - 1):
         for j in range(i + 1, len(centroids)):
             # print(centroids[i],centroids[j])
             x1 = centroids[i][0]
             x2 = centroids[j][0]
             y1 = centroids[i][1]
             y2 = centroids[j][1]
             temp = (x1 - x2)*(x1 - x2) + (y1 - y2)*(y1 - y2)
             dist = math.sqrt(temp)
             print(dist)
             dist_list.append(list(zip(centroids[i][:], centroids[j][:], itertools.repeat(dist))))

     print(dist_list)
     dist_len = len(dist_list)

     return render_template('output.html', my=displaylist, centroid=centroids, distances = dist_list, length=dist_len)
if __name__ == '__main__':
   app.run(debug = True)
