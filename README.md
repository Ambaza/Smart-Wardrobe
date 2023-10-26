# Smart Wardrobe

The Smart Wardrobe is a Python application that allows you to manage your wardrobe by importing images of clothing items and exploring your wardrobe collection. It uses a MySQL database to store the information about your clothing items.

## Features

- **Import Image:** Add a new clothing item to your wardrobe by providing a name, selecting the type of clothing (e.g., top, bottom, dress), and importing an image of the item.

- **Explore Photo:** Browse through your wardrobe collection, view the clothing items, and navigate between them.

- **Special Function:** This section can be used to extend your application with custom functionality or features.

## Prerequisites

Before using the Smart Wardrobe application, ensure you have the following dependencies:

- Python 3.x
- PyQt5
- MySQL Connector/Python

You also need to configure a MySQL database with the following details:

- **User:** Your MySQL username
- **Password:** Your MySQL password
- **Host:** MySQL server address (default: localhost)
- **Database:** The name of the wardrobe database

## Installation

1. Install the required Python packages if you haven't already:

   ```bash
   pip install PyQt5 mysql-connector-python
   ```

2. Set up your MySQL database with the name "wardrobe" and create tables for clothing items (e.g., "bottom," "dress," "top"). Update the database configuration in the code with your MySQL credentials.

## Usage

1. Run the application by executing the following command:

   ```bash
   python smart_wardrobe.py
   ```

2. Once the application is running, you can start using the features described above.

## How to Use

### Import Image

1. Click the "Import Image" button to open the import window.
2. Enter the name of the clothing item.
3. Choose the type of clothing (e.g., top, bottom, dress) from the dropdown menu.
4. Click the "Select Image" button to choose an image file of the clothing item.
5. Click the "Import" button to add the clothing item to your wardrobe.

### Explore Photo

1. Click the "Explore Photo" button to open the explore window.
2. Choose the clothing type from the dropdown to filter your clothing items.
3. Use the "Next" button to browse through your wardrobe collection.

### Special Function

This section can be used to implement custom functionality or features tailored to your specific needs.

## Known Issues

- Currently, there are no known issues.

## Author

- Your Name

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

Feel free to modify and extend this application according to your requirements. It serves as a foundation for managing your wardrobe, and you can enhance it with additional features as needed.
