#!/bin/bash

source /home/junkyul/oss/agentics_public/data_experiments/Agentics/.venv/bin/activate
cd /home/junkyul/oss/agentics_public/data_experiments/Agentics/applications/data_wrangling


export MODEL_ID=watsonx/openai/gpt-oss-120b
python data_wrangling.py --csv-file buy_test_with_fewshots__k=0.csv --impute-col manufacturer
python data_wrangling.py --csv-file buy_test_with_fewshots__k=1.csv --impute-col manufacturer
python data_wrangling.py --csv-file buy_test_with_fewshots__k=2.csv --impute-col manufacturer
python data_wrangling.py --csv-file restaurant_test_with_fewshots__k=0.csv --impute-col city
python data_wrangling.py --csv-file restaurant_test_with_fewshots__k=1.csv --impute-col city
python data_wrangling.py --csv-file restaurant_test_with_fewshots__k=2.csv --impute-col city


export MODEL_ID=watsonx/meta-llama/llama-3-3-70b-instruct
python data_wrangling.py --csv-file buy_test_with_fewshots__k=0.csv --impute-col manufacturer
python data_wrangling.py --csv-file buy_test_with_fewshots__k=1.csv --impute-col manufacturer
python data_wrangling.py --csv-file buy_test_with_fewshots__k=2.csv --impute-col manufacturer
python data_wrangling.py --csv-file restaurant_test_with_fewshots__k=0.csv --impute-col city
python data_wrangling.py --csv-file restaurant_test_with_fewshots__k=1.csv --impute-col city
python data_wrangling.py --csv-file restaurant_test_with_fewshots__k=2.csv --impute-col city


export MODEL_ID=watsonx/meta-llama/llama-4-maverick-17b-128e-instruct-fp8
python data_wrangling.py --csv-file buy_test_with_fewshots__k=0.csv --impute-col manufacturer
python data_wrangling.py --csv-file buy_test_with_fewshots__k=1.csv --impute-col manufacturer
python data_wrangling.py --csv-file buy_test_with_fewshots__k=2.csv --impute-col manufacturer
python data_wrangling.py --csv-file restaurant_test_with_fewshots__k=0.csv --impute-col city
python data_wrangling.py --csv-file restaurant_test_with_fewshots__k=1.csv --impute-col city
python data_wrangling.py --csv-file restaurant_test_with_fewshots__k=2.csv --impute-col city
