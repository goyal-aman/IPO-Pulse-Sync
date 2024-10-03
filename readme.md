## About
IPO-Pulse-Sync syncs html generated with the github repo.

## Play around with docker
```
# Step 1, start ipo-pulse-api container
docker run --rm -p 5678:5678 amangoyal8110/ipo-pulse-api:latest

# Step 2, generate index.html
docker run -e BASE_URL=http://localhost:5678 -v $PWD:/app/generated amangoyal8110/ipo-pulse-parser:latest

# Step 3, Sync with git repo, right now git repo is hard coded, this will be fixed in next versions
sudo docker run -e TOKEN=<GITHUB_TOKEN> -v $PWD/index.html:/app/index.html amangoyal8110/ipo-pulse-sync:4
```


## Next Steps
1. Improve ipo-pulse-sync to read read from config.json