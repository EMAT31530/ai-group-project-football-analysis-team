import csv
import os
from sklearn.naive_bayes import BernoulliNB
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score
from sklearn.neighbors import KNeighborsClassifier  
from sklearn.linear_model import LogisticRegression
from data_scrapy import scrapy_data


# Read csv file
def read_csv(filename):
    with open(filename, encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        # all data
        data = [(row[1:]) for row in reader]
        # reduce data
        #data = [(row[1:3] + row[8:]) for row in reader]
        
        # Integrate the data of both parties into one piece of data
        x_data = []
        y_data = []
        for i in range(int(len(data)/2)):
            x_data.append(list(map(float, data[2*i][:-1])) + list(map(float, data[2*i + 1][:-1])))
            y_data.append(data[2*i][-1])
        
        # one_hot encode
        x_data = []
        for i in range(int(len(data)/2)):
            temp_x = []
            for j in range(len(data[0]) - 1):
                if data[2*i][j] > data[2*i + 1][j]:
                    temp_x.append(1)
                elif data[2*i][j] == data[2*i + 1][j]:
                    temp_x.append(0)
                else:
                    temp_x.append(-1)
            x_data.append(temp_x)
        
        #print(x_data)
         
        return x_data, y_data

if __name__ == '__main__':
    # First determine whether there is a game data file in the folder
    if not os.path.exists('all_data.csv'):
        scrapy_data()

    # Read csv file data
    x_data, y_data = read_csv('all_data.csv')
    # Split training data and test data
    # Training data
    train_x = x_data[:340]
    train_y = list(map(int, y_data[:340]))
    # Test Data
    test_x = x_data[340:]
    test_y = list(map(int, y_data[340:]))

    # Standardize data
    scaler = StandardScaler() 
    scaler.fit(train_x)
    train_x = scaler.transform(train_x)  
    test_x = scaler.transform(test_x)

    # Use different methods for training and testing
    #######################    K neighbors   #########################
    # training
    k_neighbour = KNeighborsClassifier(n_neighbors=3)
    k_neighbour.fit(train_x, train_y)
    # prediction
    print("**************************")
    predict_y_training = k_neighbour.predict(train_x)
    print("Accuracy of k nearest neighbors in training data：")
    print(accuracy_score(predict_y_training, train_y))
    predict_y = k_neighbour.predict(test_x)
    print("k nearest neighbor prediction accuracy:")
    print(accuracy_score(predict_y, test_y))
    print("**************************")

    ########################   Bayesian network   ###########################
    # training
    NB = BernoulliNB()
    NB.fit(train_x, train_y)
    # prediction
    print("**************************")
    predict_y = NB.predict(test_x)
    predict_y_training = NB.predict(train_x)
    print("Bayesian accuracy in training data:")
    print(accuracy_score(predict_y_training, train_y))
    print("Bayesian network prediction accuracy:")
    print(accuracy_score(predict_y, test_y))
    print("**************************")

    ######################    logit regression    #######################
    # training
    lr = LogisticRegression()
    lr.fit(train_x, train_y)
    # prediction
    print("**************************")
    predict_y_training = lr.predict(train_x)
    print("Logit regression accuracy rate on training data:")
    print(accuracy_score(predict_y_training, train_y))
    predict_y = lr.predict(test_x)
    print("Logit regression prediction accuracy:")
    print(accuracy_score(predict_y, test_y))
    print("**************************")
    


    