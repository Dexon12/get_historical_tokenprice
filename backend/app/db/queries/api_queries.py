from backend.app.db.queries.base_queries import BaseDAO
from backend.app.db.models.price_history import PriceHistory

class PriceHistory(BaseDAO):
    
    model = PriceHistory

