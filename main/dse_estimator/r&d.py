import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import math
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_squared_error
from keras.models import Sequential
from keras.layers import Dense, Activation
from keras.layers import LSTM, Dropout
# import preprocessing


feature_columns = ["opening_price","High","Low","Close","OHLC_avg"]
# feature_columns=["Close", "OHLC_avg"]
columns_to_be_predicted="OHLC_avg"
#columns_to_be_predicted="Close"
filename = 'dse_1JANATAMF_data_2014-2020.csv'
dataset = pd.read_csv(filename)
# print(dataset.head(20))
# print(dataset.info())
# print(dataset.dtypes)

# OHLC_avg = (dataset['yesterdays_closing_price']+dataset['High']+dataset['Low']+dataset['Close'])/4

OHLC_avg = dataset[['yesterdays_closing_price', 'High', 'Low', 'Close']].mean(axis = 1)

HLC_avg = dataset[['High', 'Low', 'Close']].mean(axis = 1)

OHLC_avg = np.reshape(OHLC_avg.values, (len(OHLC_avg),1))
scaler = MinMaxScaler(feature_range=(0, 1))
OHLC_avg = scaler.fit_transform(OHLC_avg)
# OHLC_avg = OHLC_avg.reshape(1,len(OHLC_avg))
OHLC_avg = pd.DataFrame(OHLC_avg, columns=["OHLC_avg"])
# print(OHLC_avg)

# new_df = pd.DataFrame({'OHLC_avg':OHLC_avg,'HLC_avg':HLC_avg}).reset_index()

dataset = pd.concat([dataset, OHLC_avg], axis = 1)
print("dataset",dataset.info())

original_y = dataset[[columns_to_be_predicted]]

# columns_to_drop = [dataset.columns[0],"trading_code","value_mn","volume","yesterdays_closing_price","date","trade","last_traded_price"]

# classifier_df = dataset.drop(columns_to_drop,axis=1)
classifier_df = dataset[feature_columns].copy()

print("classifier",classifier_df.info())
#High    Low  opening_price  Close  OHLC_avg
#train_x= HIgh Low  opening_price  Close
#train_y= OHLC_avg
train_size = int(len(classifier_df)*0.75)
test_size = len(classifier_df) - train_size
train_df, test_df = classifier_df[0:train_size], classifier_df[train_size:]
print("train_df", train_df)
print("test_df", test_df)

train_x = train_df.iloc[:,train_df.columns!=columns_to_be_predicted]
train_y = train_df.iloc[:,train_df.columns==columns_to_be_predicted]

 # train_x = train_df.iloc[:len(train_df)-1,train_df.columns!=columns_to_be_predicted]
 # train_y = train_df.iloc[1:,train_df.columns==columns_to_be_predicted]

print("train_x", train_x)
print("train_y", train_y)
test_x = test_df.iloc[:,test_df.columns!=columns_to_be_predicted]
test_y = test_df.iloc[:,test_df.columns==columns_to_be_predicted]

# original_y = train_y + test_y
# print('original y', original_y)

train_x = np.reshape(train_x.values, (train_x.shape[0], 1, train_x.shape[1]))
test_x = np.reshape(test_x.values, (test_x.shape[0], 1, test_x.shape[1]))

model = Sequential()
model.add(LSTM(64, input_shape=(train_x.shape[1], train_x.shape[2]), return_sequences = True))
# model.add(LSTM(16))
model.add(LSTM(32))
# model.add(Activation('linear'))
model.add(Dense(1))
model.add(Activation('linear'))


# model = Sequential ()
# d=0.3
# model.add(LSTM(256, input_shape=(train_x.shape[1], train_x.shape[2]), return_sequences=True))
# model.add(Dropout(d))
# model.add(LSTM(256, input_shape=(train_x.shape[1], train_x.shape[2]), return_sequences=False))
# model.add(Dropout(d))
# model.add(Dense(32,kernel_initializer='uniform', activation='relu'))
# model.add(Dense(1,kernel_initializer='uniform', activation = 'linear'))

model.compile(loss='mean_squared_error', optimizer='adagrad', metrics=['accuracy']) # Try SGD, adam, adagrad and compare!!!
history = model.fit(train_x, train_y, epochs=50, batch_size=10, validation_data=(test_x, test_y),verbose=2, shuffle=False)

plt.plot(history.history['loss'], label='train')
plt.plot(history.history['val_loss'], label='test')
plt.legend()
plt.show()
model.save("mymodel")
trainPredict = model.predict(train_x)
testPredict = model.predict(test_x)
print("testPredict", len(trainPredict), len(testPredict))
print(testPredict)

