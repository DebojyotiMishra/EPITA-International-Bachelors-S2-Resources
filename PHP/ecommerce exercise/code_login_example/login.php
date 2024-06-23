<html>
    <head></head>
    <body>
        <?php 
        if(isset($_GET['Err_n']) && $_GET['Err_n'] == 1) {
            echo 'Please check your password';
        }
        ?>
        <form method="post" action="login_action.php">
            Login <input type="text" name="login">
            <br>
            Password <input type="password" name="pwd">
            <br>
            <input type="submit" value="Connect">
        </form>
    </body>
</html>