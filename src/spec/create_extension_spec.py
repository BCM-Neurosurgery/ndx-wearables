# -*- coding: utf-8 -*-
import os.path

from pynwb.spec import NWBNamespaceBuilder, export_spec, NWBGroupSpec, NWBAttributeSpec

# TODO: import other spec classes as needed
# from pynwb.spec import NWBDatasetSpec, NWBLinkSpec, NWBDtypeSpec, NWBRefSpec
import sleep
import blood_oxygen as bo

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
    
    # TODO: if your extension builds on another extension, include the namespace
    # of the other extension below
    # ns_builder.include_namespace("ndx-other-extension")

    # TODO: define your new data types
    # see https://pynwb.readthedocs.io/en/stable/tutorials/general/extensions.html
    # for more information
    sleep_stage_series = sleep.make_sleep_stage()
    blood_oxygen = bo.make_blood_oxygen()

    # TODO: add all of your new data types to this list
    new_data_types = [sleep_stage_series, blood_oxygen]

    # export the spec to yaml files in the spec folder
    output_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "spec"))
    export_spec(ns_builder, new_data_types, output_dir)


if __name__ == "__main__":
    # usage: python create_extension_spec.py
    main()
