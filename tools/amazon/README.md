# Web Bargins Ltd SP-API Wrapper

## Description

This repository contains a Python script that is used as a wrapper for the Amazon Selling Partner API (SP-API). This has been developed to automate the eCommerce operations for Web Bargins Ltd, providing a quick and efficient way to request reports regarding sales, inventory, and various other aspects of the business.

This library provides a set of tools for use and to be intergrated into wider applications. 

## Key Features

- \'inventory_report.py\' - Retrieves comprehensive reports on inventory.
- \'sales_report.py\' - Generates sales reports.
- Automates various aspects of the eCommerce operations.
- Utilizes Amazon SP-API for reliable data.

## Installation

Clone this repository using git:

\`\`\`
git clone https://github.com/teknetik/documentation-helper
cd documentation-helper
\`\`\`

It is recommended to create a virtual environment to isolate package dependencies locally and install project dependencies:

\`\`\`
pipenv install
pipenv shell
\`\`\`

## Usage

Make sure to add your SP-API credentials to the `keys.py` file:

\`\`\`python
REFRESH_TOKEN='XXXXXXX'
LWA_APP_ID='XXXXXXX'
LWA_CLIENT_SECRET='XXXXXXX'
AWS_SECRET_KEY='XXXXXXX'
AWS_ACCESS_KEY='XXXXXXX'
ROLE_ARN='arn:aws:iam::XXXXXXX:role/XXXXXXX'
DB_USER = "postgres"
DB_PASSWORD = "XXXXXXX"
\`\`\`

Once done, you can run the script:

\`\`\`bash
docker-compose up -d
\`\`\`

Provides a containerized environment for the applications supporting dependancies such as PosgreSQL. \'dbOps.py\' is used to initialize the database.

## Contribution

Contributions, issues, and feature requests are welcome. Feel free to check [issues page](http://github.com/yourusername/WebBarginsLtd_SP-API_Wrapper/issues) if you want to contribute.

## License

This project is licensed under the terms of the MIT license. See [LICENSE](LICENSE) for additional details.

## Contact

[Your Name] - your.email@example.com

Project Link: [Web Bargins Ltd SP-API Wrapper](https://github.com/yourusername/WebBarginsLtd_SP-API_Wrapper)


## Credits and thanks

Made possible by the wonderful tutorials from Deltalogic

https://www.deltalogic.com

https://github.com/jakobowsky?tab=repositories