step_size=1
# CREATING SIMILAR DATASET TO PLOT TRAINING PREDICTIONS
trainPredictPlot = np.empty_like(OHLC_avg)
trainPredictPlot[:, :] = np.nan
trainPredictPlot[step_size:len(trainPredict)+step_size, :] = trainPredict

# CREATING SIMILAR DATASSET TO PLOT TEST PREDICTIONS
testPredictPlot = np.empty_like(OHLC_avg)
testPredictPlot[:, :] = np.nan
testPredictPlot[len(trainPredict):len(trainPredict)+len(testPredict), :] = testPredict

####scaled
plt.plot(original_y, 'g', label ='original '+ columns_to_be_predicted)
plt.plot(trainPredictPlot, 'r', label = 'predicted training set')
plt.plot(testPredictPlot, 'b', label = 'predicted stock price/test set')
plt.legend(loc = 'upper right')
plt.xlabel('Time in Days')
plt.ylabel(columns_to_be_predicted + ' Value of ' + filename)
plt.show()

#***************************
#Predict OHLC, but in original data, plot the close value
temp_y = dataset[['Close']]
temp_y = scaler.fit_transform(temp_y)
temp = 'Close'
plt.plot(temp_y, 'g', label ='original '+ temp)
plt.plot(trainPredictPlot, 'r', label = 'predicted training set')
plt.plot(testPredictPlot, 'b', label = 'predicted stock price/test set')
plt.legend(loc = 'upper right')
plt.xlabel('Time in Days')
plt.ylabel(columns_to_be_predicted + ' Value of ' + filename)
plt.show()

############--------------------------------------------------------------------#######

# DE-NORMALIZING FOR PLOTTING
trainPredict = scaler.inverse_transform(trainPredict)
testPredict = scaler.inverse_transform(testPredict)
# print(train_y)
# train_y = scaler.inverse_transform([train_y])
# test_y = scaler.inverse_transform([test_y])


# TRAINING RMSE
# trainScore = math.sqrt(mean_squared_error(train_y[0], trainPredict[:,0]))
# print('Train RMSE: %.2f' % (trainScore))

# TEST RMSE
# testScore = math.sqrt(mean_squared_error(test_y[0], testPredict[:,0]))
# print('Test RMSE: %.2f' % (testScore))

# CREATING SIMILAR DATASET TO PLOT TRAINING PREDICTIONS
trainPredictPlot = np.empty_like(OHLC_avg)
trainPredictPlot[:, :] = np.nan
trainPredictPlot[1:len(trainPredict)+1, :] = trainPredict

# CREATING SIMILAR DATASSET TO PLOT TEST PREDICTIONS
testPredictPlot = np.empty_like(OHLC_avg)
testPredictPlot[:, :] = np.nan
testPredictPlot[len(trainPredict):len(trainPredict)+len(testPredict), :] = testPredict

# DE-NORMALIZING MAIN DATASET
OHLC_avg = scaler.inverse_transform(OHLC_avg)
original_y = scaler.inverse_transform(original_y)
###########denormalization
# PLOT OF MAIN OHLC VALUES, TRAIN PREDICTIONS AND TEST PREDICTIONS
plt.plot(original_y, 'g', label = 'original '+columns_to_be_predicted)
plt.plot(trainPredictPlot, 'r', label = 'predicted training set')
plt.plot(testPredictPlot, 'b', label = 'predicted stock price/test set')
plt.legend(loc = 'upper right')
plt.xlabel('Time in Days')
plt.ylabel(columns_to_be_predicted + ' Value of '+ filename)
plt.show()

# PREDICT FUTURE VALUES
last_val = testPredict[-1]
last_val_apan=test_x[-1]

print("last_val", last_val, last_val_apan)
last_val_scaled = last_val/last_val
next_val = model.predict(np.reshape(last_val_apan, (1,last_val_apan.shape[0],last_val_apan.shape[1])))
print("next_val", next_val, scaler.inverse_transform(next_val) )
# print("Last Day Value:", np.asscalar(last_val))
# print("Next Day Value:", np.asscalar(last_val*next_val))
# print np.append(last_val, next_val)

#RMSE ---- ber korte parinai
#TODO
#---- closing price predict korbo
#---- func banano drkr jeno feature er nam bole dile kaj kore
#---- notun feature gula diye predict korle kemon ashe seta dkhbo(TANVIR)
#---- amra ajker data niye ajker ta predict kortesi, amader ajker data niye kalker ta predict kora lagbe