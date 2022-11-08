# CalSysUserEngagement

Information for configurations

To set up configuration for single runs:
Create file "config.yaml"
Format as such:

DATABASE:
  HOST: "localhost"
  DATABASE: "Test2"
  USER: "postgres"
  PASSWORD: "123"

FORUM:
  ID: "77"
  POST_THRESHOLD: "0"

NETWORK:
  USER_POSTS_THRESHOLD: "4"
  USER_THREADS_THRESHOLD: "4"
  THREAD_POSTS_THRESHOLD: "4"
  THREAD_USERS_THRESHOLD: "4"

TAO:
  SUSCEPTIBLE: "8760"
  FORGETTABLE: "8760"
  
FEATURE:
  NAN: "True"
  PNE: "True"
  HUB: "False"

DATE:
  BEGIN: "2000-6-1"
  END: "2012-10-31"

Once config.yaml is created with parameters, forum-driver can be run from ide as normal.

For batch runs:
Create file directory called "configs"
Add configs to config directory. Each config should follow the format above.

batch.sh will run forum-driver with each config as an argument (sequentially)

Once configs are set, the file "batch.sh" can be run from CLI with the following command:
bash batch.sh > output.txt


