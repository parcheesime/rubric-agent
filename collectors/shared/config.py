"""Application configuration loaded from environment variables."""

from dataclasses import dataclass
import os

from dotenv import load_dotenv


load_dotenv()


@dataclass(frozen=True)
class R2Config:
    """Configuration required to connect to Cloudflare R2."""

    account_id: str
    access_key_id: str
    secret_access_key: str
    bucket_name: str

    @property
    def endpoint_url(self) -> str:
        """Return the Cloudflare R2 S3-compatible endpoint."""

        return f"https://{self.account_id}.r2.cloudflarestorage.com"


def get_r2_config() -> R2Config:
    """Load and validate Cloudflare R2 configuration."""

    environment_values = {
        "account_id": os.getenv("R2_ACCOUNT_ID"),
        "access_key_id": os.getenv("R2_ACCESS_KEY_ID"),
        "secret_access_key": os.getenv("R2_SECRET_ACCESS_KEY"),
        "bucket_name": os.getenv("R2_BUCKET_NAME"),
    }

    missing = [
        name
        for name, value in environment_values.items()
        if not value
    ]

    if missing:
        variable_names = ", ".join(
            f"R2_{name.upper()}" for name in missing
        )
        raise RuntimeError(
            f"Missing required environment variables: {variable_names}"
        )

    return R2Config(**environment_values)