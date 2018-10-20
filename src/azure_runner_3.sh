#!/usr/bin/env bash

#leanders 1 . key

source activate deeptachai
python -u image_preprocessing_script.py --start-index 4001 --end-index 6000 \
--companies-pickle-path /home/sandro/Projekte/github_projects/deeptech-ai/data/raw/companies.pickle \
--azure-key badacbb7cd4644c783d1ed916bbe9ff0 \
--num-workers 3 &> out_3.txt

