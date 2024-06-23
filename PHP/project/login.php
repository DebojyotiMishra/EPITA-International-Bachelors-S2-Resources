<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="stylesheet" href="styles/normalize.css">
    <link rel="stylesheet" href="styles/login.css">
    <title>EpiBook | Login</title>
</head>

<body>
    <nav>
        <a href=""><img src="images/EPITA-white.svg" alt="" class="nav-logo"></a>
        <ul>
            <li><a href="login.php" class="nav-link">Login</a></li>
            <li><a href="signup.php" class="nav-link">Sign up</a></li>
        </ul>
    </nav>

    <!-- Login Form -->
    <form class="form">
        <p class="login-title">Login to Epibook</p>
        <p class="login-message">Nice to see you again!</p>
        <input type="text" name="email" id="email" placeholder="Email" class="input">
        <input type="password" name="password" id="password" placeholder="Password" class="input">
        <br>
        <button type="submit" class="button submit-button">Login</button>
        <p class="login-message">Don't have an account? <a href="signup.php" class="login-link">Sign up</a></p>
    </form>
</body>

</html>