"""
HVF Media Matrix - Media Processing Subsystem (Private)
Package Initialization and Secure Endpoint Exposure.
Engineered to restrict internal imports and prevent namespace pollution.
"""
__version__ = "1.0.0"

# Expose ONLY the Orchestrator to the broader system. 
# The Ingestor, Transcoder, and Gateway remain encapsulated and protected.
from .hvf_media_orchestrator import HVFMediaOrchestrator

__all__ = ["HVFMediaOrchestrator"]