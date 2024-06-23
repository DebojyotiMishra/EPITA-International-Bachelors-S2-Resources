# IKEA Shopping Cart
## Design Pattern
The Composite Design Pattern was chosen for this because it allows us to treat individual products and bundles of products the same way. In this pattern, ```Product``` is the abstract base class (component), ```SimpleProduct``` is the leaf class, and ```Bundle``` is the composite class.

## Implementation
### Classes and Methods
1. ```Product (Abstract Base Class)```: Represents a general product. It has the name attribute and abstract methods getPrice and getItems.
<br>
2. ```SimpleProduct (Inherits from Product)```: Represents a simple product with a price. It implements the getPrice and getItems methods.
<br>
3. ```Bundle (Inherits from Product)```: Represents a bundle of products. It has a products dictionary that stores the products and their quantities in the bundle. It implements the getPrice and getItems methods.
<br>
4. ```Cart```: Manages a collection of products. It allows adding and removing products, calculating the total price, and listing all items in the cart.

## ```Product``` (Abstract Base Class)
I defined the abstractmethods

## ```SimpleProduct``` (Inheriting from ```Product```)
1. ```getPrice```: returns the price of the object
2. ```getItems```: returns a dictionary with the product itself as the key and the quantity as the value

## ```Bundle``` (Inheriting from ```Product```)
1. ```getPrice```: I used ```sum``` in python to get the price of the bundle by summing the price of each product in the bundle.
2. ```getItems```: I get the items in a bundle by using a recursive function

## ```Cart```
1. ```addProduct```: If the product is already in the cart, I increment its quantity by 1
2. ```removeProduct```: If it exists in the cart and the quantity is 1, I delete it. Else, I decrement its quantity by 1
3. ```getItem```: gets the items in the cart and their quantities by using the getItems method of the Product class.

# Check to see if code works
The following code:
```bash
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
```

Gives the following Output:

```bash
The total price of the cart is: 1414.0
The items in the cart are:
8 × METOD Base cabinet frame, white
6 × METOD door white 80x37 cm
2 × MITTLED LED kitchen worktop lighting strip
2 × STENSUND sink
4 × STENSUND tap
```

Therefore it works
