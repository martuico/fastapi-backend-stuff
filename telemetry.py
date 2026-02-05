from typing import Any

from fastapi import FastAPI
from opentelemetry import trace
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import ConsoleSpanExporter, SimpleSpanProcessor
from opentelemetry.trace import Span


def server_request_hook(span: Span, scope: dict[str, Any]) -> None:
    if not span or not span.is_recording():
        return
    path = scope.get("path")
    if path is not None:
        span.set_attribute("http.route", path)

    if scope.get("method"):
        span.set_attribute("http.method", scope["method"])

    if span and span.is_recording():
        span.set_attribute("custom_user_attribute_from_request_hook", "some-value")


def client_request_hook(span: Span, scope: dict[str, Any], message: dict[str, Any]) -> None:
    if span and span.is_recording():
        span.set_attribute("custom_user_attribute_from_client_request_hook", "some-value")


def client_response_hook(span: Span, scope: dict[str, Any], message: dict[str, Any]) -> None:
    if span and span.is_recording():
        span.set_attribute("custom_user_attribute_from_response_hook", "some-value")


def instrument_fastapi(app: FastAPI) -> None:
    FastAPIInstrumentor().instrument_app(
        app,
        server_request_hook=server_request_hook,
        client_request_hook=client_request_hook,
        client_response_hook=client_response_hook,
    )


def setup_tracing() -> None:
    provider = TracerProvider()
    provider.add_span_processor(SimpleSpanProcessor(ConsoleSpanExporter()))

    trace.set_tracer_provider(provider)
