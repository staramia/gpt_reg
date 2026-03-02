import os
import json


def _load_config(base_path):
    """从 config.json 加载配置，环境变量优先级更高。base_path 是 chatgpt_register.py 的目录。"""
    config = {
        "total_accounts": 3,
        # freemail worker settings (services/freemail.py)
        "freemail_worker_domain": "",
        "freemail_token": "",
        "proxy": "",
        "output_file": "registered_accounts.txt",
        "enable_oauth": True,
        "oauth_required": True,
        "oauth_issuer": "https://auth.openai.com",
        "oauth_client_id": "app_EMoamEEZ73f0CkXaXp7hrann",
        "oauth_redirect_uri": "http://localhost:1455/auth/callback",
        "ak_file": "ak.txt",
        "rk_file": "rk.txt",
        "token_json_dir": "codex_tokens",
        "upload_api_url": "",
        "upload_api_token": "",
        # freemail worker settings (services/freemail.py)
        "freemail_worker_domain": "",
        "freemail_token": "",
    }

    config_path = os.path.join(base_path, "config.json")
    if os.path.exists(config_path):
        try:
            with open(config_path, "r", encoding="utf-8") as f:
                file_config = json.load(f)
                config.update(file_config)
        except Exception as e:
            print(f"⚠️ 加载 config.json 失败: {e}")

    # 环境变量优先级更高
    config["proxy"] = os.environ.get("PROXY", config["proxy"])
    config["total_accounts"] = int(os.environ.get("TOTAL_ACCOUNTS", config["total_accounts"]))
    config["enable_oauth"] = os.environ.get("ENABLE_OAUTH", config["enable_oauth"]) 
    config["oauth_required"] = os.environ.get("OAUTH_REQUIRED", config["oauth_required"]) 
    config["oauth_issuer"] = os.environ.get("OAUTH_ISSUER", config["oauth_issuer"]) 
    config["oauth_client_id"] = os.environ.get("OAUTH_CLIENT_ID", config["oauth_client_id"]) 
    config["oauth_redirect_uri"] = os.environ.get("OAUTH_REDIRECT_URI", config["oauth_redirect_uri"]) 
    config["ak_file"] = os.environ.get("AK_FILE", config["ak_file"]) 
    config["rk_file"] = os.environ.get("RK_FILE", config["rk_file"]) 
    config["token_json_dir"] = os.environ.get("TOKEN_JSON_DIR", config["token_json_dir"]) 
    config["upload_api_url"] = os.environ.get("UPLOAD_API_URL", config["upload_api_url"]) 
    config["upload_api_token"] = os.environ.get("UPLOAD_API_TOKEN", config["upload_api_token"]) 
    # freemail env overrides
    config["freemail_worker_domain"] = os.environ.get("FREEMAIL_WORKER_DOMAIN", config.get("freemail_worker_domain", ""))
    config["freemail_token"] = os.environ.get("FREEMAIL_TOKEN", config.get("freemail_token", ""))

    return config


def as_bool(value):
    if isinstance(value, bool):
        return value
    if value is None:
        return False
    return str(value).strip().lower() in {"1", "true", "yes", "y", "on"}
