from tkinter import *
from tkinter import scrolledtext
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression 
from matplotlib import pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from functools import partial
from sklearn.cluster import KMeans
import numpy as np
import tkinter as tk
from tkinter import ttk
import pandas as pd
import os


#Regresion lineal
def ejecutarConcurrente(n,url):
	
	com="ab -n "+str(n)+" -c "+str(n)+" -e reporteConcurrente.csv "+url
	res=os.popen(com).read()
	print(res)

	filename="reporteConcurrente.csv"
	names=["Porcentaje","Tiempo"]
	df=pd.read_csv(filename, names=names, delimiter=",", header=0)
	txt.delete("0.0",tk.END)
	txt.insert(tk.END,df)
	txt.insert(tk.END,"\n\n")

	fig=plt.figure(figsize=(4.2,3))
	ax=fig.gca()

	array=df.values
	X_reg=array[:,0:1]
	Y_reg=array[:,1:2]

	test_size=0.2
	seed=8
	X_train, X_test, Y_train, Y_test=train_test_split(X_reg, Y_reg, test_size=test_size, random_state=seed)
	#X_train
	model=LinearRegression()
	#Entrenamos el modelo con los datos de training
	model.fit(X_train, Y_train)

	interc=model.intercept_[0]
	coef=model.coef_[0][0]

	if(interc>=0):
		y_cad="y = "+str(coef)+"x + " + str(interc)
		txt.insert(tk.END,"ECUACIÓN:\n")
		txt.insert(tk.END, y_cad)
	else:
		y_cad="y = "+str(coef)+"x - " + str(-interc)
		txt.insert(tk.END,"ECUACIÓN:\n")
		txt.insert(tk.END, y_cad)

	Y_pred=model.predict(X_test)
	#print(f"Prediccion {Y_pred}")
	#print(f"Lo que debería darnos es {Y_test}")

	plt.scatter(X_train, Y_train, color='b')
	#Curva de regresion
	X_min=X_train.min()
	X_max=X_train.max()
	Y_min=X_min*coef+interc
	Y_max=X_max*coef+interc
	plt.plot([X_min, X_max], [Y_min, Y_max], color='r')
	
	plt.title("RL Peticiones concurrentes")
	plt.grid()
	canvas=FigureCanvasTkAgg(fig, master=root)
	plot_widget=canvas.get_tk_widget()
	plot_widget.place(x=350,y=100)



#Clustering
def ejecutarSecuencial(n,url):
		
	com="ab -n "+str(n)+" -e reporteSecuencial.csv "+url
	res=os.popen(com).read()
	print(res)

	filename="reporteSecuencial.csv"
	names=["Porcentaje","Tiempo"]
	df=pd.read_csv(filename, names=names, delimiter=",", header=0)
	txt.delete("0.0",tk.END)
	txt.insert(tk.END,df)

	fig=plt.figure(figsize=(4.2,3))
	ax=fig.gca()

	clusters=int(comboBox.get())
	arr=df.values
	X=arr[:,0:1]
	Y=arr[:,1:2]
	kmeans=KMeans(n_clusters=clusters)
	kmeans.fit(arr)
	x_centroid=[]
	y_centroid=[]

	for x,y in kmeans.cluster_centers_:
		x_centroid.append(x)
		y_centroid.append(y)

	color_map = {0 : 'c', 1 : 'purple', 2 : 'b'}
	label_color = [color_map[i] for i in kmeans.labels_]
	plt.scatter(x_centroid,y_centroid, c="r")
	plt.scatter(X,Y, c=label_color)
	plt.title("Clustering Peticiones secuenciales")
	plt.grid()

	canvas=FigureCanvasTkAgg(fig, master=root)
	plot_widget=canvas.get_tk_widget()
	plot_widget.place(x=350,y=100)


root = Tk()
root.geometry("760x480+100+100")

Label(root, text="PROYECTO FINAL").place(x=300, y=10)

Label(root, text="# Peticiones").place(x=50, y=35)
num=Entry(root, width=12, text="")
num.place(x=50, y=60)
num.insert(END,"")

Label(root, text="URL").place(x=150, y=35)
url=Entry(root, width=22, text="")
url.place(x=150, y=60)
url.insert(END,"")

btnEjecutar = Button(root,command=lambda: ejecutarConcurrente(num.get(),url.get()),text="Ejecutar Concurrente")
btnEjecutar.place(x=350, y=60)

btnSecuencial = Button(root,command=lambda: ejecutarSecuencial(num.get(),url.get()),text="Ejecutar Secuencial")
btnSecuencial.place(x=500, y=60)

Label(root, text="Número de clusters(Peticiones secuenciales)").place(x=50, y=110)
comboBox = ttk.Combobox(root, values=["2", "3"], state="readonly")
comboBox.grid(padx=50, pady=130)
comboBox.current(0)

Label(root, text="Tiempo / Peticiones(%)").place(x=50, y=170)
txt=scrolledtext.ScrolledText(root, width=33, height=18)
txt.place(x=50, y=190)


mainloop()
