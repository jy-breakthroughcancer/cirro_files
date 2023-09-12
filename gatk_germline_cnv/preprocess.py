#!/usr/bin/env python3

import json
from cirro.helpers.preprocess_dataset import PreprocessDataset

s = PreprocessDataset.from_running()
json.dump(ds.params, open('inputs.0.json', 'w'))
