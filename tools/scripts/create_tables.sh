#!/bin/bash

COORDINATOR_POD=$(kubectl get pods -n trino -o jsonpath='{.items[*].metadata.name}' | tr ' ' '\n' | grep coordinator)

kubectl exec -i -n trino "$COORDINATOR_POD" -- trino <<EOF

CREATE SCHEMA IF NOT EXISTS delta.gold;

CREATE TABLE IF NOT EXISTS delta.gold.fact_video_plays (
    play_id BIGINT,
    video_id BIGINT,
    user_id BIGINT,
    category_id BIGINT,
    creator_id BIGINT,
    play_timestamp TIMESTAMP WITH TIME ZONE,
    watch_duration_seconds INTEGER,
    ingest_date DATE
);

CREATE TABLE IF NOT EXISTS delta.gold.dim_videos (
    video_id BIGINT,
    title VARCHAR,
    description VARCHAR,
    duration_seconds INTEGER,
    upload_timestamp TIMESTAMP WITH TIME ZONE,
    ingest_date DATE
);

CREATE TABLE IF NOT EXISTS delta.gold.dim_categories (
    category_id BIGINT,
    category_name VARCHAR,
    ingest_date DATE
);

CREATE TABLE IF NOT EXISTS delta.gold.dim_creators (
    creator_id BIGINT,
    creator_name VARCHAR,
    channel_name VARCHAR,
    join_date DATE,
    ingest_date DATE
);

CREATE TABLE IF NOT EXISTS delta.gold.dim_users (
    user_id BIGINT,
    user_name VARCHAR,
    subscription_type VARCHAR,
    registration_date DATE,
    ingest_date DATE
);
EOF