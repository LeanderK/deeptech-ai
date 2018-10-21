#!/usr/bin/env bash



#tatyanas key
source activate deeptachai
python -u image_preprocessing_script.py --start-index 2001 --end-index 4000 \
--companies-pickle-path /home/sandro/Projekte/github_projects/deeptech-ai/data/raw/companies.pickle \
--azure-key d5e8c84db0c04fdea75661297d0dff34 \
--num-workers 3 &> out_2.txt

