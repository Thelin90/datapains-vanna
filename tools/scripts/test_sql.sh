#!/bin/bash

echo "check information schema..."
sleep 5

COORDINATOR_POD=$(kubectl get pods -n trino -o jsonpath='{.items[*].metadata.name}' | tr ' ' '\n' | grep coordinator)

kubectl exec -i -n trino "$COORDINATOR_POD" -- trino <<EOF

SELECT * FROM delta.information_schema.columns;
EOF

