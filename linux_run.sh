#!/usr/bin/env bash
source ./env/bin/activate
python3 ./ahref_get_backlink.py
python3 ./ahref_batch_analysis.py
python3 ./filter_data.py