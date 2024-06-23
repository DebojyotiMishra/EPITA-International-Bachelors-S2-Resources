from typing import Dict, List
from abc import ABC, abstractmethod

class Product(ABC):
    def __init__(self, name: str):
        self.name = name

    @abstractmethod
    def getPrice(self) -> float:
        pass

    @abstractmethod
    def getItems(self) -> Dict['SimpleProduct', int]:
        pass


class SimpleProduct(Product):
    def __init__(self, name: str, price: float):
        super().__init__(name)
        self.price = price

    def getPrice(self) -> float:
        return self.price

    def getItems(self) -> Dict['SimpleProduct', int]:
        return {self: 1}
    
    def __hash__(self):
        return hash(self.name)

    def __eq__(self, other):
        return self.name == other.name


class Bundle(Product):
    def __init__(self, name: str, products: Dict[Product, int]):
        super().__init__(name)
        self.products = products

    def getPrice(self) -> float:
        return sum(product.getPrice() * quantity for product, quantity in self.products.items())

    def getItems(self) -> Dict[SimpleProduct, int]:
        items: Dict[SimpleProduct, int] = {}
        for product, quantity in self.products.items():
            for simple_product, count in product.getItems().items():
                if simple_product in items:
                    items[simple_product] += count * quantity
                else:
                    items[simple_product] = count * quantity
        return items

class Cart:
    def __init__(self):
        self.products: Dict[Product, int] = {}

    def addProduct(self, product: Product, quantity: int):
        if product in self.products:
            self.products[product] += quantity
        else:
            self.products[product] = quantity

    def removeProduct(self, product: Product, quantity: int):
        if product in self.products:
            if self.products[product] <= quantity:
                del self.products[product]
            else:
                self.products[product] -= quantity

    def getPrice(self) -> float:
        return sum(product.getPrice() * quantity for product, quantity in self.products.items())

    def getItems(self) -> Dict[SimpleProduct, int]:
        items: Dict[SimpleProduct, int] = {}
        for product, quantity in self.products.items():
            for simple_product, count in product.getItems().items():
                if simple_product in items:
                    items[simple_product] += count * quantity
                else:
                    items[simple_product] = count * quantity
        return items
    # the code above gets the items in the cart and their quantities by using the getItems method of the Product class


if __name__ == '__main__':
    p1 = SimpleProduct("METOD Base cabinet frame, white", 32.00)
    p2 = SimpleProduct("METOD door white 80x37 cm", 144.00)
    p3 = SimpleProduct("MITTLED LED kitchen worktop lighting strip", 17.00)
    p4 = SimpleProduct("STENSUND sink", 30.00)
    p5 = SimpleProduct("STENSUND tap", 50.00)
    b1 = Bundle("Kitchen base set", {p1: 3, p2: 3, p3: 1})
    b2 = Bundle("Kitchen tap & sink set", {p4: 1, p5: 2})
    b3 = Bundle("Kitchen set", {b1: 1, b2: 1})
    cart = Cart()
    cart.addProduct(p1, 2)
    cart.addProduct(b1, 1)
    cart.addProduct(b2, 1)
    cart.addProduct(b3, 1)
    print('The total price of the cart is:', cart.getPrice())
    
    items = cart.getItems()
    print('The items in the cart are:')
    for product, count in items.items():
        print(f'{count} × {product.name}')
        
    # ------------------- OUTPUT -------------------
    # The total price of the cart is: 1414.0
    # The items in the cart are:
    # 8 × METOD Base cabinet frame, white
    # 6 × METOD door white 80x37 cm
    # 2 × MITTLED LED kitchen worktop lighting strip
    # 2 × STENSUND sink
    # 4 × STENSUND tap