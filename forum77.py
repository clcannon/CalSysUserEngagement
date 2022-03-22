from connect import get
from feature import get_net, show_net
# from getFeatures import get_f1,get_f2,get_f3
import networkx
import pandas as pd
from sklearn.model_selection import train_test_split
from Learning import trainall
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import r2_score
from sklearn.metrics import confusion_matrix

net = get_net("pickleX77.p")

def get_f1(user):
    return list(net.neighbors(user))


def get_f3(users): # G.out_degree(1) average
    sum = 0
    for usr in users:
        sum += (net.in_degree(usr))
        
    if len(users) == 0:
        return 0
    else:
        return sum/len(users)    


forum = get('forum77', 'topics_id, users_id')

thread = get('forum77usercount', 'topics_id', modifier= 'where users > 10') # needs to be distinct
topic_list = thread['topics_id'].to_list()

positive_users = []
for topic in topic_list:
    users = forum[forum['topics_id'] == topic]['users_id'].to_list() 
    #positive_users.append(list(set(users))) #set
    positive_users.extend(users) #set

positive_users = list(set(positive_users))
print(len(positive_users))

negative_users = []

for user in positive_users:
    
    user_neighbors = list(net.neighbors(user))
    negative_users.extend(user_neighbors)

negative_users = list(set(negative_users))
com = list(set(negative_users) - set(positive_users))
print(len(com))
#user id, feature 1, feature 3, class label

#create postive dataset
data = []

for p in positive_users:
    ActiveUsers = (get_f1(p))
    if len(ActiveUsers) ==0:
        print("found" + str(p))
    else:
        AiNoAN = get_f3(ActiveUsers)
        data.append([p, len(ActiveUsers), int(AiNoAN), 1])

#create negative dataset

for n in negative_users:
    ActiveUsers = (get_f1(p))
    AiNoAN = get_f3(ActiveUsers)
    data.append([p, len(ActiveUsers), int(AiNoAN), 0])

  
df = pd.DataFrame(data, columns=['user_id', 'F1', 'F3', 'Class'])
df.to_csv('dataset.csv',header=True,index=False)



dataSet = pd.read_csv('dataset.csv')
Y = dataSet.pop('Class') # Class
X = dataSet.drop('user_id',axis = 1)
X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size = 0.3, random_state = 60)
# trainall(X_train, X_test, Y_train, Y_test)




#Creating the Model (Optimised)
model = RandomForestClassifier(max_depth=2, random_state=0)
model.fit(X_train,Y_train)
Y_pred = model.predict(X_test)
conf = round((r2_score(Y_test,Y_pred))*100,3)

# Printing Confidence of Our Model
print('Model Confidence : ' , conf)
print('Confusion Matrix : \n' , confusion_matrix(Y_test, Y_pred))


#Improvement: More features(ex.PNE), more users, more topics, imbalanced dataset/more realistic.

#Questions for Marin: What is PNE? Need access to database with forum 77! How to get root neighbor for negative samples?

#needs to be distinct
#negative users need to have same root neighboor
#active neighors are subset of neighbors who post in the same topic before the user
#pick up positive and negative users that have at least one active neighbor