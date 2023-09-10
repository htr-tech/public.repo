// This script extracts image data from a website and saves it as a text file.
// Original source: https://github.com/zeltox/Google-Drive-PDF-Downloader

function dumpImageData() {
    let imageData = '';
    const imgTags = Array.from(document.getElementsByTagName('img'));
    const checkURLString = 'blob:' + window.location.protocol + "//" + window.location.host;

    for (let i = 0; i < imgTags.length; i++) {
        if (imgTags[i].src.startsWith(checkURLString)) {
            const img = imgTags[i];

            const canvas = document.createElement('canvas');
            const context = canvas.getContext('2d');
            canvas.width = img.naturalWidth;
            canvas.height = img.naturalHeight;
            context.drawImage(img, 0, 0, img.naturalWidth, img.naturalHeight);
            const imgDataURL = canvas.toDataURL();

            imageData += `${imgDataURL}\n`;
        }
    }

    const anchorElement = document.createElement('a');
    const file = new Blob([imageData], {
        type: 'text/plain'
    });

    const url = URL.createObjectURL(file);
    anchorElement.href = url;
    anchorElement.download = `${document.title}.txt`;
    document.body.appendChild(anchorElement);
    anchorElement.click();
}

const allElements = document.querySelectorAll('*');
let chosenElement;
let heightOfScrollableElement = 0;

for (let i = 0; i < allElements.length; i++) {
    if (allElements[i].scrollHeight >= allElements[i].clientHeight) {
        if (heightOfScrollableElement < allElements[i].scrollHeight) {
            heightOfScrollableElement = allElements[i].scrollHeight;
            chosenElement = allElements[i];
        }
    }
}

if (chosenElement.scrollHeight > chosenElement.clientHeight) {
    const scrollDistance = Math.round(chosenElement.clientHeight / 2);

    let loopCounter = 0;

    function myLoop(remainingHeightToScroll, scrollToLocation) {
        loopCounter++;
        console.log(loopCounter);
        setTimeout(() => {
            if (remainingHeightToScroll === 0) {
                scrollToLocation = scrollDistance;
                chosenElement.scrollTo(0, scrollToLocation);
                remainingHeightToScroll = chosenElement.scrollHeight - scrollDistance;
            } else {
                scrollToLocation += scrollDistance;
                chosenElement.scrollTo(0, scrollToLocation);
                remainingHeightToScroll -= scrollDistance;
            }

            if (remainingHeightToScroll >= chosenElement.clientHeight) {
                myLoop(remainingHeightToScroll, scrollToLocation);
            } else {
                setTimeout(() => {
                    dumpImageData();
                }, 500);
            }
        }, 400);
    }

    myLoop(0, 0);
} else {
    setTimeout(() => {
        dumpImageData();
    }, 500);
}
