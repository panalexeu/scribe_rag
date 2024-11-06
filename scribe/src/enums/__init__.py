from src.system.utils import JsonEnum

# Unstructured document processing
UnstructuredPostprocessors = JsonEnum('postprocessors', './unstructured_loader.json')
ChunkingStrategy = JsonEnum('chunking_strategy', './unstructured_loader.json')
