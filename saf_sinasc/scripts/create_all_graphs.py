"""
This script is responsible for creating all graphs used on report

Ultimately, copying the created "/graphs" directory into overleaf project
    should be enough to update the report.
"""

import time

from saf_sinasc.scripts.create_data_graphs import create_all_data_graphs
from saf_sinasc.scripts.create_model_graphs import create_all_model_graphs

start_time = time.time()

create_all_data_graphs()
create_all_model_graphs()

end_time = time.time()

print("Time elapsed: ", end_time - start_time, "seconds")
