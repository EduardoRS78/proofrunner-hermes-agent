import ipaddress
import re
import socket
from urllib.parse import urlsplit, urlunsplit, unquote

class SafetyError(RuntimeError):
    pass

def origin(url):
    p = urlsplit(url)
    if p.scheme not in {"http", "https"} or not p.hostname or p.username or p.password:
        raise SafetyError("Only HTTP(S) URLs without embedded credentials are allowed")
    return (p.scheme, p.hostname.lower(), p.port or (443 if p.scheme == "https" else 80))

def safe_url(url):
    p = urlsplit(url)
    return urlunsplit((p.scheme, p.netloc, p.path, "", ""))

class Policy:
    def __init__(self, url, interactions=False, local_demo=False):
        self.allowed_origin = origin(url)
        self.interactions = interactions
        self.local_demo = local_demo
        self.check_url(url)

    def check_url(self, url):
        o = origin(url)
        if o != self.allowed_origin:
            raise SafetyError("Cross-origin request blocked")
        addresses = socket.getaddrinfo(o[1], o[2], type=socket.SOCK_STREAM)
        for address in addresses:
            ip = ipaddress.ip_address(address[4][0])
            if not ip.is_global and not (self.local_demo and ip.is_loopback):
                raise SafetyError("Private, metadata, and local networks blocked outside built-in demo")
        if re.search(r"(?:delete|destroy|purchase|payment|pay-now|place-order|send-message)", unquote(urlsplit(url).path), re.I):
            raise SafetyError("Potentially destructive endpoint blocked")

    def check_action(self, step, descriptor=""):
        if step["action"] in {"click", "fill", "fill_secret", "select"}:
            if not self.interactions:
                raise SafetyError("Interaction requires --allow-interactions for an authorized test environment")
            if re.search(r"\b(pay|payment|purchase|buy|delete|destroy|send|transfer|pagar|comprar|excluir|apagar|enviar|transferir)\b|place order|finalizar compra", step["target"] + " " + descriptor, re.I):
                raise SafetyError("Potentially destructive action blocked; use a test-specific flow")

def redact(value, secrets):
    if isinstance(value, str):
        for secret in sorted((s for s in secrets if s), key=len, reverse=True):
            value = value.replace(secret, "[REDACTED]")
        return value
    if isinstance(value, list):
        return [redact(v, secrets) for v in value]
    if isinstance(value, dict):
        return {k:redact(v, secrets) for k,v in value.items()}
    return value
