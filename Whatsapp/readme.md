```python
from twilio.twiml.messaging_response import MessagingResponse
from fastapi import FastAPI, Form, HTTPException
from twilio.twiml.messaging_response import MessagingResponse
import os
from starlette.responses import Response
# Initialize the FastAPI app
app = FastAPI()

twilio_account_sid = os.getenv('')
twilio_auth_token = os.getenv('')


@app.post("/whatsapp")
async def handle_whatsapp_message(Body: str = Form(...), From: str = Form(...)):
    try:
        print(Body)
              
        twiml = MessagingResponse()
        twiml.message("answer")
        
        return Response(content=twiml.to_xml(), media_type="application/xml")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Run the Flask app
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
```