# Where should I put .sh files?

It depends on who will use your script:

Only you - $HOME/.local/bin (As per the XDG Base Directory Specification)
You and other local users - /usr/local/bin
root only - /usr/local/sbin

ffmpeg -i video.mkv -vf "fps=1/10,scale=640:-1" -qscale:v 2 screenshots/screenshot\_%04d.png
ln -s /usr/local/bin/take_screenshots.sh take_screenshots.sh

# Move and unzip all

If you want to move all files from any subfolder, regardless of depth, into Folder A, use:

`find . -mindepth 2 -type f -exec mv -t . {} +`

If you also want to extract zip files from subfolders, you can use:

`find . -name '*.zip' -exec unzip {} \;`

# Merge PDFs and generate TOC from PDF files in a Directory

To generate a TOC (Table of Contents) of all folders and their files inside the current directory, you can use the following shell script command. This script will list the names of all subfolders and their corresponding files:

`for folder in */; do 
    echo "Folder: $folder" >> toc.txt; 
    find "$folder" -type f -exec basename {} \; >> toc.txt; 
    echo "" >> toc.txt; 
done`

Step 2: Convert Text to PDF
Convert the toc.txt file to a PDF using the pandoc tool (install if necessary with sudo apt install pandoc):

`pandoc toc.txt -o toc.pdf`

Step 3: Combine Folder Content into the PDF

`for folder in */; do
    for file in "$folder"/*; do
        cat "$file" >> combined_content.txt
    done
done`
`pandoc combined_content.txt -o combined_content.pdf`

Step 4: Merge TOC and File Content PDFs

`pdfunite toc.pdf combined_content.pdf final_output.pdf`
