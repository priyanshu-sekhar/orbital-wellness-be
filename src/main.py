import httpx
from fastapi import FastAPI, HTTPException
from starlette.middleware.cors import CORSMiddleware

from src.helpers import fetch_data, calculate_credits_cost
from src.models import Report, Usage, FetchMessagesResponse, GetUsageResponse

# Initialize FastAPI application
app = FastAPI()

# Add CORS middleware to allow requests from any origin
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Define the API endpoints for fetching messages and reports
MESSAGES_API = "https://owpublic.blob.core.windows.net/tech-task/messages/current-period"
REPORTS_API = "https://owpublic.blob.core.windows.net/tech-task/reports"


# Define the /usage endpoint
@app.get("/usage")
async def get_usage():
    try:
        # Fetch the messages data
        usage_resp = await fetch_data(MESSAGES_API, FetchMessagesResponse)
        messages = usage_resp.messages
        usage = []

        # Iterate over the messages to calculate the usage
        for message in messages:
            usage_item = Usage(
                message_id=message.id,
                timestamp=message.timestamp,
                credits_used=0.0,
            )

            # If a report_id is present, fetch the report data
            if message.report_id:
                try:
                    report = await fetch_data(f"{REPORTS_API}/{message.report_id}", Report)
                    usage_item.report_name = report.name
                    usage_item.credits_used = report.credit_cost
                except httpx.HTTPStatusError as e:
                    # If the report is not found, calculate the credits cost based on the message
                    if e.response.status_code == 404:
                        usage_item.credits_used = calculate_credits_cost(message)
                    else:
                        raise
            else:
                # If no report_id is present, calculate the credits cost based on the message
                usage_item.credits_used = calculate_credits_cost(message)

            usage.append(usage_item)

        return GetUsageResponse(usage=usage)
    except httpx.HTTPStatusError as e:
        # If an error occurs while fetching the data, return an HTTP exception with the error details
        return HTTPException(status_code=e.response.status_code, detail=e.response.json())
    except Exception as e:
        # If an unexpected error occurs, return an HTTP 500 error
        raise HTTPException(status_code=500, detail="Internal Server Error")


# Run the application using uvicorn
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
