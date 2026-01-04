from typing import Dict, List, Any
from schemas.campaign import CampaignDetailsResponse

def normalize_campaign_details(
    data: CampaignDetailsResponse
) -> List[Dict[str, Any]]:

    rows: List[Dict[str, Any]] = []

    for channel, details in data.channels.items():
        members = details.members or {}
        attention_levels = details.attention_levels or {}

        # -----------------------------
        # Construir mapa usuario → niveles
        # -----------------------------
        user_levels: Dict[str, List[str]] = {}

        # SOLO si AttentionLevels es dict (caso real con niveles)
        if isinstance(attention_levels, dict):
            levels_iter = attention_levels.values()
        else:
            levels_iter = []

        for level in levels_iter:
            level_name = level.get("name", "SIN NIVEL")
            users = level.get("users", {})

            if not isinstance(users, dict):
                continue

            for user_id in users.keys():
                user_levels.setdefault(user_id, []).append(level_name)

        # -----------------------------
        # Recorrer TODOS los miembros
        # -----------------------------
        if not isinstance(members, dict):
            continue

        for user_id in members.keys():
            username = user_id.split("@")[0]
            
                # 🔍 LOG CLAVE
            print(
                f"[DEBUG MATCH] raw_user={user_id} | username={username} | levels{user_levels.get(username)}")
            
            levels = user_levels.get(username)

            if levels:
                for lvl in levels:
                    rows.append({
                        "brand": data.brand,
                        "channel": channel,
                        "campaign": data.campaign_name,
                        "user": user_id,
                        "attention_level": lvl
                    })
            else:
                rows.append({
                    "brand": data.brand,
                    "channel": channel,
                    "campaign": data.campaign_name,
                    "user": user_id,
                    "attention_level": "SIN NIVEL"
                })

    return rows
