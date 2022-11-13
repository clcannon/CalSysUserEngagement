from datetime import datetime, timedelta

from connect import get, get_q
import config
import matplotlib.pyplot as plt

# Get forum configuration
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

get_users_posts_and_threads = f"select users_id, count(posts_id), count(distinct topics_id) from t_posts " \
                              f"where forums_id = {forum_id}" \
                              f"group by users_id \
                              having count(posts_id) > {user_post_requirement} and count(distinct topics_id) > {user_thread_requirement}"
users_data = get_q(get_users_posts_and_threads, ['users_id', 'count(posts_id)', 'count(distinct topics_id)'], 't_posts')

# *** Start posts per user ***
# print(users_data)
post_counts = users_data['count(posts_id)'].tolist()
count_dict = {5: 0, 10: 0, 20: 0, 50: 0, 100: 0, 200: 0, 500: 0, 1000: 0}
for count in post_counts:
    if count >= 1000:
        count_dict[1000] += 1
    elif count >= 500:
        count_dict[500] += 1
    elif count >= 200:
        count_dict[200] += 1
    elif count >= 100:
        count_dict[100] += 1
    elif count >= 50:
        count_dict[50] += 1
    elif count >= 20:
        count_dict[20] += 1
    elif count >= 10:
        count_dict[10] += 1
    elif count >= 5:
        count_dict[5] += 1
    elif count not in count_dict:
        count_dict[count] = 0
    else:
        count_dict[count] += 1

key_strings = []
values = []
for key in sorted(count_dict.keys()):
    if key >= 5:
        key_strings.append(str(key) + "+")
    else:
        key_strings.append(str(key))
    values.append(count_dict[key])

color = "navy"
if forum_id == '77':
    color = "navy"
elif forum_id == '84':
    color = "#a17f1a"  # dark gold
else:
    color = "maroon"

plt.bar(key_strings, values, color=color,
        width=0.4)

plt.xlabel("Amount of posts")
plt.ylabel("Amount of users")
plt.title("Posts per user in forum " + str(forum_id))
plt.show()

# *** Start unique threads per user ***
unique_participation_count = users_data['count(distinct topics_id)'].tolist()
thread_count_dict = {5: 0, 10: 0, 20: 0, 50: 0, 100: 0, 200: 0, 500: 0, 1000: 0}
for count in unique_participation_count:
    if count >= 1000:
        thread_count_dict[1000] += 1
    elif count >= 500:
        thread_count_dict[500] += 1
    elif count >= 200:
        thread_count_dict[200] += 1
    elif count >= 100:
        thread_count_dict[100] += 1
    elif count >= 50:
        thread_count_dict[50] += 1
    elif count >= 20:
        thread_count_dict[20] += 1
    elif count >= 10:
        thread_count_dict[10] += 1
    elif count >= 5:
        thread_count_dict[5] += 1
    elif count not in thread_count_dict:
        thread_count_dict[count] = 0
    else:
        thread_count_dict[count] += 1

key_strings = []
values = []
for key in sorted(thread_count_dict.keys()):
    if key >= 5:
        key_strings.append(str(key) + "+")
    else:
        key_strings.append(str(key))
    values.append(thread_count_dict[key])

color = "navy"
if forum_id == '77':
    color = "navy"
elif forum_id == '84':
    color = "#a17f1a"  # dark gold
else:
    color = "maroon"

plt.bar(key_strings, values, color=color,
        width=0.4)

plt.xlabel("Amount of threads")
plt.ylabel("Amount of users")
plt.title("Unique thread participation by user for forum " + str(forum_id))
plt.show()
