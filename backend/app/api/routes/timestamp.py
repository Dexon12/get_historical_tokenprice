from datetime import datetime
from typing import Any, Optional

from fastapi import APIRouter, HTTPException, Query

from backend.app.logic.price_by_timestamp import ChainlinkGetPrice
from backend.extra.network_slug import NetworkSlug

router = APIRouter(prefix="", tags=["timestamp"])


@router.get("/timestamp")
async def get_token_price_by_timestamp(
    timestamp: datetime = Query(
        description="Timestamp in the format 'YYYY-MM-DD HH:MM:SS'",
        example="2023-01-01 12:00:00",
    ),
    end_timestamp: Optional[datetime] = Query(
        default=None,
        description="End timestamp in the format 'YYYY-MM-DD HH:MM:SS'",
    ),
    network: NetworkSlug = Query(description="In what network do you want to check the price?"),
    token_tiker: str = Query(description="Which token price do you want to get?"),
    second_token_tiker: str = Query(description="In what token do you want to see that token?")
) -> Any:
    try:
        token_pair = f"{token_tiker}-{second_token_tiker}"

        unix_timestamp = int(timestamp.timestamp())
        if end_timestamp:
            unix_end_timestamp = int(end_timestamp.timestamp())
            
        if not end_timestamp:
            end_timestamp = timestamp
            unix_end_timestamp = unix_timestamp

        chainlink_get_price = ChainlinkGetPrice(
                    network=network, token_pair=token_pair,
                    timestamp=unix_timestamp, end_timestamp=unix_end_timestamp
                )

        result = await chainlink_get_price.get_price_by_timestamp()
        
        return {
            "timestamp": timestamp.isoformat(), 
            "end_timestamp": end_timestamp.isoformat() if end_timestamp else None,
            "unix_timestamp": unix_timestamp, 
            "price": result, 
            "token pair": token_pair
        }
    
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid timestamp format. Use 'YYYY-MM-DD HH:MM:SS'")
    