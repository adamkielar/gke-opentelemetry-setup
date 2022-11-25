import logging
import httpx

from google.cloud import logging as gcp_logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.instrumentation.httpx import HTTPXClientInstrumentor
from opentelemetry import trace
from opentelemetry.exporter.cloud_trace import CloudTraceSpanExporter
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor

logging_client = gcp_logging.Client()
logging_client.setup_logging()

tracer_provider = TracerProvider()
cloud_trace_exporter = CloudTraceSpanExporter()
tracer_provider.add_span_processor(
    BatchSpanProcessor(cloud_trace_exporter)
)
trace.set_tracer_provider(tracer_provider)
tracer = trace.get_tracer(__name__)


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


FastAPIInstrumentor.instrument_app(app)
HTTPXClientInstrumentor().instrument()


@app.get("/home")
async def home():
    with tracer.start_as_current_span("call_test_endpoint") as current_span:
        async with httpx.AsyncClient() as client:
            r = await client.get("https://test.pl/")
        logging.info(f"Received response {r}")
        current_span.add_event(name="get_home")
        home = await get_home()
        logging.info(f"Calling function get_home: {home}")
        return home


async def get_home():
    data_dict = {"hello": "world"}
    logging.info("message field", extra={"json_fields": data_dict})
    return "Hello, World"
