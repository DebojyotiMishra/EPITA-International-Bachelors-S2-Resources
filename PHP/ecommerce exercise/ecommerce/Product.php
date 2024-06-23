<?php
require_once 'Connection.php';
class Product
{
    private int $id;
    private string $item_code;
    private string $item_des;
    private float $unit_price;
    private int $discount;

    public function __construct(string $code, string $desig, float $price, int $discount=0)
    {
        //Write the code for the constructor.
    }
    
    public function addProduct()
    {
        $query = "insert into product(item_code, item_des, unit_price, discount)
                values('------------', '------------', ------------, -------------)";
        try {
            $con = -----------------------;
            $con->exec(-------------);
        } catch (\Throwable $th) {
            echo $th->getMessage();
        }
    }

    public static function getAllProducts()
    {
        $query = "select * from product";
        $con = -------------------------;
        $stmt = $con->prepare(---------);
        $stmt->execute();
        return -------------------;
    }
}