<?php

// Just another dumb base64 obfuscation (2019)

function utf8_($in)
{
    $val_ = '';
    foreach (str_split($in) as $i) $val_ .= sprintf('\\x%x', ord($i));
    return sprintf('%s', $val_);
}

$func_main = "
function _____(\$__I,\$__l)
{
	\$__l = preg_replace('/\n$/','',\$__l);
    if (sha1(\$__l) == \$__I) {
        eval(\"?>\".gzuncompress(gzinflate(base64_decode(\$__l))));
    } else { 
        echo '[!] Code has been modified [!]';
        exit;
    }
}";

$en_func_main = base64_encode($func_main);
if (substr($en_func_main, -2) == "==") {
    $en_func_main = substr($en_func_main, 0, -2);
}
$en_func_main = strtr($en_func_main, 'asuio23456', '65432asuio');
$len_func_main = strlen($en_func_main);

if (!empty($argv[1])) {
    $script = $argv[1];
} else {
    $script = readline('File Name : ');
}

$openfile = @fopen($script, "r") or die("Unable to open file!");
$data = fread($openfile, filesize($script));
$encoded_data = base64_encode(gzdeflate(gzcompress($data, 9)));

$func_one = "
\$___ = str_replace('__FILE__', \"'\" . \$__ . \"'\", file(\$__));
function S__(\$i,\$l=0,\$k=40){
    global \$__;
    \$r = count(\$i) - 1;
    while (1 == 1) {
        if (empty(trim(\$i[\$r]))) {
            \$r = \$r - 1;
        } else {
            break;
        }
    }
    \$x = explode(\"__halt_compiler();\",\$i[\$r])[1];
    if (\$l == 1) {
        \$val_ = substr(\$x,$len_func_main,\$k);
    } elseif (\$l == 2) {
        \$val_ = explode(substr(\$x,$len_func_main,\$k),\$x)[1];
    } else {
        \$val_ = substr(\$x,0,$len_func_main);
        \$val_ = str_replace(\"'\" . \$__ . \"'\", '__FILE__', strtr(\$val_, '65432asuio', 'asuio23456')).'==';
    }
    return \$val_;
}";

$en_func_one = "eval(base64_decode(\"" . utf8_(base64_encode($func_one)) . "\"));";

$output = "<?php /* OBFUSCATED BY CATZ ?? */ error_reporting(0);\$__ = __FILE__;" . $en_func_one;
$output .= "eval(base64_decode(S__(\$___)));";
$output .= "eval(_____(S__(\$___,1),S__(\$___,2)));__halt_compiler();";
$output .= $en_func_main . sha1($encoded_data) . $encoded_data;

// echo $output;
$out = fopen('en_' . $script, "w") or die("Unable to open file!");
fwrite($out, $output);
fclose($out);
