import base64
import json
import logging
import re
from typing import Dict, Any, Optional, List
import httpx
from pydantic import ValidationError
from .config import config
from .models import ExtractedItem, ExtractionResponse

logger = logging.getLogger("gemma_client")

SYSTEM_PROMPT = (
    "You are a medical text recognition tool. Read all visible medicine brand names, "
    "active chemical molecules, and dosage strengths from the image. "
    "Return ONLY a valid JSON object matching this schema, with no preamble or markdown ticks:\n"
    "{\"items\": [{\"raw_text\": \"...\", \"brand\": \"...\", \"molecule\": \"...\", \"strength\": \"...\"}]}"
)

class GemmaClient:
    def __init__(self):
        self.provider = config.GEMMA_PROVIDER.lower().strip()
        self.base_url = config.GEMMA_BASE_URL.rstrip("/")
        self.api_key = config.GEMMA_API_KEY.strip()
        self.model = config.GEMMA_MODEL.strip()
        self.timeout = config.GEMMA_TIMEOUT_SECONDS

    async def extract_from_image(self, image_bytes: bytes, filename: str = "upload.jpg") -> ExtractionResponse:
        base64_data = base64.b64encode(image_bytes).decode("utf-8")
        data_url = f"data:image/jpeg;base64,{base64_data}"

        # 1 attempt + 1 retry = 2 attempts total
        for attempt in range(2):
            try:
                content = await self._call_model(data_url, base64_data)
                items = self._parse_and_validate(content)
                if items:
                    return ExtractionResponse(
                        success=True,
                        model_used=self.model,
                        items=items
                    )
            except Exception as e:
                logger.warning(f"[GemmaClient] Attempt {attempt + 1} failed: {e}")
                if attempt == 1:
                    break

        return ExtractionResponse(
            success=False,
            model_used=self.model,
            items=[],
            warning="Scan unavailable, type the name instead"
        )

    async def _call_model(self, data_url: str, raw_base64: str) -> str:
        headers = {
            "Content-Type": "application/json"
        }
        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"

        if self.provider == "ollama":
            url = f"{self.base_url}/api/chat"
            payload = {
                "model": self.model,
                "messages": [
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {
                        "role": "user",
                        "content": "Extract medicine brand, molecule, and strength from this image in JSON format.",
                        "images": [raw_base64]
                    }
                ],
                "stream": False,
                "format": "json",
                "options": {
                    "temperature": 0.0
                }
            }
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                resp = await client.post(url, json=payload, headers=headers)
                resp.raise_for_status()
                data = resp.json()
                return data.get("message", {}).get("content", "")

        else:
            # Default: openai_compat (e.g. NVIDIA API https://integrate.api.nvidia.com/v1)
            url = f"{self.base_url}/chat/completions"
            payload = {
                "model": self.model,
                "messages": [
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": "Extract all medicine brand names, molecules, and strengths in JSON format {items: [{raw_text, brand, molecule, strength}]}"},
                            {"type": "image_url", "image_url": {"url": data_url}}
                        ]
                    }
                ],
                "temperature": 0.0,
                "response_format": {"type": "json_object"}
            }
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                resp = await client.post(url, json=payload, headers=headers)
                resp.raise_for_status()
                data = resp.json()
                choices = data.get("choices", [])
                if choices:
                    return choices[0].get("message", {}).get("content", "")
                return ""

    def _parse_and_validate(self, text: str) -> List[ExtractedItem]:
        clean = text.strip()
        clean = re.sub(r"^```(?:json)?\s*", "", clean, flags=re.MULTILINE)
        clean = re.sub(r"\s*```$", "", clean, flags=re.MULTILINE).strip()

        try:
            parsed = json.loads(clean)
            raw_items = parsed.get("items", [])
            valid_items: List[ExtractedItem] = []
            for item in raw_items:
                extracted = ExtractedItem(
                    raw_text=item.get("raw_text") or item.get("brand") or "",
                    brand=item.get("brand"),
                    molecule=item.get("molecule"),
                    strength=item.get("strength")
                )
                valid_items.append(extracted)
            return valid_items
        except (json.JSONDecodeError, ValidationError) as e:
            logger.warning(f"Validation error parsing Gemma response: {e}")
            return []

gemma_client = GemmaClient()
