import time
import os
from services.freemail import EmailService


def create_temp_email(duckmail_api_base, duckmail_bearer, default_proxy, freemail_worker_domain, freemail_token, user_agent=None):
    """Create a temporary email using freemail worker only.

    Signature kept for compatibility but duckmail args are ignored.
    Returns (email, password, mail_token) — password is empty for freemail.
    """
    if not freemail_worker_domain or not freemail_token:
        raise Exception("freemail 未配置：请在 config.json 中设置 freemail_worker_domain 与 freemail_token 或通过环境变量提供。")

    # ensure EmailService can read the values (its current implementation reads env)
    os.environ.setdefault("WORKER_DOMAIN", freemail_worker_domain)
    os.environ.setdefault("FREEMAIL_TOKEN", freemail_token)

    proxies = {}
    if default_proxy:
        proxies = {"http": default_proxy, "https": default_proxy}

    es = EmailService(proxies=proxies)
    email, mailbox = es.create_email()
    if not email:
        raise Exception("freemail: 创建邮箱失败")
    return email, "", mailbox


def wait_for_verification_email(duckmail_api_base, mail_token: str, timeout: int = 120, user_agent=None, proxy=None, freemail_worker_domain=None, freemail_token=None):
    """Poll freemail worker for verification code. other args ignored for compatibility."""
    if not freemail_worker_domain or not freemail_token:
        raise Exception("freemail 未配置：无法轮询验证码")

    os.environ.setdefault("WORKER_DOMAIN", freemail_worker_domain)
    os.environ.setdefault("FREEMAIL_TOKEN", freemail_token)
    proxies = {}
    if proxy:
        proxies = {"http": proxy, "https": proxy}

    es = EmailService(proxies=proxies)
    start_time = time.time()
    while time.time() - start_time < timeout:
        code = es.fetch_verification_code(mail_token, max_attempts=1, debug=False)
        if code:
            return code
        time.sleep(3)
    return None
