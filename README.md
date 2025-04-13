# Datapains Vanna AI Demo

This demo is based on the initial trino setup made [here](https://medium.com/@simon.thelin90/trino-minio-metastore-workshop-kubernetes-dbede7b1eca1).

Once you setup trino on your local k8s cluster, you can continue with this demo.

This is highly experimental, and VannaAI does not explicitly support trino, but I have
worked around it with their `run_sql` functionality.

## Requirements

* trino `see comment above`
* python3.11
* uv
* make
* gemini (free tier)

## Vanna AI Caveat

Since I run on mac, I had to pin:

`kaleido==0.2.1` to avoid issue:

When installing vanna it uses `0.2.1.post1`. Hence giving error:

* `error: Distribution `kaleido==0.2.1.post1 @ registry+https://pypi.org/simple` can't be installed because it doesn't have a source distribution or wheel for the current platform`

## Setup Gemini

Head out to google [AI Studio And Create an API key](https://aistudio.google.com/apikey).

Once you have this you need to make sure either globally, or within your session you have:

```bash
export GEMINI_API_KEY=...
```

The rest of the demo assumes this.

## Data Source -  Table Definitions

### fact_video_plays
Fact table of video playback events. References dimensions: dim_videos (video_id), dim_categories (category_id), dim_creators (creator_id), dim_users (user_id).

### dim_videos
Dimension table describing videos

### dim_categories
Dimension table categorising video content

### dim_creators
Dimension table containing video creator details

### dim_users
Dimension table describing user/viewer metadata

## Context

```bash
                  dim_categories
                        │
                        │
dim_creators─────fact_video_plays─────dim_videos
                        │
                        │
                    dim_users
```

## Setup

```bash
uv venv
```

```bash
make setup-environment
```

## Run App

### Run with training

```bash
make run-app TRAIN=--train
```

### Run without training

```bash
make run-app
```

## Access UI

* [local vanna ai setup](http://localhost:8084)
