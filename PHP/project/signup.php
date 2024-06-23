<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="stylesheet" href="styles/normalize.css">
    <link rel="stylesheet" href="styles/login.css">
    <title>EpiBook | Sign Up</title>
</head>

<body>
    <nav>
        <a href=""><img src="images/EPITA-white.svg" alt="" class="nav-logo"></a>
        <ul>
            <li><a href="login.php" class="nav-link">Login</a></li>
            <li><a href="register.php" class="nav-link">Sign up</a></li>
        </ul>
    </nav>

    <!-- Login Form -->
    <form class="form">
        <p class="login-title">Sign up for Epibook</p>
        <p class="login-message">Welcome to EPIbook!</p>
        <input type="text" name="first-name" id="first-name" placeholder="First Name" class="input">
        <input type="text" name="last-name" id="last-name" placeholder="Last Name" class="input">
        <br>
        <input type="text" name="email" id="email" placeholder="Email" class="input">
        <input type="password" name="password" id="password" placeholder="Password" class="input">
        <input type="password" name="confirm-password" id="confirm-password" placeholder="Confirm Password" class="input">
        <br>
        <button type="submit" class="button submit-button">Login</button>
        <p class="login-message">Already have an account? <a href="login.php" class="login-link">Log in</a></p>
    </form>
</body>

</html>