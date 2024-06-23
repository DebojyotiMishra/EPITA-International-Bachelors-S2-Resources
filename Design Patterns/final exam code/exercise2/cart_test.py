import unittest
from shopping_cart import Cart, SimpleProduct, Bundle

class TestCartSystem(unittest.TestCase):
    def setUp(self):
        self.p1 = SimpleProduct("METOD Base cabinet frame, white", 32.00)
        self.p2 = SimpleProduct("METOD door white 80x37 cm", 144.00)
        self.p3 = SimpleProduct("MITTLED LED kitchen worktop lighting strip", 17.00)
        self.p4 = SimpleProduct("STENSUND sink", 30.00)
        self.p5 = SimpleProduct("STENSUND tap", 50.00)
        self.b1 = Bundle("Kitchen base set", {self.p1: 3, self.p2: 3, self.p3: 1})
        self.b2 = Bundle("Kitchen tap & sink set", {self.p4: 1, self.p5: 2})
        self.b3 = Bundle("Kitchen set", {self.b1: 1, self.b2: 1})
        self.cart = Cart()

    def test_add_product(self):
        self.cart.addProduct(self.p1, 2)
        self.cart.addProduct(self.b1, 1)
        self.cart.addProduct(self.b2, 1)
        self.cart.addProduct(self.b3, 1)
        self.assertEqual(self.cart.getPrice(), 1414.0)
        

    def test_get_items(self):
        self.cart.addProduct(self.b3, 1)
        items = self.cart.getItems()
        expected_items = {
            self.p1: 3,
            self.p2: 3,
            self.p3: 1,
            self.p4: 1,
            self.p5: 2
        }
        for product, count in expected_items.items():
            self.assertEqual(items[product], count)

    def test_remove_product(self):
        self.cart.addProduct(self.b3, 1)
        self.cart.removeProduct(self.b3, 1)
        self.assertEqual(self.cart.getPrice(), 0.0)
        self.assertEqual(self.cart.getItems(), {})
    
    def test_remove_product_quantity(self):
        self.cart.addProduct(self.b3, 1)
        self.cart.removeProduct(self.b3, 1)
        self.assertEqual(self.cart.getPrice(), 0.0)
        self.assertEqual(self.cart.getItems(), {})
        
        self.cart.addProduct(self.b3, 1)
        self.cart.removeProduct(self.b3, 1)
        self.assertEqual(self.cart.getPrice(), 0.0)    

if __name__ == "__main__":
    unittest.main()
