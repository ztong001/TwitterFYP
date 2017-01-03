import re
import json
import os

# Regex used to filter out retweets
retweets_re = re.compile(r'^RT\s')

filename = str(os.getcwd()) + "/outData/tweetdata.txt"
with open(filename, 'r', newline="\r\n") as f:
    tweets = [line for line in f if re.search(
        retweets_re, line) is None]
    print(len(tweets))

with open(filename, 'w') as output:
    for l in tweets:
        output.write(json.dumps(l, sort_keys=True))
        output.write("\r\n")
        print("Writing tweets")
print("Sanitized")
