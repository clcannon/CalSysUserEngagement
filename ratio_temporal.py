from bitarray import bitarray
from create_network import query_data, create_network, create_thread_info
from connect import get
from getFeatures import get_balanced_dataset, get_ratio
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

# need a better idea of what this is doing
ratio = get_ratio(thread_info, net, t_sus, t_fos, len(users))
print(ratio)

#  0.015554723409280933
#  0.01848600868647399 When looking at earliest instance of posting
#  0.020856128936101347 When trimmed to highest post frequency
