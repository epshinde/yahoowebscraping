<!DOCTYPE html>
<html>
<body>
<table border='1'>
<tr> <th><a href="index.php?sort=index">Index</a></th> <th><a href="index.php?sort=symbol">Symbol</a></th> <th><a href="index.php?sort=name">Name</a></th><th><a href="index.php?sort=price">Price (Intraday)</a></th><th><a href="index.php?sort=change">Change</a></th> <th><a href="index.php?sort=volume">Volume</a></th></tr>
<?php
# echo "test";
require 'vendor/autoload.php';
$client = new MongoDB\Client();
$db = $client->yahoofinance;
$collection = $db->stocks;
$sortby = $_GET['sort'] ?? 'index';
$records = $collection->find([], ['sort' => [$sortby => 1]]);
#$secondrecords = $collection->find([], ['sort' => [$_GET['sort'] => 1]]);
foreach($records as $record) {
	echo "<tr> <td>" . $record["index"] . "</td> <td>" . $record["symbol"] . "</td> <td>" . $record["name"] . "</td> <td>" . $record["price"] . "</td> <td>" . $record["change"] . "</td> <td>" . $record["volume"] . $record["volumeunit"] . "</td> </tr>";
}
?>
</table>
</body>
</html>
