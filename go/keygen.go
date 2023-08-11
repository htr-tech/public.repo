/*

Go Practise

Generate unique key-pair for each device.

*/

package main

import (
	"crypto/rand"
	"encoding/base64"
	"encoding/hex"
	"fmt"
	"math/big"
	"os/exec"
	"runtime"
	"strings"
)

func randomString(n int) string {
	const letters = "abcdefghijklmnopqrstuvwxyz-_#*+!?(@"
	result := make([]byte, n)
	for i := range result {
		val, _ := rand.Int(rand.Reader, big.NewInt(int64(len(letters))))
		result[i] = letters[val.Int64()]
	}
	return string(result)
}

func main() {
	var deviceID string

	fmt.Println(`  _    _                              
 | |  / )                             
 | | / / ____ _   _  ____  ____ ____  
 | |< < / _  ) | | |/ _  |/ _  )  _ \ 
 | | \ ( (/ /| |_| ( ( | ( (/ /| | | |
 |_|  \_)____)\__  |\_|| |\____)_| |_|
             (____/(_____|                    
              `)

	if strings.Contains(runtime.GOOS, "windows") {
		out, _ := exec.Command("cmd", "/C", "wmic csproduct get uuid").Output()
		deviceID = strings.Split(string(out), "\n")[1]
	} else {
		out, _ := exec.Command("uname", "-a").Output()
		deviceID = string(out)
	}

	prefix := randomString(7)
	hexEncoded := hex.EncodeToString([]byte(strings.TrimSpace(deviceID)))
	base64Encoded := strings.NewReplacer("1", "-", "z", "x").Replace(base64.StdEncoding.EncodeToString([]byte(hexEncoded)))
	finalCode := prefix + base64Encoded + prefix

	fmt.Printf(" Send this key to Admin \n\n %s\n", finalCode)
	fmt.Scanln()
}
