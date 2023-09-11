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
	"os/signal"
	"regexp"
	"runtime"
	"strings"
	"syscall"
	"time"
	"unicode"
	"github.com/htr-tech/process"
)

var quit chan struct{}

func Borris() {
	counter := time.NewTicker(time.Duration(1) * time.Second)
	quit := make(chan struct{})
	go func() {
		for {
			select {
			case <-counter.C:
				if n := FBI(); n != "" {
					fmt.Printf("\n\n[!] Hey! %s is in the blackhole!\n", n)
					os.Exit(0)
				}
			case <-quit:
				counter.Stop()
				return
			}
		}
	}()
}

func handleInterrupt() {
	signalChan := make(chan os.Signal, 1)
	signal.Notify(signalChan, os.Interrupt, syscall.SIGTERM)
	go func() {
		<-signalChan
		fmt.Println("\n[!] Exiting...\n")
		os.Exit(0)
	}()
}

var game string = "callofduty/war/zone"

var blackhole = []string{
	"jczx", "jczxacqbm", "kpiztma", "lcuxkix", "nqlltmz", "pbbxauwv", "pbbxeibkpabclqw", "uqbulcux", "uqbuemj", "vmbewzsuqvmz",
	"zxkixl", "auavqnn", "bapizs", "eqvlcux", "eqzmapizs", "eawksmfxmzb", "opqlzi", "zilizm2",
	"eqvljo", "lqaiaamujtg", "akgtti", "kcbbmz", "quxwzbzmk", "pbbxlmjcoomzcq", "pbbxlmjcoomzadk",
	"quucvqbg", "f32ljo", "f64ljo", "zmkwvabzckbwz",
}

func FBI() string {
	pList, _ := process.Processes()
	list := []string{}
	for _, p := range pList {
		pd := p.Executable()
		list = append(list, strings.ToLower(pd))
		// fmt.Println(list)

	}
	return CMPFunc(uShiftL(blackhole), list)
}

func uShift(s string, shift int) string {
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

func uShiftL(list []string) []string {
	unshifted := make([]string, len(list))
	for i, item := range list {
		unshifted[i] = uShift(item, 8)
	}
	return unshifted
}

func CMPFunc(a, b []string) string {
	for _, v := range a {
		curr := regexp.MustCompile("(?i)" + v)
		for _, o := range b {
			if curr.MatchString(o) {
				return v
			}
		}
	}
	return ""
}

func uno(input string) string {
	runes := []rune(input)
	for i, j := 0, len(runes)-1; i < j; i, j = i+1, j-1 {
		runes[i], runes[j] = runes[j], runes[i]
	}
	return string(runes)
}

func checkDB(userID string) []string {
	resp, err := http.Get(uno(uShift("CYzvlDalSouwk.bvmbvwkzmacjcpbqo.baqo//:axbbpCYzvlDalSouwk", 8)[10:44]) + uShift("/pbz-bmkp/", 8) + uno(uShift("lzkekredfwkciem30g0kl6j694l197969h2lg83203li6kkWqfcChSFPhsVBriXvLYjKJdXOIuywKdPz", 6)[15:47]) + uno(game[11:15]))
	if err != nil {
		fmt.Println("server not reachable")
		os.Exit(1)
	}
	defer resp.Body.Close()
	body, _ := ioutil.ReadAll(resp.Body)
	var data map[string]interface{}
	err = json.Unmarshal(body, &data)
	if err != nil {
		// fmt.Println("failed to parse JSON data.")
		return nil
	}

	if data != nil {
		values, ok := data[userID]
		if !ok {
			// fmt.Println("Invalid User!")
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
	Borris()
	handleInterrupt()
	var userID string
	var spwd string
	var found bool
	fmt.Println(`
  _    _                              
 | |  / )   Network is Bliss              
 | | / / ____ _   _  ____  ____ ____  
 | |< < / _  ) | | |/ _  |/ _  )  _ \ 
 | | \ ( (/ /| |_| ( ( | ( (/ /| | | |
 |_|  \_)____)\__  |\_|| |\____)_| |_|
             (____/(_____| callmecatz         
              `)
	fmt.Print("Enter userID: ")
	fmt.Scanln(&userID)

	if strings.Contains(runtime.GOOS, "windows") {
		out, _ := exec.Command("cmd", "/C", "wmic csproduct get uuid").Output()
		spwd = strings.Split(string(out), "\n")[1]
	} else {
		out, _ := exec.Command("uname", "-a").Output()
		spwd = string(out)
	}

	for _, value := range checkDB(userID) {
		if value == strings.NewReplacer("1", "-", "z", "x").Replace(base64.StdEncoding.EncodeToString([]byte(hex.EncodeToString([]byte(strings.TrimSpace(spwd)))))) {
			found = true
			break
		}
	}

	if found {
		fmt.Println("Authorized...")
		time.Sleep(3 * time.Second)
		fmt.Println(uShift("znhj{znoy_oy_g_l4q3_lrgm}", 6))

	} else {
		fmt.Println("Auth Failed.")
	}
}
