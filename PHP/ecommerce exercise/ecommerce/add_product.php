<html>

<head></head>

<body>
    <form method="post" action="add_product_action.php">
        <fieldset>
            <legend>Add product</legend>
            <label style="display: inline-block; width: 130px; ">Item code</label>
            <input type="text" name="item_code">
            <br>
            <label style="display: inline-block; width: 130px; ">Item description</label>
            <input type="text" name="item_des">
            <br>
            <label style="display: inline-block; width: 130px; ">Unit price</label>
            <input type="text" name="unit_price">
            <br>
            <label style="display: inline-block; width: 130px; ">Discount</label>
            <input type="text" name="discount">
            <br>
            <input type="submit" value="Validate">
        </fieldset>
    </form>

</body>

</html>