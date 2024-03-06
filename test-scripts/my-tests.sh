#!/usr/bin/env bash

HOST="localhost:3000"
SCORE=0

#####################################################################
# Test 1: list cells (no cells present)
#####################################################################
RESOURCE="$HOST/cells"
ANSWER="\[\]"
STATUS=$(curl -s -X GET -o body -w "%{http_code}" $RESOURCE)
if [ $STATUS == "200" ]; then
    grep -q $ANSWER body
    if [ $? -eq 0 ]; then
        echo "Test [1]: OK"; SCORE=$(expr $SCORE + 1)
    else
        echo "Test [1]: FAIL"
    fi
else
    echo "Test [1]: FAIL (" $STATUS "!= 200 )"
fi

#####################################################################
# Test 2: Create cell (basic number)
#####################################################################
ID="A1"
FORMULA="6"
RESOURCE=$HOST/cells/$ID

STATUS=$(curl -s -X PUT -d "{\"id\":\"$ID\",\"formula\":\"$FORMULA\"}" \
    -H "Content-Type: application/json" -w "%{http_code}" $RESOURCE)
if [ $STATUS == "201" ]; then
    echo "Test [2]: OK"; SCORE=$(expr $SCORE + 1)
else
    echo "Test [2]: FAIL (" $STATUS "!= 201 )"
fi

#####################################################################
# Test 3: list cells (1 cell present)
#####################################################################
RESOURCE="$HOST/cells"
ANSWER="\['A1'\]"
STATUS=$(curl -s -X GET -o body -w "%{http_code}" $RESOURCE)
if [ $STATUS == "200" ]; then
    grep -q $ANSWER body
    if [ $? -eq 0 ]; then
        echo "Test [3]: OK"; SCORE=$(expr $SCORE + 1)
    else
        echo "Test [3]: FAIL"
    fi
else
    echo "Test [3]: FAIL (" $STATUS "!= 200 )"
fi


#####################################################################
# Test 4: create cell (add two numbers)
#####################################################################
ID="A2"
FORMULA="1 + 1"
RESOURCE=$HOST/cells/$ID

STATUS=$(curl -s -X PUT -d "{\"id\":\"$ID\",\"formula\":\"$FORMULA\"}" \
    -H "Content-Type: application/json" -w "%{http_code}" $RESOURCE)
if [ $STATUS == "201" ]; then
    echo "Test [4]: OK"; SCORE=$(expr $SCORE + 1)
else
    echo "Test [4]: FAIL (" $STATUS "!= 201 )"
fi

#####################################################################
# Test 5: get cell (add two numbers)
#####################################################################
ID="A2"
ANSWER="\"formula\":\"2\""
RESOURCE=$HOST/cells/$ID

STATUS=$(curl -s -X GET -o body -w "%{http_code}" $RESOURCE)
if [ $STATUS == "200" ]; then
    grep -q $ANSWER body
    if [ $? -eq 0 ]; then
        echo "Test [5]: OK"; SCORE=$(expr $SCORE + 1)
    else
        echo "Test [5]: FAIL"
    fi
else
    echo "Test [5]: FAIL (" $STATUS "!= 200 )"
fi



echo "** Overall score:" $SCORE "**"