import argparse
import json
import logging
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Optional

# Configure root logger
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s - %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)
logger = logging.getLogger(__name__)


@dataclass
class Config:
    """Configuration model for the Signalink presentation system."""

    signalink_endpoint: str
    api_key: str
    data_path: Path
    output_path: Path
    log_level: str = "INFO"

    @staticmethod
    def from_file(file_path: Path) -> "Config":
        """Load configuration from a JSON file."""
        if not file_path.is_file():
            raise FileNotFoundError(f"Configuration file not found: {file_path}")
        with file_path.open("r", encoding="utf-8") as f:
            data = json.load(f)

        required_keys = {"signalink_endpoint", "api_key", "data_path", "output_path"}
        missing = required_keys - data.keys()
        if missing:
            raise ValueError(f"Missing required config keys: {', '.join(missing)}")

        return Config(
            signalink_endpoint=data["signalink_endpoint"],
            api_key=data["api_key"],
            data_path=Path(data["data_path"]).expanduser().resolve(),
            output_path=Path(data["output_path"]).expanduser().resolve(),
            log_level=data.get("log_level", "INFO"),
        )


class SignalinkClient:
    """Placeholder client for interacting with the Signalink API."""

    def __init__(self, endpoint: str, api_key: str) -> None:
        self.endpoint = endpoint.rstrip("/")
        self.api_key = api_key
        logger.debug("SignalinkClient initialized with endpoint %s", self.endpoint)

    def send_payload(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Simulate sending a payload to Signalink.

        In a real implementation this would perform an HTTP request.
        """
        logger.info("Sending payload to Signalink: %s", payload)
        # Mock response
        response = {"status": "success", "received": payload}
        logger.debug("Received mock response: %s", response)
        return response


class DataProcessor:
    """Core data processing logic."""

    def __init__(self, data_path: Path) -> None:
        self.data_path = data_path
        logger.debug("DataProcessor initialized with data_path %s", self.data_path)

    def load_data(self) -> List[Dict[str, Any]]:
        """Load JSON lines data from the configured data_path."""
        if not self.data_path.is_file():
            raise FileNotFoundError(f"Data file not found: {self.data_path}")

        records: List[Dict[str, Any]] = []
        with self.data_path.open("r", encoding="utf-8") as f:
            for line_number, line in enumerate(f, start=1):
                line = line.strip()
                if not line:
                    continue
                try:
                    record = json.loads(line)
                    records.append(record)
                except json.JSONDecodeError as e:
                    logger.warning(
                        "Skipping invalid JSON at line %d: %s", line_number, e
                    )
        logger.info("Loaded %d records from %s", len(records), self.data_path)
        return records

    @staticmethod
    def transform(record: Dict[str, Any]) -> Dict[str, Any]:
        """
        Apply transformation logic to a single record.

        This placeholder simply adds a processed flag.
        """
        transformed = dict(record)
        transformed["processed"] = True
        return transformed

    def process(self, records: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Process a list of records."""
        processed = [self.transform(r) for r in records]
        logger.info("Transformed %d records", len(processed))
        return processed


def save_results(results: List[Dict[str, Any]], output_path: Path) -> None:
    """Write processed results as JSON lines to the output file."""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8") as f:
        for item in results:
            json.dump(item, f)
            f.write("\n")
    logger.info("Saved %d results to %s", len(results), output_path)


def parse_args(argv: Optional[List[str]] = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Signalink presentation preparation script"
    )
    parser.add_argument(
        "-c",
        "--config",
        type=Path,
        required=True,
        help="Path to JSON configuration file",
    )
    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="Enable debug level logging",
    )
    return parser.parse_args(argv)


def main(argv: Optional[List[str]] = None) -> int:
    args = parse_args(argv)

    # Load configuration
    try:
        config = Config.from_file(args.config)
    except Exception as exc:
        logger.error("Failed to load configuration: %s", exc)
        return 1

    # Adjust log level if verbose flag is set
    if args.verbose:
        logger.setLevel(logging.DEBUG)
        logger.debug("Verbose mode enabled, log level set to DEBUG")

    logger.setLevel(getattr(logging, config.log_level.upper(), logging.INFO))

    # Initialize components
    client = SignalinkClient(config.signalink_endpoint, config.api_key)
    processor = DataProcessor(config.data_path)

    try:
        raw_data = processor.load_data()
        processed_data = processor.process(raw_data)
        for item in processed_data:
            client.send_payload(item)
        save_results(processed_data, config.output_path)
    except Exception as exc:
        logger.exception("An unexpected error occurred: %s", exc)
        return 1

    logger.info("Script completed successfully")
    return 0


if __name__ == "__main__":
    sys.exit(main())