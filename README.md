This is a Python script for web scraping that extracts contact information (email and phone numbers) from a list of websites provided in a text file named web_urls.txt. The script is multithreaded, making it suitable for processing a large number of websites concurrently.

## Prerequisites

Before running the script, make sure you have the following prerequisites installed:

    Python 3.x
    Required Python packages (install using pip install <package_name>):
        coloredlogs
        pandas
        beautifulsoup4
        requests
        openpyxl
        requests_random_user_agent
## Usage/Examples

```python
python main.py
```

Replace main.py with the actual name of the Python script.

The script will start processing the URLs in the web_urls.txt file concurrently, extracting email and phone number information. Progress and errors will be displayed in the terminal.

Once the scraping process is complete, the script will generate an Excel file named websites_info.xlsx containing the extracted contact information.
## Configuration

You can adjust the number of concurrent threads by modifying the num_threads variable in the main() function. Increasing the number of threads may improve performance but consume more system resources.
## Notes

This script uses multithreading to scrape multiple websites simultaneously. However, be aware that excessive concurrent requests may result in IP blocks or CAPTCHA challenges from websites.

The script is configured to ignore SSL certificate verification (via verify=False) when making HTTP requests. This is done to simplify the script but is not recommended for production use. Consider using a more secure approach in production environments.

The extracted contact information is saved in an Excel file named websites_info.xlsx. You can modify the output format or file name as needed in the main() function.
## Disclaimer

Use this script responsibly and ensure that you have the legal right to scrape the websites you target. Web scraping may be subject to legal restrictions and terms of service agreements of the websites being scraped. Be respectful of website owners' policies and guidelines.
