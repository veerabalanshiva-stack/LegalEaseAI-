from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from ai_core.gemini_generator import (
    GeminiDocumentGenerator,
    GeminiConfigurationError,
    GeminiGenerationError,
)


router = APIRouter()

generator = None


class DocumentRequest(BaseModel):
    document_type: str = Field(
        ...,
        min_length=2,
        max_length=200
    )

    parties: str = Field(
        ...,
        min_length=2,
        max_length=5000
    )

    terms: str = Field(
        ...,
        min_length=2,
        max_length=10000
    )

    dates: str = Field(
        ...,
        min_length=2,
        max_length=500
    )


class DocumentResponse(BaseModel):
    document: str
    model: str


def get_generator():
    global generator

    if generator is None:
        generator = GeminiDocumentGenerator()

    return generator


@router.post(
    "/generate",
    response_model=DocumentResponse
)
def generate_legal_document(
    request: DocumentRequest
):
    try:
        gemini = get_generator()

        generated_document = gemini.generate_document(
            document_type=request.document_type,
            parties=request.parties,
            terms=request.terms,
            dates=request.dates,
        )

        return {
            "document": generated_document,
            "model": gemini.model_name,
        }

    except GeminiConfigurationError as error:
        raise HTTPException(
            status_code=503,
            detail=str(error)
        )

    except GeminiGenerationError as error:
        raise HTTPException(
            status_code=502,
            detail=str(error)
        )

    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=f"Unexpected error: {error}"
        )