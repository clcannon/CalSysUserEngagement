from bitarray import bitarray
from create_network import query_data, create_network, create_thread_info
from connect import get
from getFeatures import get_balanced_dataset
from sklearn.model_selection import train_test_split
from Learning import trainall
from sklearn.ensemble import RandomForestClassifier, ExtraTreesClassifier
from sklearn.metrics import confusion_matrix, accuracy_score, precision_score, recall_score
import config
from datetime import timedelta

# Get forum config
forum_config = config.get_config(config, "FORUM")
forum_id = forum_config.get("ID")
forum_post_threshold = forum_config.get("POST_THRESHOLD")
date_config = config.get_config(config, "DATE")
date_begin = date_config.get("BEGIN")
date_end = date_config.get("END")

# Get network config
network_config = config.get_config(config, "NETWORK")

# Get tao config
t_config = config.get_config(config, "TAO")
t_sus = timedelta(hours=int(t_config.get("SUSCEPTIBLE")))
t_fos = timedelta(hours=int(t_config.get("FORGETTABLE")))

# Get feature config
feature_config = config.get_config(config, "FEATURE")

# Create features bit array
# 0 - NAN
# 1 - PNE
# 2 - HUB
features_bits = bitarray()
for feature in feature_config:
    val = 1 if (feature_config[feature] == "True" or feature_config[feature] == "TRUE" or feature_config[feature] == "true") else 0
    features_bits.append(val)

# load in social network graph for respective forum
# currently create_network is coupled to the data retrieval... change?
users, posts = query_data(network_config.get("USER_POSTS_THRESHOLD"),
                          network_config.get("USER_THREADS_THRESHOLD"),
                          network_config.get("THREAD_POSTS_THRESHOLD"),
                          network_config.get("THREAD_USERS_THRESHOLD"),
                          forum_id)

mask = (posts['posted_date'] > date_begin) & (posts['posted_date'] <= date_end)
posts = posts.loc[mask]

thread_info = create_thread_info(users, posts)
net = create_network(thread_info)

# get "forum" - topic_id and user_id of every post
forum = get('t_posts', 'topics_id, users_id', where='forums_id = ' + forum_id)

# first in topic is the innovator
# early adopters : only took one or two active users to adopt - define early adopters

# need a better idea of what this is doing
dataSet = get_balanced_dataset(thread_info, net, t_sus, t_fos, features_bits)

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

