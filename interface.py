import numpy as np
import pandas as pd
import pickle
from tkinter import *
from tkinter.filedialog import askopenfilename
from tkinter import messagebox
from sklearn.feature_selection import SelectFromModel
from sklearn import preprocessing

class App():
	def __init__(self, master):
		frame = Frame(master, background="red")

		self.l1 = Label(text="Select the input file to Classify", font=("Times", 16))
		#self.l1.grid(row=0, sticky=E)
		self.l1.pack()
		self.button = Button(main, text='Select File', foreground="white",background="black")
		self.button.bind("<Button-1>", self.ask)
		#self.button.grid(row=1)
		self.button.pack()

	def ask(self, event):
		Tk().withdraw() # we don't want a full GUI, so keep the root window from appearing
		file = askopenfilename() # show an "Open" dialog box and return the path to the selected file

		# Check File type
		if file.endswith('.xlsx'):
			data = pd.read_excel(file)
			App.classify(data)
		elif file.endswith('.csv'):
			data = pd.read_csv(file)
			App.classify(data)
		else:
			answer = messagebox.askokcancel("Question","Invalid file, Want to try again?")
			if answer:
				quit()
				App.__init__(self, master)
			else:
				quit()
	
	def classify(data):
		X = pre_process(data)
		feat = pickle.load(open('feature_select.sav','rb'))
		model = SelectFromModel(feat, prefit=True)
		data_new = model.transform(X)

		loaded_model = pickle.load(open('finalized_model.sav', 'rb'))
		pred = loaded_model.predict(data_new)
		if(pred):
			messagebox.showinfo("Result:","Diagnosed Positively")
		else:
			messagebox.showinfo("Result:","Diagnosed Negatively")
		quit()


def pre_process(data):
	# Drop irrelevant columns
	data = data.drop(['id','gender'],1)

	column = data.columns
	scaler = preprocessing.MinMaxScaler()

	# Scaling only required columns
	for col in column:
		if data[col].max() > 100:
			float_array = data[[col]].values.astype(float)
			scaled_array = scaler.fit_transform(float_array)
			data[[col]]= pd.DataFrame(scaled_array)   

	return data

main = Tk()
#s = Style()
app = App(main)
main.mainloop()