import os
import socket

from allauth.account.adapter import DefaultAccountAdapter
#uase phones IP

def get_lan_ip():
    """Find this laptop's current IP on the hotspot/Wi-Fi."""
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("10.255.255.255", 1))   # no data is actually sent
        return s.getsockname()[0]
    except Exception:
        return None
    finally:
        s.close()


class CustomAccountAdapter(DefaultAccountAdapter):
    def send_mail(self, template_prefix, email, context):
        ip = get_lan_ip() or os.getenv("LAN_IP")
        url = context.get("password_reset_url")
        if ip and url:
            for local in ("http://127.0.0.1:8000", "http://localhost:8000"):
                url = url.replace(local, f"http://{ip}:8000")
            context["password_reset_url"] = url
        super().send_mail(template_prefix, email, context)