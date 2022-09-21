import create_network
from connect import get
from feature import get_net, show_net
from getFeatures import get_all
import networkx
import pandas as pd
from sklearn.model_selection import train_test_split
from Learning import trainall
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import r2_score
from sklearn.metrics import confusion_matrix, accuracy_score, precision_score, recall_score
import config

forum_config = config.get_config(config, "FORUM")
forum_id = forum_config.get("ID")
forum_post_threshold = forum_config.get("POST_THRESHOLD")

network_config = config.get_config(config, "NETWORK")

# load in social network graph for respective forum
# currently create_network is coupled to the data retrieval... change?
net, thread_info = create_network.create_graph(network_config.get("USER_POSTS_THRESHOLD"),
                                               network_config.get("USER_THREADS_THRESHOLD"),
                                               network_config.get("THREAD_POSTS_THRESHOLD"),
                                               network_config.get("THREAD_USERS_THRESHOLD"),
                                               forum_id, 0, 0)

# net = get_net(f'pickleX{forum_id}.p')
# net2 = networkx.DiGraph()
# net2 = get_net("pickleX77.p")
# pickle file is a digraph with 1 edge per user with the t of the most recent interaction?
# only one connection which is "refreshed" per interaction

# for node in net:
#    y = list(net.in_edges(node))

# get "forum" - topic_id and user_id of every post
forum = get('t_posts', 'topics_id, users_id', where='forums_id = ' + forum_id)

# add count constraint
thread = get('t_posts', cols="topics_id", where='forums_id = ' + forum_id,
             modifier='group by topics_id having count(*) > ' + forum_post_threshold)  # needs to be distinct
topic_list = thread['topics_id'].to_list()

# creates list of users per thread (active users) in relation to another user (if within ts)
# do we even need this?
positive_users = {}
for topic in topic_list:
    users = forum[forum['topics_id'] == topic]['users_id'].to_list()
    positive_users[topic] = (list(users))

# neighborhood outgoing neighbors

# first in topic is the innovator
# early adopters : only took one or two active users to adopt - define early adopters
# delta ts tao sus - visualization
# delta tf tao fos - memorization
# t fos will resent after a post?

# need a better idea of what this is doing
dataSet = get_all(thread_info, net)

# dataSet = pd.read_csv('dataset.csv')
Y = dataSet.pop('Class')  # Class
X = dataSet.drop('user_id', axis=1)
# change this to 50/50?
X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.3, random_state=60)
# trainall(X_train, X_test, Y_train, Y_test)


# Creating the Model (Optimised)
model = RandomForestClassifier(max_depth=2, random_state=0)
model.fit(X_train, Y_train)
Y_pred = model.predict(X_test)
# conf = round((r2_score(Y_test,Y_pred))*100,3)
accuracy = accuracy_score(Y_test, Y_pred)
recall = recall_score(Y_test, Y_pred)
precision = precision_score(Y_test, Y_pred)

# Printing Confidence of Our Model
print(f"The accuracy of the model is {round(accuracy, 5) * 100} %")
print(f"The recall of the model is {round(recall, 3) * 100} %")
print(f"The precision of the model is {round(precision, 5) * 100} %")
print('Confusion Matrix : \n', confusion_matrix(Y_test, Y_pred))


# Improvement: More features(ex.PNE), more users, more topics, imbalanced dataset/more realistic.

# Questions for Marin: What is PNE? Need access to database with forum 77! How to get root neighbor for negative samples?

# needs to be distinct
# negative users need to have same root neighboor
# active neighors are subset of neighbors who post in the same topic before the user
# pick up positive and negative users that have at least one active neighbor


def remove_duplicates_preserve_order(users_list):
    seen = set()
    seen_add = seen.add
    return [x for x in users_list if not (x in seen or seen_add(x))]
