#!/usr/bin/env bash
HOST=localhost:3000
echo "{\"id\": \"$1\", \"formula\": \"$2\"}"
curl -X PUT -H "Content-Type: application/json" -d "{\"id\":\"$1\",\"formula\":\"$2\"}" $HOST/cells/$1