make_report: ../data/full_data_feather.feather q1.py q2.py q3.py q4.py
	pweave -f markdown README.pmd
	@echo "Report has been created: README.md"

../data/full_data_csv.csv:
	curl http://prod.publicdata.landregistry.gov.uk.s3-website-eu-west-1.amazonaws.com/pp-2020.csv -L -o ../data/full_data_csv.csv

../data/full_data_feather.feather: ../data/full_data_csv.csv
	python3 0prepare_data.py

install_required_pip_packages: install_pip
	pip3 install -r ../requirements.txt
	@echo "Now run this to go into the virtual environment: source ../venv/bin/activate"

install_pip:
	sudo -H python3 -m ensurepip

code_quality_metrics:
	@echo "Codeclimate is available from: https://github.com/codeclimate/codeclimate"
	codeclimate analyze
