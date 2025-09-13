from app.domain.crypto.models.price import Price
from app.infrastructure.crypto.database.table_models import PriceTableModel


class DbPriceTranslator:
    def bulk_translate_to_table_model(
        self, domain_prices: list[Price]
    ) -> list[PriceTableModel]:
        return [
            self.translate_to_table_model(domain_price)
            for domain_price in domain_prices
        ]

    def translate_to_table_model(self, domain_price: Price) -> PriceTableModel:
        price_table_model = PriceTableModel(
            ticker_id=domain_price.ticker_id,
            price=domain_price.price,
            timestamp=domain_price.timestamp,
        )

        if domain_price.id is not None:
            price_table_model.id = domain_price.id

        return price_table_model
