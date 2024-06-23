<?php
session_start();
$login = $_POST['login'];
$pwd = $_POST['pwd'];

if($login=='toto' && $pwd=='tata'){
    $_SESSION['login']=$login;
    header("location: my_profile.php");
}else{
    header('location: login.php?Err_n=1');
}