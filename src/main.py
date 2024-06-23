import httpx
from fastapi import FastAPI, HTTPException

from src.helpers import fetch_data, calculate_credits_cost
from src.models import Report, Usage, FetchMessagesResponse, GetUsageResponse

app = FastAPI()

MESSAGES_API = "https://owpublic.blob.core.windows.net/tech-task/messages/current-period"
REPORTS_API = "https://owpublic.blob.core.windows.net/tech-task/reports"


@app.get("/usage")
async def get_usage():
    try:
        usage_resp = await fetch_data(MESSAGES_API, FetchMessagesResponse)
        messages = usage_resp.messages
        usage = []

        for message in messages:
            usage_item = Usage(
                message_id=message.id,
                timestamp=message.timestamp,
                credits_used=0.0,
            )

            if message.report_id:
                try:
                    report = await fetch_data(f"{REPORTS_API}/{message.report_id}", Report)
                    usage_item.report_name = report.name
                    if report.credits_cost is not None:
                        usage_item.credits_used = report.credits_cost
                    else:
                        usage_item.credits_used = calculate_credits_cost(message)
                except httpx.HTTPStatusError as e:
                    if e.response.status_code == 404:
                        usage_item.credits_used = calculate_credits_cost(message)
                    else:
                        raise

            usage.append(usage_item)

        return GetUsageResponse(usage=usage)
    except httpx.HTTPStatusError as e:
        return HTTPException(status_code=e.response.status_code, detail=e.response.json())


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
