<!DOCTYPE html>
<head>
<style>
body {background-color: black;color: red;}
textarea {background-color: black;color: red;}
</style>
</head>
<body>
<center><h1>Simple PHP Obfuscator</h1>
<form action="" method="POST">
<textarea rows="10" cols="100" name="payload" placeholder="Php Code"></textarea><br><br>
<input type="submit" name="enter" value="Submit" /><br>
</center>

<?php

// Easy to Decode It Though

/*
<?php 
$h4x0r = "eval("?>".gzuncompress(gzuncompress(gzinflate(gzinflate(gzinflate(base64_decode(strrev($n00b))))))));";
$n00b = "...........................................";
eval(htmlspecialchars_decode(urldecode(base64_decode($h4x0r))));
exit;?>
*/

if (isset($_POST['enter'])) {
$code = $_POST['payload'];
if (!empty($code)) {

$h1  = "eval('?>'.gzuncompress(gzinflate(base64_decode(strrev(\$H4X0R)))));";
$f1 = 'eval("?>".gzuncompress(gzuncompress(gzinflate(gzinflate(gzinflate(base64_decode(strrev($n00b))))))));';
$h2 = base64_encode(gzdeflate(str_rot13($h1)));
$f2 = base64_encode(urlencode(htmlspecialchars($f1)));
$h3 = strrev(base64_encode(gzdeflate(gzcompress($code,9))));
$h4 = "<?php /* ENCODED BY HAX0R T4HM1D */ \$t4hm1d = '".$h2."';\$H4X0R = '".$h3."';eval(str_rot13(gzinflate(base64_decode(\$t4hm1d))));?>";
$f3 = strrev(base64_encode(gzdeflate(gzdeflate(gzdeflate(gzcompress(gzcompress($h4)))))));
echo '<br><center><textarea rows="10" cols="100">
<?php /* Obfuscated by H4X0R T4HM1D */ $h4x0r = "'.$f2.'";$n00b = "'.$f3.'";eval(htmlspecialchars_decode(urldecode(base64_decode($h4x0r))));exit;?>
</textarea></center>';}}?>

</form>
</body>
</html>
