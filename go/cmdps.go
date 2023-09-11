/*

Go Practise

Prints Windows PID, PPID, Executable Name, Command Line (using wmic)

*/

package main

import (
	"fmt"
	"log"
	"os/exec"
	"strconv"
	"strings"
)

type Process interface {
	Pid() int
	PPid() int
	Executable() string
	CommandLine() string
}

type WindowsProcess struct {
	pid         int
	ppid        int
	exe         string
	commandLine string
}

func (p *WindowsProcess) Pid() int {
	return p.pid
}

func (p *WindowsProcess) PPid() int {
	return p.ppid
}

func (p *WindowsProcess) Executable() string {
	return p.exe
}

func (p *WindowsProcess) CommandLine() string {
	return p.commandLine
}

func processes() ([]Process, error) {
	out, err := exec.Command("wmic", "process", "get", "ProcessId,ParentProcessId,ExecutablePath,CommandLine", "/format:list").Output()
	if err != nil {
		return nil, err
	}

	lines := strings.Split(string(out), "\r\r\n\r\r\n")

	var processes []Process
	for _, line := range lines {
		fields := strings.Split(line, "\r\r\n")
		process := &WindowsProcess{}

		for _, field := range fields {
			keyValue := strings.SplitN(field, "=", 2)
			if len(keyValue) == 2 {
				key := keyValue[0]
				value := keyValue[1]

				switch key {
				case "ProcessId":
					process.pid, _ = strconv.Atoi(value)
				case "ParentProcessId":
					process.ppid, _ = strconv.Atoi(value)
				case "ExecutablePath":
					process.exe = value
				case "CommandLine":
					process.commandLine = value
				}
			}
		}

		processes = append(processes, process)
	}

	return processes, nil
}

func main() {
	procs, err := processes()
	if err != nil {
		log.Fatal(err)
	}

	for _, proc := range procs {
		fmt.Printf("PID: %d, PPID: %d, Executable: %s, Command Line: %s\n", proc.Pid(), proc.PPid(), proc.Executable(), proc.CommandLine())
	}
}
