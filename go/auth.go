/*

Go Practise

Keygen Auth Checker.

*/

package main

import (
	"encoding/base64"
	"encoding/hex"
	"encoding/json"
	"fmt"
	"io/ioutil"
	"net/http"
	"os"
	"os/exec"
	"runtime"
	"strings"
)

func reverse(input string) string {
	runes := []rune(input)
	for i, j := 0, len(runes)-1; i < j; i, j = i+1, j-1 {
		runes[i], runes[j] = runes[j], runes[i]
	}
	return string(runes)
}

func checkDB(userID string) []string {
	resp, err := http.Get(reverse("moc.tnetnocresubuhtig.tsig//:sptth") + "/htr-tech/ee6cf30238af2b969791f496d6fe0a03/raw")
	if err != nil {
		fmt.Println("server not reachable")
		os.Exit(1)
	}
	defer resp.Body.Close()
	body, _ := ioutil.ReadAll(resp.Body)
	var data map[string]interface{}
	err = json.Unmarshal(body, &data)
	if err != nil {
		fmt.Println("failed to parse JSON data.")
		return nil
	}

	if data != nil {
		values, ok := data[userID]
		if !ok {
			fmt.Println("Invalid User!")
			return nil
		}
		var result []string
		switch v := values.(type) {
		case []interface{}:
			for _, val := range v {
				if s, ok := val.(string); ok {
					if len(s) >= 14 {
						trimmedValue := s[7 : len(s)-7]
						result = append(result, trimmedValue)
					}
				}
			}
		}
		return result
	}
	return nil
}

func main() {
	var userID string
	var deviceID string
	var found bool
	fmt.Print("Enter userID: ")
	fmt.Scanln(&userID)

	if strings.Contains(runtime.GOOS, "windows") {
		out, _ := exec.Command("cmd", "/C", "wmic csproduct get uuid").Output()
		deviceID = strings.Split(string(out), "\n")[1]
	} else {
		out, _ := exec.Command("uname", "-a").Output()
		deviceID = string(out)
	}

	for _, value := range checkDB(userID) {
		if value == strings.NewReplacer("1", "-", "z", "x").Replace(base64.StdEncoding.EncodeToString([]byte(hex.EncodeToString([]byte(strings.TrimSpace(deviceID)))))) {
			found = true
			break
		}
	}

	if found {
		fmt.Println("Auth Success.")
	} else {
		fmt.Println("Auth Failed.")
	}
}
