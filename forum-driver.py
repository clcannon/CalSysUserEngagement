from create_network import query_data, create_network, create_thread_info
from connect import get
from getFeatures import get_all
from sklearn.model_selection import train_test_split
from Learning import trainall
from sklearn.ensemble import RandomForestClassifier, ExtraTreesClassifier
from sklearn.metrics import confusion_matrix, accuracy_score, precision_score, recall_score
import config
from datetime import timedelta

forum_config = config.get_config(config, "FORUM")
forum_id = forum_config.get("ID")
forum_post_threshold = forum_config.get("POST_THRESHOLD")

network_config = config.get_config(config, "NETWORK")
t_config = config.get_config(config, "TAO")

t_sus = timedelta(hours=int(t_config.get("SUSCEPTIBLE")))
t_fos = timedelta(hours=int(t_config.get("FORGETTABLE")))

# load in social network graph for respective forum
# currently create_network is coupled to the data retrieval... change?
users, posts = query_data(network_config.get("USER_POSTS_THRESHOLD"),
                          network_config.get("USER_THREADS_THRESHOLD"),
                          network_config.get("THREAD_POSTS_THRESHOLD"),
                          network_config.get("THREAD_USERS_THRESHOLD"),
                          forum_id)
thread_info = create_thread_info(users, posts)
net = create_network(thread_info)

# get "forum" - topic_id and user_id of every post
forum = get('t_posts', 'topics_id, users_id', where='forums_id = ' + forum_id)

# creates list of users per thread (active users) in relation to another user (if within ts)
# I think we should use this. Just for the list of users not having to be made later?
positive_users = {}
for topic in thread_info:
    users = forum[forum['topics_id'] == topic]['users_id'].to_list()
    positive_users[topic] = (set(users))

# first in topic is the innovator
# early adopters : only took one or two active users to adopt - define early adopters

# need a better idea of what this is doing
dataSet = get_all(thread_info, net, t_sus, t_fos)

# dataSet = pd.read_csv('dataset.csv')
Y = dataSet.pop('Class')  # Class
X = dataSet.drop('user_id', axis=1)
# change this to 50/50?
X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.3, random_state=60)
trainall(X_train, X_test, Y_train, Y_test)

# Creating the Model (Optimised)
model = ExtraTreesClassifier()
model.fit(X_train, Y_train)
Y_pred = model.predict(X_test)

accuracy = accuracy_score(Y_test, Y_pred)
recall = recall_score(Y_test, Y_pred)
precision = precision_score(Y_test, Y_pred)

# Printing Confidence of Our Model
print(f"The accuracy of the model is {round(accuracy, 5) * 100} %")
print(f"The recall of the model is {round(recall, 3) * 100} %")
print(f"The precision of the model is {round(precision, 5) * 100} %")
print('Confusion Matrix : \n', confusion_matrix(Y_test, Y_pred))
print(f"{round(accuracy, 5) * 100}  {round(recall, 3) * 100}  {round(precision, 5) * 100}")


# Improvement: More features(ex.PNE), more users, more topics, imbalanced dataset/more realistic.


def remove_duplicates_preserve_order(users_list):
    seen = set()
    seen_add = seen.add
    return [x for x in users_list if not (x in seen or seen_add(x))]
