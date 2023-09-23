// Base__ Encoded String Decoder in Golang
// Practise
// Future Project? : Maybe (*OwO*)

package main

import (
	"bytes"
	"encoding/ascii85"
	"encoding/base32"
	"encoding/base64"
	"encoding/hex"
	"fmt"
	"math/big"
	"strings"
)

func Base16(char string) string {
	bytes, err := hex.DecodeString(char)
	if err != nil {
		return ""
	}
	return string(bytes)
}

func Base32(char string) string {
	bytes, err := base32.StdEncoding.DecodeString(char)
	if err != nil {
		return ""
	}
	return string(bytes)
}

func Base64(char string) string {
	bytes, err := base64.StdEncoding.DecodeString(char)
	if err != nil {
		return ""
	}
	return string(bytes)
}

func Base85(char string) string {
	output := make([]byte, ascii85.MaxEncodedLen(len(char)))
	x, _, err := ascii85.Decode(output, []byte(char), true)
	if err != nil {
		return ""
	}
	return string(output[:x])
}

// Base45 Mapping
var DICT45 = func() map[rune]int {
	dict := make(map[rune]int)
	for x, y := range "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ $%*+-./:" {
		dict[y] = x
	}
	return dict
}()

func Base45(char string) string {
	var res []int
	for i := 0; i < len(char); i += 3 {
		if len(char)-i >= 3 {
			val1, tes1 := DICT45[rune(char[i])]
			val2, tes2 := DICT45[rune(char[i+1])]
			val3, tes3 := DICT45[rune(char[i+2])]
			if !tes1 || !tes2 || !tes3 {
				return ""
			}
			x := val1 + val2*45 + val3*45*45
			res = append(res, x/256, x%256)
		} else {
			val1, k1 := DICT45[rune(char[i])]
			val2, k2 := DICT45[rune(char[i+1])]
			if !k1 || !k2 {
				return ""
			}
			res = append(res, val1+val2*45)
		}
	}
	out := new(bytes.Buffer)
	for _, v := range res {
		out.WriteRune(rune(v))
	}
	return out.String()
}

func baseDecode(input string, base int, mapp []byte) string {
	var result big.Int
	result.SetUint64(0)
	for _, r := range input {
		index := -1
		for i, b := range mapp {
			if b == byte(r) {
				index = i
				break
			}
		}
		if index == -1 {
			return ""
		}
		result.Mul(&result, big.NewInt(int64(base)))
		result.Add(&result, big.NewInt(int64(index)))
	}
	out := result.Bytes()
	return string(out)
}

func Base58(char string) string {
	var maps = []byte("123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz")
	return baseDecode(char, 58, maps)
}

func Base62(char string) string {
	var maps = []byte("0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz")
	return baseDecode(char, 62, maps)
}

var DICT91 = func() map[rune]int {
	dict := make(map[rune]int)
	for x, y := range "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789!#$%&()*+,./:;<=>?@[]^_`{|}~\"" {
		dict[y] = x
	}
	return dict
}()

func Base91(char string) string {
	v, b, n := -1, 0, 0
	out := []byte{}
	for _, x := range char {
		c, ok := DICT91[x]
		if !ok {
			continue
		}
		if v < 0 {
			v = c
		} else {
			v += c * 91
			b |= v << n
			if (v & 8191) > 88 {
				n += 13
			} else {
				n += 14
			}
			for n > 7 {
				out = append(out, byte(b&255))
				b >>= 8
				n -= 8
			}
			v = -1
		}
	}
	if v+1 != 0 {
		out = append(out, byte((b|v<<n)&255))
	}
	return string(out)
}

func Base100(char string) string {
	bytes := []byte(char)
	tmp := 0
	res := make([]byte, len(bytes)/4)
	for i, b := range bytes {
		if i%4 == 2 {
			tmp = ((int(b) - 143) * 64) % 256
		} else if i%4 == 3 {
			res[i/4] = byte((int(b) - 128 + tmp - 55) & 0xff)
		}
	}
	decode := strings.TrimRight(string(res), "\x00")
	return decode
}

// Test Case
func main() {
	fmt.Println("Base16 : " + Base16("48656c6c6f20576f726c64"))
	fmt.Println("Base32 : " + Base32("JBSWY3DPEBLW64TMMQ======"))
	fmt.Println("Base64 : " + Base64("SGVsbG8gV29ybGQ="))
	fmt.Println("Base85 : " + Base85("87cURD]i,\"Ebo7"))
	fmt.Println("Base45 : " + Base45("%69 VD82EI2B.KEA2"))
	fmt.Println("Base58 : " + Base58("JxF12TrwUP45BMd"))
	fmt.Println("Base62 : " + Base62("73XpUgyMwkGr29M"))
	fmt.Println("Base91 : " + Base91(">OwJh>Io0Tv!lE"))
	fmt.Println("Base100 : " + Base100("🐿👜👣👣👦🐗👎👦👩👣👛"))
}
