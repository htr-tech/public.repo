// This script converts images in a specified folder to PDF

package main

import (
	"fmt"
	"github.com/jung-kurt/gofpdf"
	"image"
	"os"
	"path/filepath"
	"strings"
)

func getImages(path string) ([]string, error) {
	var imgFiles []string
	files, err := os.ReadDir(path)
	if err != nil {
		fmt.Println(err)
		os.Exit(1)
	}

	for _, file := range files {
		ext := strings.ToLower(filepath.Ext(file.Name()))
		// fmt.Println(file.Name())
		if ext == ".jpg" || ext == ".png" {
			imgFiles = append(imgFiles, filepath.Join(path, file.Name()))
		}
	}
	return imgFiles, nil
}

func getDimensions(imgPath string) (float64, float64) {
	file, err := os.Open(imgPath)
	defer file.Close()

	image, _, err := image.DecodeConfig(file)
	if err != nil {
		return 0, 0
	}

	return float64(image.Width), float64(image.Height)
}

func main() {
	var folderPath string
	if len(os.Args) > 1 {
		folderPath = os.Args[1]
	} else {
		fmt.Print("Enter folder name: ")
		fmt.Scanln(&folderPath)
	}

	pdf := gofpdf.New("P", "mm", "A4", "")
	imageFiles, _ := getImages(folderPath)

	for _, file := range imageFiles {
		pdf.AddPage()
		width, height := getDimensions(file)
		pdf.Rect(0, 0, width, height, "F")
		pdf.ImageOptions(file, 0, 0, 0, 0, false, gofpdf.ImageOptions{ReadDpi: true}, 0, "")

	}

	err := pdf.OutputFileAndClose(folderPath + ".pdf")
	if err != nil {
		fmt.Println("Error:", err)
		return
	}

	fmt.Println("PDF generated successfully!")
}
