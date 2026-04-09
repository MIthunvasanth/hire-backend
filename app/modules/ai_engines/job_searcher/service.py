import httpx

from app.core.config import settings

from .schema import JobDetails, JobSearchResponse


async def search_jobs_service(data: dict) -> JobSearchResponse:
    if not settings.rapidapi_key:
        raise ValueError("RAPIDAPI_KEY is not configured on backend")

    params = {
        "query": data["query"],
        "page": data.get("page", 1),
        "num_pages": data.get("num_pages", 1),
        "country": data.get("country", "us"),
        "language": data.get("language"),
        "location": data.get("location"),
        "date_posted": data.get("date_posted", "all"),
        "work_from_home": data.get("work_from_home", False),
        "employment_types": data.get("employment_types"),
        "job_requirements": data.get("job_requirements"),
        "radius": data.get("radius"),
        "exclude_job_publishers": data.get("exclude_job_publishers"),
        "fields": data.get("fields"),
    }
    params = {key: value for key, value in params.items() if value not in (None, "")}
    headers = {
        "x-rapidapi-key": settings.rapidapi_key,
        "x-rapidapi-host": settings.rapidapi_host,
    }

    async def _execute_request(request_params: dict) -> httpx.Response:
        async with httpx.AsyncClient(timeout=45.0) as client:
            return await client.get(f"{settings.rapidapi_base_url}/search", params=request_params, headers=headers)

    try:
        response = await _execute_request(params)
    except httpx.TimeoutException as exc:
        raise ValueError("Job search provider timed out. Please retry in a few seconds.") from exc
    except httpx.RequestError as exc:
        raise ValueError(f"Unable to reach job provider: {exc}") from exc

    # Some location queries fail with strict country filters; retry once with 'all'.
    if response.status_code >= 400 and params.get("country") != "all":
        retry_params = {**params, "country": "all"}
        try:
            response = await _execute_request(retry_params)
            params = retry_params
        except httpx.TimeoutException as exc:
            raise ValueError("Job search provider timed out. Please retry in a few seconds.") from exc
        except httpx.RequestError as exc:
            raise ValueError(f"Unable to reach job provider: {exc}") from exc

    if response.status_code >= 400:
        raise ValueError(f"Job search API failed: {response.status_code} {response.text}")

    payload = response.json()
    jobs = [_map_job_item(item) for item in payload.get("data", [])]

    return JobSearchResponse(
        status=payload.get("status", "OK"),
        query=params["query"],
        page=params["page"],
        total_results=len(jobs),
        jobs=jobs,
    )


def _map_job_item(item: dict) -> JobDetails:
    return JobDetails(
        job_id=item.get("job_id", ""),
        title=item.get("job_title") or item.get("job_job_title") or "Untitled role",
        company=item.get("employer_name") or "Unknown company",
        location=item.get("job_location"),
        city=item.get("job_city"),
        state=item.get("job_state"),
        country=item.get("job_country"),
        is_remote=bool(item.get("job_is_remote", False)),
        employment_type=item.get("job_employment_type_text") or item.get("job_employment_type"),
        salary_min=item.get("job_min_salary"),
        salary_max=item.get("job_max_salary"),
        salary_currency=item.get("job_salary_currency"),
        posted_at=item.get("job_posted_at_datetime_utc"),
        posted_human_readable=item.get("job_posted_human_readable"),
        apply_link=item.get("job_apply_link"),
        publisher=item.get("job_publisher"),
        description=item.get("job_description"),
        apply_options=item.get("apply_options") or [],
        highlights=item.get("job_highlights") or {},
    )
