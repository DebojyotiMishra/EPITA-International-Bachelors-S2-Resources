<?php

class Connection
{
    const USER='root';
    const PASSWORD='';
    const HOST='localhost';
    const DBNAME = 'ecommerce';

    public static function getConnection():PDO {
        try {
            $dsn = 'mysql:dbname='.s-----------.";host=".------------;
            return new PDO($dsn, ------------, ---------------);

        } catch (PDOException $ex) {
            echo $ex->getMessage();
        }
        
    }
}

