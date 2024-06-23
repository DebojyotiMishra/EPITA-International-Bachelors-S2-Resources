<?php
session_start();
if(!isset($_SESSION['login'])){
    header('Location: login.php');
}

echo 'Hello '.$_SESSION['login'];