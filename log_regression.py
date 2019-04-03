#thank you to https://towardsdatascience.com/building-a-logistic-regression-in-python-step-by-step-becd4d56c9c8 for guidance
#this program executes all the steps leading up to the final log_regression...
#I split up my data into train and test, I encode my categorical variables properly...
#Recursive feature elimination is used on the variables I do have..
#The output of this process led me to update what columns I use for the final analysis
#Then we do the final analysis... Then print out its accuracy and a confusion matrix

import csv
import pandas as pd
import numpy as np
from sklearn import preprocessing
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split


input_file = "File_for_regression.csv"
df = pd.read_csv(input_file, header=0)
df = df.dropna()

count_loss = len(df[df['Outcome']==0])
count_win = len(df[df['Outcome']==1])
print(count_loss)
print(count_win)

print(df.shape)
print(list(df.columns))
print(df.head())
pd.set_option('display.max_columns', None)

#creating encoding for dummy versions of our categorical variables
cat_vars=['Home','OrderType']
for var in cat_vars:
	cat_list='var'+ '_' + var
	cat_list = pd.get_dummies(df[var], prefix=var, drop_first=True)
	df1=df.join(cat_list)
	df=df1

df_vars=df.columns.values.tolist()
to_keep=[i for i in df_vars if i not in cat_vars]
df_final = df[to_keep]
#our new categorical variable list
print(df_final.columns.values)

X = df_final.loc[:, df_final.columns != 'Outcome']
y = df_final.loc[:, df_final.columns == 'Outcome']

from imblearn.over_sampling import SMOTE

#breaking up our data into training and testing
os = SMOTE(random_state=0)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=0)
columns = X_train.columns

os_data_X,os_data_y=os.fit_sample(X_train, y_train.values.ravel())
os_data_X = pd.DataFrame(data=os_data_X,columns=columns )
os_data_y= pd.DataFrame(data=os_data_y,columns=['Outcome'])
#Checking the numbers of our oversampled data
print("length of oversampled data is ",len(os_data_X))
print("Number of lost matches in oversampled data",len(os_data_y[os_data_y['Outcome']==0]))
print("Number of won matches",len(os_data_y[os_data_y['Outcome']==1]))
print("Proportion of lost matches in oversampled data is ",len(os_data_y[os_data_y['Outcome']==0])/len(os_data_X))
print("Proportion of won matches in oversampled data is ",len(os_data_y[os_data_y['Outcome']==1])/len(os_data_X))

df_final_vars=df_final.columns.values.tolist()
y=['Outcome']
X=[i for i in df_final_vars if i not in y]

#now we begin fitting a model to our training data
from sklearn.feature_selection import RFE
from sklearn.linear_model import LogisticRegression

logreg = LogisticRegression(solver='lbfgs')

#using recursive feature elimination package to see what is really useless
rfe = RFE(logreg, 6)
rfe = rfe.fit(os_data_X, os_data_y.values.ravel())
print(rfe.support_)
print(rfe.ranking_)

#the following variables are really the only ones that show up as having promise 
#(neutral does also, but probably in large part because I encoded all of Pakistan's matches in the UAE as 'neutral' games)... 
#Bigger analyses of ODI match data seem to show a slight advantage batting first in day-night games...
#but this didn't show up in my data. Nevertheless, including the variable 'OrderType_1st. night' gives me a 1% prediction boost on my test data versus not including it
cols = ['RankAdvantage', 'BatAdvantage', 'BowlAdvantage', 'Home_home', 'OrderType_1st. night', 'OrderType_2nd. day']

X = os_data_X[cols]
y = os_data_y['Outcome']

import statsmodels.api as sm
logit_model=sm.Logit(y,X)
result=logit_model.fit()
print(result.summary2())

#now we finally do our logistic regression
from sklearn.linear_model import LogisticRegression
from sklearn import metrics

#splitting up data again, now that it has been updated
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=0)
logreg = LogisticRegression(solver='lbfgs')
logreg.fit(X_train, y_train)

y_pred = logreg.predict(X_test)
print('Accuracy of logistic regression classifier on test set: {:.2f}'.format(logreg.score(X_test, y_test)))

from sklearn.metrics import confusion_matrix
confusion_matrix = confusion_matrix(y_test, y_pred)
print(confusion_matrix)


