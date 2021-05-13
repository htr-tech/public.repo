#!/bin/bash

# Encode Bash Script with Base64

obfuscate() {
printf "#!/bin/bash
mew=\$(mktemp)
base64 -d  > \${mew} << hulu
$(base64 $1)
hulu
source \${mew}
rm -rf \${mew}" > $2
}

if [[ -e $1 && ! $2 == "" ]]; then
    obfuscate $1 $2
else
    echo -e "Usage: "$0" <input> <output>"
fi
