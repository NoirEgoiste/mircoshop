from core.models import Base


class ProductBase(Base):
    name: str
    description: str
    price: int


class ProductCreate(Base):
    pass


class Product(ProductBase):
    id: int
