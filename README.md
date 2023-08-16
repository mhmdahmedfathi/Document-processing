# RDI
## Description

 Document processing: where data finds purpose.
 An API that is used for a document processing service. Users can upload images and PDF files to the API,
 and the API will perform some operations on the files and return the results.

## Table of Contents

- [Document processing](#book-author)
  - [Description](#description)
  - [Table of Contents](#table-of-contents)
  - [Installation](#installation)
  - [Models](#Models)
  - [Usage](#usage)
  - [License](#license)

## Installation

### If you wish to use your machine to run this application, you will need to install the following dependencies:

    \`\`\`
    
    pip install requirements.txt
    apt-get update && apt-get install -y libgdal-dev
    apt-get install poppler-utils
    pip install GDAL==3.2.2.1
    pip install numpy psycopg2-binary
    
    \`\`\`

    make sure to install django and django rest framework, and then run the following command:

    \`\`\`
    python manage.py runserver
    \`\`\`

### If you wish to use docker to run this application:

    make sure to install docker and docker compose, and then run the following command:

    \`\`\`
    docker compose up
    \`\`\`

    This will run the application on port 8000.

## Models 

- #### media (Base Class)

    - ##### Image 

    - ##### PDFS



## Usage

Users can upload images and PDF files to the API, and the API will perform some operations on the files 
and return the results.
## License

This project is licensed under the MIT license.




