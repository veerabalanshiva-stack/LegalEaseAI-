from google import genai
from google.genai import types

from config import settings


class GeminiConfigurationError(Exception):
    pass


class GeminiGenerationError(Exception):
    pass


class GeminiDocumentGenerator:

    def __init__(self):
        if not settings.GEMINI_API_KEY:
            raise GeminiConfigurationError(
                "GEMINI_API_KEY is missing. "
                "Please add your Gemini API key to the .env file."
            )

        self.client = genai.Client(
            api_key=settings.GEMINI_API_KEY
        )

        self.model_name = settings.GEMINI_MODEL

    def build_prompt(
        self,
        document_type,
        parties,
        terms,
        dates
    ):

        prompt = f"""
You are LegalEase, an AI-assisted legal document drafting system.

Create a professional legal document draft using ONLY the
information supplied by the user.

IMPORTANT RULES:

1. Do not invent facts.
2. Do not invent names.
3. Do not invent addresses.
4. Do not invent dates.
5. Do not invent monetary amounts.
6. Do not invent jurisdictions.
7. If important information is missing, use:
   [INSERT INFORMATION]
8. Do not claim that the document is legally valid.
9. Do not claim that the document is legally enforceable.
10. This document is an AI-assisted draft and must be reviewed
    by a qualified legal professional before use.
11. Use formal professional legal language.
12. Maintain consistency throughout the document.
13. Use numbered sections.
14. Use headings where appropriate.
15. Do not wrap the answer inside a Markdown code block.

DOCUMENT TYPE:
{document_type}

PARTIES:
{parties}

TERMS AND CONDITIONS:
{terms}

DATE INFORMATION:
{dates}

Use the following structure where appropriate:

1. Document Title
2. Effective Date
3. Parties
4. Introduction / Purpose
5. Definitions
6. Main Terms and Conditions
7. Payment
8. Confidentiality
9. Intellectual Property
10. Term and Termination
11. Liability
12. Governing Law
13. Dispute Resolution
14. Severability
15. Entire Agreement
16. Signatures

Only include sections relevant to the document.

If information required for a section was not supplied,
use [INSERT INFORMATION].

At the end add:

DRAFTING NOTICE

This document is an AI-assisted draft and should be reviewed
by a qualified legal professional before signing, filing,
or relying upon it.
"""

        return prompt.strip()

    def generate_document(
        self,
        document_type,
        parties,
        terms,
        dates
    ):

        prompt = self.build_prompt(
            document_type=document_type,
            parties=parties,
            terms=terms,
            dates=dates
        )

        try:
            response = self.client.models.generate_content(
                model=self.model_name,
                contents=prompt,
                config=types.GenerateContentConfig(
                    temperature=0.2,
                    max_output_tokens=8192
                )
            )

        except Exception as error:
            raise GeminiGenerationError(
                f"Gemini API error: {error}"
            ) from error

        generated_text = response.text

        if not generated_text:
            raise GeminiGenerationError(
                "Gemini returned an empty response."
            )

        generated_text = generated_text.strip()

        return generated_text[:settings.MAX_GENERATED_CHARS]