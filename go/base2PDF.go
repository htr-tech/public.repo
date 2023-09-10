// This script reads a file containing Base64 encoded PNG images,
// decodes the images, and saves them as individual PNG files in
// the same directory as the input file. Each image is saved
// with a file name corresponding to its line number in the input file.

package main

import (
	"bufio"
	"encoding/base64"
	"fmt"
	"image/png"
	"io"
	"os"
	"path/filepath"
	"strings"
)

func main() {
	var inputFilePath string
	if len(os.Args) > 1 {
		inputFilePath = os.Args[1]
	} else {
		fmt.Print("Input file: ")
		fmt.Scanln(&inputFilePath)
	}

	file, err := os.Open(inputFilePath)
	if err != nil {
		fmt.Println("Failed to open the input file")
		os.Exit(1)
	}
	defer file.Close()

	outputDir := strings.TrimSuffix(inputFilePath, filepath.Ext(inputFilePath))
	os.MkdirAll(outputDir, os.ModePerm)

	reader := bufio.NewReader(file)
	lineCounter := 0

	for {
		line, err := reader.ReadString('\n')
		lineCounter++
		line = strings.TrimSpace(line)

		if len(line) > 0 {
			base64CheckStr := "data:image/png;base64,"

			if len(line) > len(base64CheckStr) && line[:len(base64CheckStr)] == base64CheckStr {
				line = strings.TrimSpace(line[len(base64CheckStr):])

				imageData, _ := base64.StdEncoding.DecodeString(line)
				imageReader := strings.NewReader(string(imageData))
				pngImage, _ := png.Decode(imageReader)
				imagePath := filepath.Join(outputDir, fmt.Sprintf("%d.png", lineCounter))
				imageFile, _ := os.Create(imagePath)
				defer imageFile.Close()

				png.Encode(imageFile, pngImage)
				// fmt.Printf("Saved PNG image for line %d\n", lineCounter)
			} else {
				fmt.Printf("Invalid PNG Base64 data on line %d\n", lineCounter)
			}
		}

		if err == io.EOF {
			break
		}
	}

	fmt.Println("Images saved successfully.")
}
