#!/bin/sh
###############################################################
## Spreadsheet test script                                   ##
###############################################################

HOST=localhost:3000

SCORE=0

###############################################################
## Test [1]: list                                            ##
###############################################################
RESOURCE=$HOST/cells
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

###############################################################
## Test [2]: update                                          ##
###############################################################
ID="B2"; FORMULA="6"
RESOURCE=$HOST/cells/$ID

STATUS=$(curl -s -X PUT -d "{\"id\":\"$ID\",\"formula\":\"$FORMULA\"}" \
    -H "Content-Type: application/json" -w "%{http_code}" $RESOURCE)
if [ $STATUS == "201" ]; then
    echo "Test [2]: OK"; SCORE=$(expr $SCORE + 1)
else
    echo "Test [2]: FAIL (" $STATUS "!= 201 )"
fi

###############################################################
## Test [3]: update                                          ##
###############################################################
ID="B3"; FORMULA="3 + 4"
RESOURCE=$HOST/cells/$ID

STATUS=$(curl -s -X PUT -d "{\"id\":\"$ID\",\"formula\":\"$FORMULA\"}" \
    -H "Content-Type: application/json" -w "%{http_code}" $RESOURCE)
if [ $STATUS == "201" ]; then
    echo "Test [3]: OK"; SCORE=$(expr $SCORE + 1)
else
    echo "Test [3]: FAIL (" $STATUS "!= 201 )"
fi

###############################################################
## Test [4]: update                                          ##
###############################################################
ID="D4"; FORMULA="3000"
RESOURCE=$HOST/cells/$ID

STATUS=$(curl -s -X PUT -d "{\"id\":\"$ID\",\"formula\":\"$FORMULA\"}" \
    -H "Content-Type: application/json" -w "%{http_code}" $RESOURCE)
if [ $STATUS == "201" ]; then
    echo "Test [4]: OK"; SCORE=$(expr $SCORE + 1)
else
    echo "Test [4]: FAIL (" $STATUS "!= 201 )"
fi

###############################################################
## Test [5]: update                                          ##
###############################################################
ID="D4"; FORMULA="B2 * B3"
RESOURCE=$HOST/cells/$ID

STATUS=$(curl -s -X PUT -d "{\"id\":\"$ID\",\"formula\":\"$FORMULA\"}" \
    -H "Content-Type: application/json" -w "%{http_code}" $RESOURCE)
if [ $STATUS == "204" ]; then
    echo "Test [5]: OK"; SCORE=$(expr $SCORE + 1)
else
    echo "Test [5]: FAIL (" $STATUS "!= 204 )"
fi

###############################################################
## Test [6]: read                                            ##
###############################################################
ID="D4"
ANSWER="\"formula\":\"42\""
RESOURCE=$HOST/cells/$ID

STATUS=$(curl -s -X GET -o body -w "%{http_code}" $RESOURCE)
if [ $STATUS == "200" ]; then
    grep -q $ANSWER body
    if [ $? -eq 0 ]; then
        echo "Test [6]: OK"; SCORE=$(expr $SCORE + 1)
    else
        echo "Test [6]: FAIL"
    fi
else
    echo "Test [6]: FAIL (" $STATUS "!= 200 )"
fi

###############################################################
## Test [7]: update                                          ##
###############################################################
ID="A9"
RESOURCE=$HOST/cells/$ID

STATUS=$(curl -s -X PUT -d "{\"id\":\"$ID\"}" \
    -H "Content-Type: application/json" -w "%{http_code}" $RESOURCE)
if [ $STATUS == "400" ]; then
    echo "Test [7]: OK"; SCORE=$(expr $SCORE + 1)
else
    echo "Test [7]: FAIL (" $STATUS "!= 400 )"
fi

###############################################################
## Test [8]: update                                          ##
###############################################################
ID="A9"
FORMULA="3000 + 7000"
RESOURCE=$HOST/cells/$ID

STATUS=$(curl -s -X PUT -d "{\"formula\":\"$FORMULA\"}" \
    -o body -H "Content-Type: application/json" -w "%{http_code}" $RESOURCE)
if [ $STATUS == "400" ]; then
    echo "Test [8]: OK"; SCORE=$(expr $SCORE + 1)
else
    echo "Test [8]: FAIL (" $STATUS "!= 400 )"
