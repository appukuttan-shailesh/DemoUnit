import json
from hbp_validation_framework import TestLibrary

test_library = TestLibrary("shailesh")

list_of_test_definitions = []
test_aliases = ["VF_RestingPotential",
                "VF_InputResistance",
                "VF_AP_Height",
                "VF_AP_HalfWidth"]

for t_alias in test_aliases:
    test_info = test_library.get_test_definition(alias=t_alias)
    list_of_test_definitions.append(test_info)

with open("VF_test_info.json", "w") as f:
    json.dump(list_of_test_definitions, f, indent=4, sort_keys=True)