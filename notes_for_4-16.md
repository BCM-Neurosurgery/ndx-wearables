
Step	              File	                            Action
1	spec/ndx-wearables.extensions.yaml	                Add WearableEvents spec
2	src/spec/wearables_infrastructure.py	            Add Python-spec definition of WearableEvents
3	src/spec/create_extension_spec.py	                Re-run this to generate updated YAML
4	src/pynwb/ndx_wearables/wearables_classes.py        (optional)	Register a class for custom logic
5	src/pynwb/tests/test_wearables_infrastructure.py	Add tests for WearableEvents