fi

###############################################################
## Test [9]: update                                          ##
###############################################################
ID="B2"; ID2="B3"; FORMULA="3 + 4"
RESOURCE=$HOST/cells/$ID2

STATUS=$(curl -s -X PUT -d "{\"id\":\"$ID\",\"formula\":\"$FORMULA\"}" \
    -H "Content-Type: application/json" -w "%{http_code}" $RESOURCE)
if [ $STATUS == "400" ]; then
    echo "Test [9]: OK"; SCORE=$(expr $SCORE + 1)
else
    echo "Test [9]: FAIL (" $STATUS "!= 400 )"
fi

###############################################################
## Test [10]: list                                           ##
###############################################################
RESOURCE=$HOST/cells
ANSWER1="B2"
ANSWER2="B3"
ANSWER3="D4"

STATUS=$(curl -s -X GET -o body -w "%{http_code}" $RESOURCE)
if [ $STATUS == "200" ]; then
    grep -q $ANSWER1 body
    if [ $? -eq 0 ]; then
        grep -q $ANSWER2 body
        if [ $? -eq 0 ]; then
            grep -q $ANSWER3 body
            if [ $? -eq 0 ]; then
                echo "Test [10]: OK"; SCORE=$(expr $SCORE + 1)
            else
                echo "Test [10]: FAIL"
            fi
        else
            echo "Test [10]: FAIL"
        fi
    else
        echo "Test [10]: FAIL"
    fi
else
    echo "Test [10]: FAIL (" $STATUS "!= 200 )"
fi

###############################################################
## Test [11]: delete                                         ##
###############################################################
ID="B2"
RESOURCE=$HOST/cells/$ID

STATUS=$(curl -s -X DELETE -w "%{http_code}" $RESOURCE)
if [ $STATUS == "204" ]; then
    echo "Test [11]: OK"; SCORE=$(expr $SCORE + 1)
else
    echo "Test [11]: FAIL (" $STATUS "!= 204 )"
fi

###############################################################
## Test [12]: read (should fail after delete)                ##
###############################################################
ID="B2"
RESOURCE=$HOST/cells/$ID

STATUS=$(curl -s -X GET -o body -w "%{http_code}" $RESOURCE)
if [ $STATUS == "404" ]; then
    echo "Test [12]: OK"; SCORE=$(expr $SCORE + 1)
else
    echo "Test [12]: FAIL (" $STATUS "!= 404 )"
fi

###############################################################
## Test [13]: list (should not contain deleted ID)           ##
###############################################################
RESOURCE=$HOST/cells
ANSWER="B2"

STATUS=$(curl -s -X GET -o body -w "%{http_code}" $RESOURCE)
if [ $STATUS == "200" ]; then
    grep -q $ANSWER body
    if [ $? -eq 1 ]; then
        echo "Test [13]: OK"; SCORE=$(expr $SCORE + 1)
    else
        echo "Test [13]: FAIL"
    fi
else
    echo "Test [13]: FAIL (" $STATUS "!= 200 )"
fi

###############################################################
## Test [14]: create cell for addition                       ##
###############################################################
ID="C1"; FORMULA="3 + 4"
RESOURCE=$HOST/cells/$ID

STATUS=$(curl -s -X PUT -d "{\"id\":\"$ID\",\"formula\":\"$FORMULA\"}" \
    -H "Content-Type: application/json" -w "%{http_code}" $RESOURCE)
if [ $STATUS == "201" ]; then
    echo "Test [14]: OK"; SCORE=$(expr $SCORE + 1)
else
    echo "Test [14]: FAIL (" $STATUS "!= 201 )"
fi

###############################################################
## Test [15]: create cell for subtraction                    ##
###############################################################
ID="C2"; FORMULA="10 - 5"
RESOURCE=$HOST/cells/$ID

STATUS=$(curl -s -X PUT -d "{\"id\":\"$ID\",\"formula\":\"$FORMULA\"}" \
    -H "Content-Type: application/json" -w "%{http_code}" $RESOURCE)
if [ $STATUS == "201" ]; then
    echo "Test [15]: OK"; SCORE=$(expr $SCORE + 1)
else
    echo "Test [15]: FAIL (" $STATUS "!= 201 )"
fi

