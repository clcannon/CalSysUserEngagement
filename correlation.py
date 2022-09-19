import create_network
from connect import get
import config
from getFeatures import get_NAN

forum_config = config.get_config(config, "FORUM")
forum_id = forum_config.get("ID")
forum_post_threshold = forum_config.get("POST_THRESHOLD")

network_config = config.get_config(config, "NETWORK")

net, thread_info = create_network.create_graph(network_config.get("USER_POSTS_THRESHOLD"),
                                               network_config.get("USER_THREADS_THRESHOLD"),
                                               network_config.get("THREAD_POSTS_THRESHOLD"),
                                               network_config.get("THREAD_USERS_THRESHOLD"),
                                               forum_id, 0, 0)
# for
# NAN = get_NAN()