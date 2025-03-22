_Guys... Instagram is sh*t. Even [bibliogram](https://www.reddit.com/r/privacy/comments/wrczxc/bibliogram_is_being_discontinued/) 
is being discontinued. If you're able to migrate you profile to any fediverse instance or contact to person, whose 
instagram you'd like to cross-post and ask him to post to fediverse to, it wil be the best decision_

# Instagram2Fedi <span><img width="50px" src="https://upload.wikimedia.org/wikipedia/commons/9/93/Fediverse_logo_proposal.svg"></span>

Simple tool for cross-posting posts from instagram to Mastodon/Pixelfed.

## Using without docker
See [Docs.md](./Docs.md)

## Using docker-compose

1. create `docker-compose.yaml` with following content
_You can use default.docker-compose.yaml from repo_
``` yaml
version: '3'
services:
  bot:
    build:
      context: .
    image: "horhik/instagram2fedi:latest"
    environment:
      - YOUR_CONTAINER_NAME=<whatever>
      - I2M_INSTAGRAM_USER=<instgram username>
      - I2M_INSTANCE=<mastodon or pixelfed instance> # Not needed, if instance is stored in user_credentials.secret
      - I2M_TOKEN=<your token here> # SECRET MASTODON TOKEN filename. See: src/create_credentials.py
      - I2M_CHECK_INTERVAL=3600 #1 hour    
      - I2M_POST_INTERVAL=3600 #1 hour   
      - I2M_USE_MASTODON=4 #max carouse    - is 4, if there's no limit set to -1
      - I2M_FETCH_COUNT=5 # how many instagram posts to fetch per check_interval   -
      - I2M_USER_NAME=admin # Your instagram login name
      - I2M_USER_PASSWORD=admin # Your instagram password
```

> ** Note: ** _Since some time it seems to be not possible to fetch any data from Instagram anonymously (maybe I'm wrong 
and there's a solution, I'll be very happy to know about it). Due to that you unfortunately need an Instagram account 
and provide login and password to this script_

> ** Note: ** _Instagram may block login attempts from this script, and may suspend your account._

2. And edit environment variables

3. Run `docker-compose up -d`


## Using with Dockerfile

Just clone repo, specify variables and run it.
You can write all needed variables in `./env.sh` and then do `source ./run.sh`

``` bash
git clone https://github.com/horhik/instagram2fedi
cd instagram2fedi
nano ./env.sh
source ./run.sh
```


![screenshot](./img.png)
