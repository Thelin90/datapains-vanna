#!/bin/bash

COORDINATOR_POD=$(kubectl get pods -n trino -o jsonpath='{.items[*].metadata.name}' | tr ' ' '\n' | grep coordinator)

kubectl exec -i -n trino "$COORDINATOR_POD" -- trino <<EOF
COMMENT ON TABLE delta.gold.fact_video_plays IS 'Fact table of video playback events. References dimensions: dim_videos (video_id), dim_categories (category_id), dim_creators (creator_id), dim_users (user_id)';
COMMENT ON TABLE delta.gold.dim_videos IS 'Dimension table describing videos';
COMMENT ON TABLE delta.gold.dim_categories IS 'Dimension table categorising video content';
COMMENT ON TABLE delta.gold.dim_creators IS 'Dimension table containing video creator details';
COMMENT ON TABLE delta.gold.dim_users IS 'Dimension table describing user/viewer metadata';
EOF
