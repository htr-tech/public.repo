/*

Go Practise

Bitwise Shift/Unshift characters of a list.

*/

package main

import (
	"fmt"
	"strings"
	"unicode"
)

var blackList = []string{
	"gdb", "burpsuite", "charles", "dumpcap", "fiddler", "httpsmon", "httpwatchstudio", "mitmdump", "mitmweb",
	"networkminer", "rpcapd", "smsniff", "tshark", "windump", "wireshark", "wsockexpert", "ghidra", "radare2",
	"x32dbg", "x64dbg", "windbg", "disassembly", "scylla", "cutter", "importrec", "httpdebugger", "immunity",
}

func shiftCharacters(s string, shift int) string {
	shifted := make([]rune, len(s))
	for i, char := range s {
		if unicode.IsLower(char) {
			shifted[i] = (char-'a'+rune(shift))%26 + 'a'
		} else {
			shifted[i] = char
		}
	}
	return string(shifted)
}

func shiftList(list []string, shift int) []string {
	shifted := make([]string, len(list))
	for i, item := range list {
		shifted[i] = shiftCharacters(item, shift)
	}
	return shifted
}

func unshiftCharacters(s string, shift int) string {
	unshifted := make([]rune, len(s))
	for i, char := range s {
		if unicode.IsLower(char) {
			unshifted[i] = (char-'a'-rune(shift)+26)%26 + 'a'
		} else {
			unshifted[i] = char
		}
	}
	return string(unshifted)
}

func unshiftList(list []string, shift int) []string {
	unshifted := make([]string, len(list))
	for i, item := range list {
		unshifted[i] = unshiftCharacters(item, shift)
	}
	return unshifted
}

func main() {
	fmt.Println("=== Shifted ===")
	shiftedBlackList := shiftList(blackList, 8)
	fmt.Printf("var encodedList = []string{\n\"%s\",\n}\n\n", strings.Join(shiftedBlackList, "\", \""))

	fmt.Println("=== Unshifted ===")
	unshiftedBlackList := unshiftList(shiftedBlackList, 8)
	fmt.Printf("var decodedList = []string{\n\"%s\",\n}\n\n", strings.Join(unshiftedBlackList, "\", \""))

}
