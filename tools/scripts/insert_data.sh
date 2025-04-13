#!/bin/bash

COORDINATOR_POD=$(kubectl get pods -n trino -o jsonpath='{.items[*].metadata.name}' | tr ' ' '\n' | grep coordinator)

# We make sure we delete+insert to keep data idempotent for basic poc
kubectl exec -i -n trino "$COORDINATOR_POD" -- trino <<EOF
SET SESSION delta.vacuum_min_retention='0s';

DELETE FROM delta.gold.fact_video_plays WHERE TRUE;
INSERT INTO delta.gold.fact_video_plays
(play_id, video_id, user_id, category_id, creator_id, play_timestamp, watch_duration_seconds, ingest_date)
VALUES
(1001, 201, 301, 401, 501, TIMESTAMP '2025-04-13 10:30:00 UTC', 360, DATE '2025-04-13'),
(1002, 202, 302, 402, 502, TIMESTAMP '2025-04-13 11:00:00 UTC', 120, DATE '2025-04-13'),
(1003, 203, 303, 401, 501, TIMESTAMP '2025-04-13 12:15:00 UTC', 480, DATE '2025-04-13');
ALTER TABLE delta.gold.fact_video_plays EXECUTE OPTIMIZE;
ANALYZE delta.gold.fact_video_plays;
CALL delta.system.vacuum('gold', 'fact_video_plays', '0s');

DELETE FROM delta.gold.dim_videos WHERE TRUE;
INSERT INTO delta.gold.dim_videos
(video_id, title, description, duration_seconds, upload_timestamp, ingest_date)
VALUES
(201, 'Introduction to Star Schema', 'A beginner-friendly introduction', 600, TIMESTAMP '2025-03-01 09:00:00 UTC', DATE '2025-03-01'),
(202, 'Advanced Trino Queries', 'Deep dive into Trino', 1200, TIMESTAMP '2025-03-05 12:00:00 UTC', DATE '2025-03-05'),
(203, 'Video Analytics 101', 'Understanding video analytics', 900, TIMESTAMP '2025-03-10 15:00:00 UTC', DATE '2025-03-10');
ALTER TABLE delta.gold.dim_videos EXECUTE OPTIMIZE;
ANALYZE delta.gold.dim_videos;
CALL delta.system.vacuum('gold', 'dim_videos', '0s');

DELETE FROM delta.gold.dim_categories WHERE TRUE;
INSERT INTO delta.gold.dim_categories
(category_id, category_name, ingest_date)
VALUES
(401, 'Education', DATE '2025-01-01'),
(402, 'Technology', DATE '2025-01-01'),
(403, 'Entertainment', DATE '2025-01-01');
ALTER TABLE delta.gold.dim_categories EXECUTE OPTIMIZE;
ANALYZE delta.gold.dim_categories;
CALL delta.system.vacuum('gold', 'dim_categories', '0s');

DELETE FROM delta.gold.dim_creators WHERE TRUE;
INSERT INTO delta.gold.dim_creators
(creator_id, creator_name, channel_name, join_date, ingest_date)
VALUES
(501, 'Alice Johnson', 'Data Wizardry', DATE '2024-05-15', DATE '2025-01-01'),
(502, 'Bob Smith', 'Tech Talks', DATE '2024-07-20', DATE '2025-01-01');
ALTER TABLE delta.gold.dim_creators EXECUTE OPTIMIZE;
ANALYZE delta.gold.dim_creators;
CALL delta.system.vacuum('gold', 'dim_creators', '0s');

DELETE FROM delta.gold.dim_users WHERE TRUE;
INSERT INTO delta.gold.dim_users
(user_id, user_name, subscription_type, registration_date, ingest_date)
VALUES
(301, 'Charlie Brown', 'Premium', DATE '2025-02-20', DATE '2025-02-20'),
(302, 'Dana White', 'Free', DATE '2025-03-01', DATE '2025-03-01'),
(303, 'Eve Black', 'Premium', DATE '2025-01-15', DATE '2025-01-15');
ALTER TABLE delta.gold.dim_users EXECUTE OPTIMIZE;
ANALYZE delta.gold.dim_users;
CALL delta.system.vacuum('gold', 'dim_users', '0s');
EOF
