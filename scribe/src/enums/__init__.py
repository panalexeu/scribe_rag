from src.system.utils import JsonEnum

# Unstructured document processing
UnstructuredPostprocessors = JsonEnum('postprocessors', './src/enums/unstructured_loader.json')
ChunkingStrategy = JsonEnum('chunking_strategy', './src/enums/unstructured_loader.json')
