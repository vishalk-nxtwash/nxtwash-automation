"""Failed-API-call capture for test failure diagnostics.

Flags HTTP >= 400 responses, and write calls (POST/PUT/PATCH/DELETE) that
return HTTP 200 with an error ``statusCode`` in the JSON body.

DriverFactory enables Chrome's network performance log; on test failure the
root conftest calls ``failed_api_calls`` to pull every non-2xx API response
(with request payload and response body) seen during the test. Backend errors
the UI swallows silently — e.g. a 499 "already exists" on save — then show up
directly in the CI log instead of as a confusing downstream assertion.

Disable with NETWORK_CAPTURE=0.
"""
import json
import os

ENABLED = os.getenv("NETWORK_CAPTURE", "1").strip().lower() not in ("0", "false", "no")

# Only API traffic is interesting; static assets and analytics are noise.
_API_MARKER = "/api/"
_MAX_BODY = 2000
_WRITE_METHODS = ("POST", "PUT", "PATCH", "DELETE")


def chrome_logging_capabilities(options):
    """Turn on network-only performance logging for a ChromeOptions object."""
    if not ENABLED:
        return
    options.set_capability("goog:loggingPrefs", {"performance": "ALL"})
    options.add_experimental_option(
        "perfLoggingPrefs", {"enableNetwork": True, "enablePage": False}
    )


def failed_api_calls(driver):
    """Return non-2xx API calls from the performance log as a list of dicts.

    Drains the log buffer. Never raises — diagnostics must not mask the
    original failure.
    """
    if not ENABLED:
        return []
    try:
        entries = driver.get_log("performance")
    except Exception:  # noqa: BLE001
        return []

    requests, failures, write_candidates = {}, [], []
    for entry in entries:
        try:
            msg = json.loads(entry["message"])["message"]
        except (KeyError, ValueError):
            continue
        method, params = msg.get("method"), msg.get("params", {})
        if method == "Network.requestWillBeSent":
            req = params.get("request", {})
            if _API_MARKER in req.get("url", "") and req.get("method") != "OPTIONS":
                requests[params.get("requestId")] = req
        elif method == "Network.responseReceived":
            resp = params.get("response", {})
            req_id = params.get("requestId")
            if req_id not in requests:
                continue
            entry = {
                "requestId": req_id,
                "method": requests[req_id].get("method"),
                "url": resp.get("url"),
                "status": resp.get("status"),
                "request_body": (requests[req_id].get("postData") or "")[:_MAX_BODY],
            }
            if resp.get("status", 0) >= 400:
                failures.append(entry)
            elif entry["method"] in _WRITE_METHODS:
                # The app often answers HTTP 200 with the real error in the
                # body ({"statusCode": 499, "message": "... already exists"}).
                # Writes are few, so checking their bodies is cheap.
                write_candidates.append(entry)
        elif method == "Network.loadingFailed":
            req_id = params.get("requestId")
            if req_id in requests and not params.get("canceled"):
                failures.append({
                    "requestId": req_id,
                    "method": requests[req_id].get("method"),
                    "url": requests[req_id].get("url"),
                    "status": "network-error: %s" % params.get("errorText"),
                    "request_body": (requests[req_id].get("postData") or "")[:_MAX_BODY],
                })

    for entry in write_candidates:
        try:
            body = driver.execute_cdp_cmd(
                "Network.getResponseBody", {"requestId": entry["requestId"]}
            ).get("body", "")
            code = json.loads(body).get("statusCode") if body.strip().startswith("{") else None
        except Exception:  # noqa: BLE001
            continue
        if isinstance(code, int) and code >= 400:
            entry["status"] = "200 (body statusCode %s)" % code
            entry["response_body"] = body[:_MAX_BODY]
            failures.append(entry)

    for failure in failures:
        if "response_body" in failure:
            continue
        try:
            body = driver.execute_cdp_cmd(
                "Network.getResponseBody", {"requestId": failure["requestId"]}
            ).get("body", "")
        except Exception:  # noqa: BLE001
            body = "<body unavailable>"
        failure["response_body"] = body[:_MAX_BODY]
    return failures


def format_failures(failures):
    lines = []
    for f in failures:
        lines.append("%s %s -> %s" % (f["method"], f["url"], f["status"]))
        if f["request_body"]:
            lines.append("  request:  %s" % f["request_body"])
        lines.append("  response: %s" % f.get("response_body", ""))
    return "\n".join(lines)
