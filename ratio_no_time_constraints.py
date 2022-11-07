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

# * This script is no good as it looks into the future.

# Get forum config
forum_config = config.get_config(config, "FORUM")
forum_id = forum_config.get("ID")
forum_post_threshold = forum_config.get("POST_THRESHOLD")

# Get network config
network_config = config.get_config(config, "NETWORK")

# Get tao config
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

positive_users = {}  # Key: thread Value: [user]
ratio = 0.0

for thread in thread_info:
    positive_users[thread] = set()
    for user, date in thread_info[thread]:
        positive_users[thread].add(user)
    ratio += (len(positive_users[thread]) / len(users))

print(ratio / len(thread_info.keys()))


# .010000
