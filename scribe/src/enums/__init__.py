from src.system.utils import JsonEnum

# Unstructured document processing
Postprocessor = JsonEnum('postprocessor', './src/enums/unstructured_loader.json')
ChunkingStrategy = JsonEnum('chunking_strategy', './src/enums/unstructured_loader.json')
ChatModelName = JsonEnum('model', './src/enums/chat_model.json')
