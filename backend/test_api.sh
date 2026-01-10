#!/bin/bash
# API Testing Script

TOKEN="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxIiwiZXhwIjoxNzY3OTg2MjQ2LCJpYXQiOjE3Njc4OTk4NDZ9.fM47rf3R8kFtxKQh4zNPwR8zDZu-nX3fzajqZPr2re8"

echo "=========================================="
echo "TEST 1: Create Task - Complete project proposal"
echo "=========================================="
TASK1=$(curl -s -X POST http://localhost:8000/api/tasks \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"title":"Complete project proposal","description":"Draft and submit the Q1 project proposal"}')
echo "$TASK1" | python3 -m json.tool
TASK1_ID=$(echo "$TASK1" | python3 -c "import sys, json; print(json.load(sys.stdin)['id'])")
echo "✅ Created task ID: $TASK1_ID"
echo ""

echo "=========================================="
echo "TEST 2: Create Task - Review pull requests"
echo "=========================================="
TASK2=$(curl -s -X POST http://localhost:8000/api/tasks \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"title":"Review pull requests","description":"Check and merge pending PRs"}')
echo "$TASK2" | python3 -m json.tool
TASK2_ID=$(echo "$TASK2" | python3 -c "import sys, json; print(json.load(sys.stdin)['id'])")
echo "✅ Created task ID: $TASK2_ID"
echo ""

echo "=========================================="
echo "TEST 3: Create Task - Update documentation"
echo "=========================================="
TASK3=$(curl -s -X POST http://localhost:8000/api/tasks \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"title":"Update documentation"}')
echo "$TASK3" | python3 -m json.tool
TASK3_ID=$(echo "$TASK3" | python3 -c "import sys, json; print(json.load(sys.stdin)['id'])")
echo "✅ Created task ID: $TASK3_ID"
echo ""

echo "=========================================="
echo "TEST 4: List All Tasks"
echo "=========================================="
curl -s http://localhost:8000/api/tasks \
  -H "Authorization: Bearer $TOKEN" | python3 -m json.tool
echo ""

echo "=========================================="
echo "TEST 5: Get Single Task (ID: $TASK1_ID)"
echo "=========================================="
curl -s http://localhost:8000/api/tasks/$TASK1_ID \
  -H "Authorization: Bearer $TOKEN" | python3 -m json.tool
echo ""

echo "=========================================="
echo "TEST 6: Update Task (ID: $TASK1_ID)"
echo "=========================================="
curl -s -X PUT http://localhost:8000/api/tasks/$TASK1_ID \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"title":"Complete project proposal by Friday","description":"Draft, review, and submit by EOD Friday"}' \
  | python3 -m json.tool
echo ""

echo "=========================================="
echo "TEST 7: Toggle Task Completion (ID: $TASK2_ID)"
echo "=========================================="
curl -s -X PATCH http://localhost:8000/api/tasks/$TASK2_ID/toggle \
  -H "Authorization: Bearer $TOKEN" | python3 -m json.tool
echo ""

echo "=========================================="
echo "TEST 8: List Complete Tasks Only"
echo "=========================================="
curl -s "http://localhost:8000/api/tasks?status=complete" \
  -H "Authorization: Bearer $TOKEN" | python3 -m json.tool
echo ""

echo "=========================================="
echo "TEST 9: List Incomplete Tasks Only"
echo "=========================================="
curl -s "http://localhost:8000/api/tasks?status=incomplete" \
  -H "Authorization: Bearer $TOKEN" | python3 -m json.tool
echo ""

echo "=========================================="
echo "TEST 10: Delete Task (ID: $TASK3_ID)"
echo "=========================================="
curl -s -X DELETE http://localhost:8000/api/tasks/$TASK3_ID \
  -H "Authorization: Bearer $TOKEN"
echo "✅ Task deleted"
echo ""

echo "=========================================="
echo "TEST 11: Verify Deletion - List All Tasks"
echo "=========================================="
curl -s http://localhost:8000/api/tasks \
  -H "Authorization: Bearer $TOKEN" | python3 -m json.tool
echo ""

echo "=========================================="
echo "✅ ALL TESTS COMPLETED!"
echo "=========================================="
