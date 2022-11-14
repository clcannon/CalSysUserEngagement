from bitarray import bitarray
from create_network import query_data, create_network, create_thread_info
from connect import get
from getFeatures import get_balanced_dataset
from sklearn.model_selection import train_test_split
from Learning import trainall
from sklearn.ensemble import ExtraTreesClassifier
from sklearn.metrics import confusion_matrix
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
user_post_requirement = network_config.get("USER_POSTS_THRESHOLD")
user_thread_requirement = network_config.get("USER_THREADS_THRESHOLD")
thread_post_requirement = network_config.get("THREAD_POSTS_THRESHOLD")
thread_users_requirement = network_config.get("THREAD_USERS_THRESHOLD")

# Get tao config
t_config = config.get_config(config, "TAO")
t_sus = timedelta(hours=int(t_config.get("SUSCEPTIBLE")))
t_fos = timedelta(hours=int(t_config.get("FORGETTABLE")))

# Get feature config
feature_config = config.get_config(config, "FEATURE")

# Get hyperparam config
hyperparams_et_config = config.get_config(config, "HYPERPARAMS_ET")
n_estimators = hyperparams_et_config.get("N_ESTIMATORS")
max_features = hyperparams_et_config.get("sqrt")
min_samples_split = hyperparams_et_config.get("MIN_SAMPLES_SPLIT")
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
users, posts = query_data(user_post_requirement,
                          user_thread_requirement,
                          thread_post_requirement,
                          thread_users_requirement,
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
trim_X_test = X_test
trim_Y_test = Y_test

remove_indexes = []
count = 0
for label, index in zip(Y_test, trim_X_test.index):
    # for every 1, skip the next 48 1's.
    if count >= 49 and label == 1:
        count = 0
    elif label == 1:
        remove_indexes.append(index)
    else:
        count += 1

trim_X_test.drop(index=remove_indexes, inplace=True)
trim_Y_test.drop(index=remove_indexes, inplace=True)

count_1 = 0
count_0 = 0
for label in trim_Y_test:
    if label == 1 or label == '1':
        count_1 += 1
    else:
        count_0 += 1

print("Ratio: " + str(count_1/count_0))

# trainall(X_train, X_test, Y_train, Y_test)

# Creating the Model (Optimised)
model = ExtraTreesClassifier(n_estimators=int(n_estimators), max_features=max_features, min_samples_split=int(min_samples_split))
model.fit(X_train, Y_train)
Y_pred = model.predict(X_test)

# recall = balanced_recall_score(Y_test, Y_pred, adjusted=False)
# precision = precision_score(Y_test, Y_pred)

# Printing Confidence of Our Model
# Due to altered test proportion, confusion matrix must be interpreted as:
# TN FN
# FP TP
conf_matrix = confusion_matrix(Y_test, Y_pred)
TN = conf_matrix[0][0]
FN = conf_matrix[0][1]
FP = conf_matrix[1][0]
TP = conf_matrix[1][1]

print('Confusion Matrix : \n', confusion_matrix(Y_test, Y_pred))
print(TN, FN)
print(FP, TP)

recall = TP/(TP + FN)
precision = TP/(TP + FP)
f1 = (precision * recall) / (precision + recall)

print(f"The recall of the model is {round(recall, 3) * 100} %")
print(f"The precision of the model is {round(precision, 5) * 100} %")
print(f"The F1 score of the model is {round(f1, 5) * 100} %")


print(f"Forum: {forum_id}")
print(f"t_sus: {t_sus}")
print(f"t_fos: {t_fos}")
print(f"Begin Date: {date_begin}")
print(f"End Date: {date_end}")
print(f"Network Filters: ")
print(f"    User must post at least {user_post_requirement}")
print(f"    User must post in at least {user_thread_requirement} unique threads")
print(f"    Thread must contain at least {thread_post_requirement} posts")
print(f"    Thread must have at least {thread_post_requirement} unique user participants")


print(f"{round(f1, 5) * 100}  {round(recall, 3) * 100}  {round(precision, 5) * 100}")
