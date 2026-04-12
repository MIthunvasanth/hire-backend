"""
Coding Challenge API routes

Provides endpoints for secure code execution via Piston API
"""

from fastapi import APIRouter, HTTPException, Body
from pydantic import BaseModel, Field
from typing import Optional
from app.core.security import verify_token
import httpx
import json

router = APIRouter(prefix="/api/v1/coding", tags=["coding"])

# Constants
PISTON_API_BASE = "https://api.piston.codes"
MAX_CODE_LENGTH = 50000  # 50KB max code
MAX_INPUT_LENGTH = 10000  # 10KB max input
TIMEOUT_SECONDS = 30


class ExecuteCodeRequest(BaseModel):
    language: str = Field(..., min_length=1, max_length=50)
    code: str = Field(..., min_length=1, max_length=MAX_CODE_LENGTH)
    input: Optional[str] = Field(default="", max_length=MAX_INPUT_LENGTH)


class ExecuteCodeResponse(BaseModel):
    language: str
    version: str
    stdout: str
    stderr: str
    code: Optional[int]
    signal: Optional[str]
    execution_time: Optional[float] = None


class LanguageInfo(BaseModel):
    id: str
    name: str
    aliases: list[str]
    version: str


@router.get("/languages")
async def get_supported_languages() -> list[LanguageInfo]:
    """
    Get list of supported programming languages from Piston API
    """
    try:
        async with httpx.AsyncClient(timeout=10) as client:
            response = await client.get(f"{PISTON_API_BASE}/v1/runtimes")
            response.raise_for_status()

            languages = response.json()

            # Format response
            result = []
            seen = set()

            for lang in languages:
                lang_id = lang.get("language", "")
                if lang_id and lang_id not in seen:
                    seen.add(lang_id)
                    result.append(
                        LanguageInfo(
                            id=lang_id,
                            name=format_language_name(lang_id),
                            aliases=lang.get("aliases", []),
                            version=lang.get("version", "1.0.0"),
                        )
                    )

            return sorted(result, key=lambda x: x.name)

    except httpx.RequestError as e:
        raise HTTPException(
            status_code=503, detail=f"Failed to fetch languages: {str(e)}"
        )


@router.post("/execute", response_model=ExecuteCodeResponse)
async def execute_code(
    request: ExecuteCodeRequest,
    user_token: Optional[str] = None,
) -> ExecuteCodeResponse:
    """
    Execute code in the specified language

    - **language**: Programming language (e.g., 'python3', 'javascript')
    - **code**: Source code to execute (max 50KB)
    - **input**: Optional standard input (max 10KB)
    """

    # Validate language
    if not request.language or len(request.language) > 50:
        raise HTTPException(status_code=400, detail="Invalid language")

    # Validate code
    if not request.code or len(request.code) > MAX_CODE_LENGTH:
        raise HTTPException(
            status_code=400,
            detail=f"Code size exceeds maximum ({MAX_CODE_LENGTH} bytes)",
        )

    # Validate input
    if request.input and len(request.input) > MAX_INPUT_LENGTH:
        raise HTTPException(
            status_code=400,
            detail=f"Input size exceeds maximum ({MAX_INPUT_LENGTH} bytes)",
        )

    try:
        # Prepare Piston API request
        piston_request = {
            "language": request.language,
            "files": [
                {
                    "name": f"main.{get_file_extension(request.language)}",
                    "content": request.code,
                }
            ],
            "stdin": request.input or "",
            "run_timeout": TIMEOUT_SECONDS,
        }

        async with httpx.AsyncClient(timeout=TIMEOUT_SECONDS + 5) as client:
            response = await client.post(
                f"{PISTON_API_BASE}/v1/execute",
                json=piston_request,
            )
            response.raise_for_status()

            result = response.json()

            return ExecuteCodeResponse(
                language=result.get("language", request.language),
                version=result.get("version", "1.0.0"),
                stdout=result.get("run", {}).get("stdout", ""),
                stderr=result.get("run", {}).get("stderr", ""),
                code=result.get("run", {}).get("code"),
                signal=result.get("run", {}).get("signal"),
            )

    except httpx.RequestError as e:
        raise HTTPException(
            status_code=503, detail=f"Execution failed: {str(e)}"
        )
    except (json.JSONDecodeError, KeyError) as e:
        raise HTTPException(status_code=502, detail=f"Invalid response from Piston: {str(e)}")


def format_language_name(language_id: str) -> str:
    """Format language ID for display"""
    name_map = {
        "bash": "Bash",
        "csharp": "C#",
        "cpp": "C++",
        "c": "C",
        "clojure": "Clojure",
        "cobol": "COBOL",
        "crystal": "Crystal",
        "dart": "Dart",
        "elixir": "Elixir",
        "erlang": "Erlang",
        "emacs": "Emacs Lisp",
        "fortran": "Fortran",
        "go": "Go",
        "groovy": "Groovy",
        "haskell": "Haskell",
        "java": "Java",
        "javascript": "JavaScript",
        "kotlin": "Kotlin",
        "lua": "Lua",
        "nasm": "NASM",
        "objective-c": "Objective-C",
        "ocaml": "OCaml",
        "pascal": "Pascal",
        "perl": "Perl",
        "php": "PHP",
        "python": "Python",
        "python3": "Python 3",
        "r": "R",
        "ruby": "Ruby",
        "rust": "Rust",
        "scala": "Scala",
        "swift": "Swift",
        "typescript": "TypeScript",
        "vb": "Visual Basic",
        "zig": "Zig",
    }
    return name_map.get(language_id, language_id.capitalize())


def get_file_extension(language: str) -> str:
    """Get file extension for language"""
    extension_map = {
        "bash": "sh",
        "c": "c",
        "cpp": "cpp",
        "csharp": "cs",
        "clojure": "clj",
        "cobol": "cob",
        "crystal": "cr",
        "dart": "dart",
        "elixir": "exs",
        "erlang": "erl",
        "emacs": "el",
        "fortran": "f90",
        "go": "go",
        "groovy": "groovy",
        "haskell": "hs",
        "java": "java",
        "javascript": "js",
        "kotlin": "kt",
        "lua": "lua",
        "nasm": "asm",
        "objective-c": "m",
        "ocaml": "ml",
        "pascal": "pas",
        "perl": "pl",
        "php": "php",
        "python": "py",
        "python3": "py",
        "r": "R",
        "ruby": "rb",
        "rust": "rs",
        "scala": "scala",
        "swift": "swift",
        "typescript": "ts",
        "vb": "vb",
        "zig": "zig",
    }
    return extension_map.get(language, "txt")
