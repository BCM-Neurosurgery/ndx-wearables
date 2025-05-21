# -*- coding: utf-8 -*-
import os.path

from pynwb.spec import NWBNamespaceBuilder, export_spec, NWBGroupSpec, NWBAttributeSpec
from wearables_infrastructure import make_wearables_infrastructure

# TODO: import other spec classes as needed
# from pynwb.spec import NWBDatasetSpec, NWBLinkSpec, NWBDtypeSpec, NWBRefSpec
import sleep
import hrv
import vo2max

def main():
    # these arguments were auto-generated from your cookiecutter inputs
    ns_builder = NWBNamespaceBuilder(
        name="""ndx-wearables""",
        version="""0.1.0""",
        doc="""Store data from human wearables""",
        author=[
            "Tomek", 
        ],
        contact=[
            "tomek.fraczek@bcm.edu", 
        ],
    )
    ns_builder.include_namespace("core")
    ns_builder.include_namespace("ndx-events")
    
    # TODO: if your extension builds on another extension, include the namespace
    # of the other extension below
    # ns_builder.include_namespace("ndx-other-extension")

    # TODO: define your new data types
    # see https://pynwb.readthedocs.io/en/stable/tutorials/general/extensions.html
    # for more information

    wearables_infra_datastructures = make_wearables_infrastructure()
    sleep_stage_series = sleep.make_sleep_stage()
    hrv_series = hrv.make_hrv_stage()
    vo2max_series = vo2max.make_vo2max_stage()

    # TODO: add all of your new data types to this list
    #new_data_types = [sleep_stage_series, *wearables_infra_datastructures]
    # new_data_types = [hrv_series]
    #new_data_types = [vo2max_series, sleep_stage_series]
    
    # Combine all series types
    new_data_types = [*wearables_infra_datastructures, hrv_series, vo2max_series, sleep_stage_series]



    # export the spec to yaml files in the spec folder
    output_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "spec"))
    export_spec(ns_builder, new_data_types, output_dir)


if __name__ == "__main__":
    # usage: python create_extension_spec.py
    main()
