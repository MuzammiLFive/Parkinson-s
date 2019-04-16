import numpy as np
import pandas as pd
from sklearn import preprocessing
from sklearn.ensemble import AdaBoostClassifier
import pickle
from sklearn.feature_selection import SelectFromModel
from sklearn.metrics import accuracy_score 
filename = 'finalized_model.sav'

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

def feature_selection(X, y):
	# Creating instance of AdaBoost Classifier
	clf_feat =  AdaBoostClassifier(n_estimators=100,learning_rate=1.2,random_state=2)

	# Fitting data to the model
	clf_feat = clf_feat.fit(X, y)
	pickle.dump(clf_feat, open('feature_select.sav', 'wb'))

	# Selecting important features for the algorithm
	model = SelectFromModel(clf_feat, prefit=True)
	X_new = model.transform(X)

	# getting selected column names
	feature_idx = model.get_support()
	feature_name = df.columns[feature_idx]

	# Saving the new transformed data
	df_new = pd.DataFrame(X_new,columns=feature_name)
	df_new['class'] = df['class']
	return df_new

def prediction(df_new):
	# Training the algorithm
	clf = AdaBoostClassifier(n_estimators=300,learning_rate=0.3, random_state=5).fit(features,label)
	
	# Saving the model to the disk
	pickle.dump(clf, open(filename, 'wb'))


#--------------------MAIN--------------------#
# Read data5
df = pd.read_csv('pd_speech_features_set.csv')

data = pre_process(df)

#Splitting features and class labels
X, y = data.drop(['class'],1), data['class']

df_new = feature_selection(X, y)

# Splitting the Dataset into training and testing set
test_size = 0.3
train_data = df_new[:-int(test_size*len(df_new))]
test_data =  df_new[-int(test_size*len(df_new)):]
features = train_data.drop(['class'],1)
label = train_data['class']
test_features = test_data.drop(['class'],1)
test_label = test_data['class']

prediction(df_new)

# load the model from disk
loaded_model = pickle.load(open(filename, 'rb'))
pred = loaded_model.predict(test_features)

print("Accuracy:", 100*accuracy_score(test_label, pred))