import csv
from sklearn.naive_bayes import BernoulliNB
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score
from sklearn.neighbors import KNeighborsClassifier  
from sklearn.linear_model import LogisticRegression


# 读取csv文件
def read_csv(filename):
    with open(filename, encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        # all data
        data = [(row[1:]) for row in reader]
        # reduce data
        #data = [(row[1:3] + row[8:]) for row in reader]
        
        # 将比赛双方的数据整合为一条数据
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
    # 读取csv文件数据
    x_data, y_data = read_csv('all_data.csv')
    # 分割训练数据和测试数据
    # 训练数据
    train_x = x_data[:340]
    train_y = list(map(int, y_data[:340]))
    # 测试数据
    test_x = x_data[340:]
    test_y = list(map(int, y_data[340:]))

    # 将数据标准化
    scaler = StandardScaler() 
    scaler.fit(train_x)
    train_x = scaler.transform(train_x)  
    test_x = scaler.transform(test_x)

    # 使用不同方法进行训练和测试
    #######################    K近邻   #########################
    # 训练
    k_neighbour = KNeighborsClassifier(n_neighbors=3)
    k_neighbour.fit(train_x, train_y)
    # 预测
    print("**************************")
    predict_y_training = k_neighbour.predict(train_x)
    print("k近邻在训练数据准确率：")
    print(accuracy_score(predict_y_training, train_y))
    predict_y = k_neighbour.predict(test_x)
    print("k近邻预测准确率:")
    print(accuracy_score(predict_y, test_y))
    print("**************************")

    ########################   贝叶斯网络   ###########################
    # 训练
    NB = BernoulliNB()
    NB.fit(train_x, train_y)
    # 预测
    print("**************************")
    predict_y = NB.predict(test_x)
    predict_y_training = NB.predict(train_x)
    print("贝叶斯在训练数据准确率：")
    print(accuracy_score(predict_y_training, train_y))
    print("贝叶斯网络预测准确率:")
    print(accuracy_score(predict_y, test_y))
    print("**************************")

    ######################    logit回归    #######################
    # 训练
    lr = LogisticRegression()
    lr.fit(train_x, train_y)
    # 预测
    print("**************************")
    predict_y_training = lr.predict(train_x)
    print("Logit回归在训练数据准确率：")
    print(accuracy_score(predict_y_training, train_y))
    predict_y = lr.predict(test_x)
    print("Logit回归预测准确率:")
    print(accuracy_score(predict_y, test_y))
    print("**************************")
    


    