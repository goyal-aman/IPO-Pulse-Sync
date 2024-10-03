## About
IPO-Pulse-Sync syncs html generated with the github repo.

## Play around with docker
```
# Step 1, start ipo-pulse-api container
docker run --rm -p 5678:5678 amangoyal8110/ipo-pulse-api:latest

# Step 2, generate index.html
sudo docker run -p 5679:5679 -e IPO_PULSE_BASE_URL=http://localhost:5678 amangoyal8110/ipo-pulse-parser:9

# Step 3, run ipo-pulse-sync
sudo docker run -p 5680:5680 -e GHTOKEN=<GITHUB_TOKEN> -e IPO_PULSE_PARSER_BASE_URL=<IPO_PULSE_PARSER_BASE_URL> amangoyal8110/ipo-pulse-sync:6
```


## Next Steps
1. Improve ipo-pulse-sync to read read from config.json