###############################################################
## Test [16]: create cell for multiplication                 ##
###############################################################
ID="C3"; FORMULA="2 * 3"
RESOURCE=$HOST/cells/$ID

STATUS=$(curl -s -X PUT -d "{\"id\":\"$ID\",\"formula\":\"$FORMULA\"}" \
    -H "Content-Type: application/json" -w "%{http_code}" $RESOURCE)
if [ $STATUS == "201" ]; then
    echo "Test [16]: OK"; SCORE=$(expr $SCORE + 1)
else
    echo "Test [16]: FAIL (" $STATUS "!= 201 )"
fi

###############################################################
## Test [17]: create cell for division                       ##
###############################################################
ID="C4"; FORMULA="8 / 2"
RESOURCE=$HOST/cells/$ID

STATUS=$(curl -s -X PUT -d "{\"id\":\"$ID\",\"formula\":\"$FORMULA\"}" \
    -H "Content-Type: application/json" -w "%{http_code}" $RESOURCE)
if [ $STATUS == "201" ]; then
    echo "Test [17]: OK"; SCORE=$(expr $SCORE + 1)
else
    echo "Test [17]: FAIL (" $STATUS "!= 201 )"
fi

###############################################################
## Test [18]: read                                            #
###############################################################
ID="C1"
ANSWER="\"formula\":\"7\""
RESOURCE=$HOST/cells/$ID

STATUS=$(curl -s -X GET -o body -w "%{http_code}" $RESOURCE)
if [ $STATUS == "200" ]; then
    grep -q $ANSWER body
    if [ $? -eq 0 ]; then
        echo "Test [18]: OK"; SCORE=$(expr $SCORE + 1)
    else
        echo "Test [18]: FAIL"
    fi
else
    echo "Test [18]: FAIL (" $STATUS "!= 200 )"
fi

###############################################################
## Test [19]: read                                            #
###############################################################
ID="C2"
ANSWER="\"formula\":\"5\""
RESOURCE=$HOST/cells/$ID

STATUS=$(curl -s -X GET -o body -w "%{http_code}" $RESOURCE)
if [ $STATUS == "200" ]; then
    grep -q $ANSWER body
    if [ $? -eq 0 ]; then
        echo "Test [19]: OK"; SCORE=$(expr $SCORE + 1)
    else
        echo "Test [19]: FAIL"
    fi
else
    echo "Test [19]: FAIL (" $STATUS "!= 200 )"
fi

###############################################################
## Test [20]: read                                            #
###############################################################
ID="C3"
ANSWER="\"formula\":\"6\""
RESOURCE=$HOST/cells/$ID

STATUS=$(curl -s -X GET -o body -w "%{http_code}" $RESOURCE)
if [ $STATUS == "200" ]; then
    grep -q $ANSWER body
    if [ $? -eq 0 ]; then
        echo "Test [20]: OK"; SCORE=$(expr $SCORE + 1)
    else
        echo "Test [20]: FAIL"
    fi
else
    echo "Test [20]: FAIL (" $STATUS "!= 200 )"
fi

###############################################################
## Test [21]: read                                            #
###############################################################
ID="C4"
ANSWER="\"formula\":\"4\""
RESOURCE=$HOST/cells/$ID

STATUS=$(curl -s -X GET -o body -w "%{http_code}" $RESOURCE)
if [ $STATUS == "200" ]; then
    grep -q $ANSWER body
    if [ $? -eq 0 ]; then
        echo "Test [21]: OK"; SCORE=$(expr $SCORE + 1)
    else
        echo "Test [21]: FAIL" $ANSWER
    fi
else
    echo "Test [21]: FAIL (" $STATUS "!= 200 )"
fi

###############################################################
## Test [22]: read D4 (should return 0 because B2 is empty)   #
###############################################################
ID="D4"
ANSWER="\"formula\":\"0\""
RESOURCE=$HOST/cells/$ID

STATUS=$(curl -s -X GET -o body -w "%{http_code}" $RESOURCE)
if [ $STATUS == "200" ]; then
    grep -q $ANSWER body
    if [ $? -eq 0 ]; then
        echo "Test [22]: OK"; SCORE=$(expr $SCORE + 1)
    else
        echo "Test [22]: FAIL"
    fi
else
    echo "Test [22]: FAIL (" $STATUS "!= 200 )"
fi


echo "** Overall score:" $SCORE "**"
