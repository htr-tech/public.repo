// This script reads a file containing Base64 encoded PNG images,
// decodes the images, and saves them as individual PNG files in
// a directory . Then it converts images PDF format.

package main

import (
	"bufio"
	"encoding/base64"
	"fmt"
	"github.com/jung-kurt/gofpdf"
	"image"
	"image/jpeg"
	"image/png"
	"io"
	"os"
	"path/filepath"
	"strings"
)

func getImages(path string) ([]string, error) {
	var imgFiles []string
	files, err := os.ReadDir(path)
	if err != nil {
		return nil, err
	}

	for _, file := range files {
		ext := strings.ToLower(filepath.Ext(file.Name()))
		if ext == ".jpg" || ext == ".png" {
			imgFiles = append(imgFiles, filepath.Join(path, file.Name()))
		}
	}
	return imgFiles, nil
}

func getDimensions(imgPath string) (float64, float64) {
	file, err := os.Open(imgPath)
	if err != nil {
		return 0, 0
	}
	defer file.Close()

	image, _, err := image.DecodeConfig(file)
	if err != nil {
		return 0, 0
	}

	return float64(image.Width), float64(image.Height)
}

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
	imageFiles := make([]string, 0)

	for {
		line, err := reader.ReadString('\n')
		lineCounter++
		line = strings.TrimSpace(line)

		if len(line) > 0 {
			pngCheckStr := "data:image/png;base64,"
			jpegCheckStr := "data:image/jpeg;base64,"

			if len(line) > len(pngCheckStr) && line[:len(pngCheckStr)] == pngCheckStr {
				line = strings.TrimSpace(line[len(pngCheckStr):])

				imageData, _ := base64.StdEncoding.DecodeString(line)
				imageReader := strings.NewReader(string(imageData))
				pngImage, _ := png.Decode(imageReader)

				imagePath := filepath.Join(outputDir, fmt.Sprintf("%02d.png", lineCounter))
				imageFile, _ := os.Create(imagePath)
				defer imageFile.Close()
				png.Encode(imageFile, pngImage)

				imageFiles = append(imageFiles, imagePath)

			} else if len(line) > len(jpegCheckStr) && line[:len(jpegCheckStr)] == jpegCheckStr {
				line = strings.TrimSpace(line[len(jpegCheckStr):])

				imageData, _ := base64.StdEncoding.DecodeString(line)
				imageReader := strings.NewReader(string(imageData))
				jpegImage, _ := jpeg.Decode(imageReader)

				imagePath := filepath.Join(outputDir, fmt.Sprintf("%02d.jpg", lineCounter))
				imageFile, _ := os.Create(imagePath)
				defer imageFile.Close()
				jpeg.Encode(imageFile, jpegImage, nil)

				imageFiles = append(imageFiles, imagePath)

			} else {
				fmt.Printf("Invalid image data on line %d\n", lineCounter)
			}
		}

		if err == io.EOF {
			break
		}
	}

	pdf := gofpdf.New("P", "mm", "A4", "")

	for _, file := range imageFiles {
		pdf.AddPage()
		width, height := getDimensions(file)
		pdf.Rect(0, 0, width, height, "F")
		pdf.ImageOptions(file, 0, 0, 0, 0, false, gofpdf.ImageOptions{ReadDpi: true}, 0, "")
	}

	err = pdf.OutputFileAndClose(outputDir + ".pdf")
	fmt.Println("PDF generated successfully!")
}
