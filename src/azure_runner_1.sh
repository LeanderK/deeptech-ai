#!/usr/bin/env bash

# Mein key
source activate deeptachai
python -u image_preprocessing_script.py --start-index 0 --end-index 2000 \
--companies-pickle-path /home/sandro/Projekte/github_projects/deeptech-ai/data/raw/companies.pickle \
--azure-key efdb6416d7d34344b01f7fe6eec963d5 \
--num-workers 3 &> out_1.txt

