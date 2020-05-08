import pandas as pd

#Reading File from Excel
data = pd.read_excel('CHP with PSA.xlsx')

#Column Names
headers = data.columns

#Checking for Empty Columns
empty = []
for e in headers:
    if all(data[e].isna()):
        empty.append(e)

#removing unncessary columns
data = data.drop(empty, axis=1)


#removing rows with empty 'LabParamFinalResult'
check = data['LabParamFinalResult'].isnull()
rm = []
for i in range(len(check)):
    if check[i]:
        rm.append(i)
data = data.drop(rm)

#Converting processed data to csv file
data.to_csv('output.csv',mode='w',date_format='%d-%m-%Y %H-%M')



