"""
╔══════════════════╗
              TEAMDEV
╚══════════════════╝

[ PROJECT   ]  TeamDev AIO (All-In-One Downloader)
[ DEVELOPER ]  @MR_ARMAN_08

────────────────────

[ SUPPORT   ]  https://t.me/Team_X_Og
[ UPDATES   ]  https://t.me/TeamDevXBots
[ ABOUT US  ]  https://TeamDev.sbs

────────────────────

[ DONATE    ]  https://Pay.TeamDev.sbs

────────────────────
      FAST • POWERFUL • ALL-IN-ONE
      
"""

from fastapi import Header, Query, HTTPException, Request
from datetime import datetime
from app.core.database import get_db

async def require_api_key(
    request: Request,
    x_api_key: str = Header(None, alias="X-API-Key"),
    api: str = Query(None),
    api_key: str = Query(None),
):
    db = get_db()
    key = x_api_key or api or api_key

    if db and key:
        record = await db.api_keys.find_one({"key": key})
        if record and record.get("enabled", True):
            expiry = record.get("expires_at")
            if not expiry or datetime.utcnow() <= expiry:
                await db.api_keys.update_one(
                    {"key": key},
                    {"$inc": {"usage_count": 1}, "$set": {"last_used": datetime.utcnow()}}
                )
                return record

    return {"key": None, "owner": "anonymous", "enabled": True, "usage_count": 0}
