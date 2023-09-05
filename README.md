```markdown
# Restaurant API Project

This repository contains a Django Rest Framework (DRF)
based project that simulates a restaurant's delivery network.
The project is designed to manage various aspects of a restaurant's operations
, including customer orders, delivery crew, and manager functionalities.

## Table of Contents

- [Features](#features)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Usage](#usage)
- [API Endpoints](#api-endpoints)
- [License](#license)

## Features

- **Customer Management**: Create, update, and manage customer accounts.
- **Order Placement**: Customers can place food orders from the restaurant's menu.
- **Delivery Crew Management**: Add and manage delivery crew members.
- **Order Assignment**: Assign delivery orders to the available delivery crew.
- **Manager Dashboard**: Managers can monitor and control the overall operations.

## Prerequisites

Before you begin, ensure you have met the following requirements:

- **Pip**: Ensure that `pip` is installed and its location is added to your system's PATH.

- **Python**: Install Python (>= 3.7) on your system.

## Installation

1. Clone this repository:

   ```shell
   git clone https://github.com/hanifidemir5/Restoran-Api-Project.git
   ```

2. Navigate to the project directory:

   ```shell
   cd Restoran-Api-Project
   ```

3. Create a virtual environment (optional but recommended):

   ```shell
   python -m venv venv
   ```

4. Activate the virtual environment:

   - On Windows:

     ```shell
     venv\Scripts\activate
     ```

   - On macOS and Linux:

     ```shell
     source venv/bin/activate
     ```

5. Install Django and other required packages:

   ```shell
   pip install django
   pip install djangorestframework
   pip install djangorestframework-xml
   pip install djoser
   ```
  - "pip install django" for using python-django framework
  - "pip install  djangorestframework" for using django-restframework,
  - "pip install djangorestframework-xml" to make django rest framework support xml files
  - "pip install djoser" djoser provides basic login and logout pages.
  
## Usage

1. Start the Django development server:

   ```shell
   python manage.py runserver
   ```

2. Access the API in your web browser or use a tool like [Postman](https://www.postman.com/) to interact with the API endpoints.


## API Endpoints

Here are the main API endpoints and their descriptions:

- `/api-auth/`: Authentication-related endpoints provided by Django Rest Framework.

- `/`: Authentication-related endpoints provided by Djoser.

- `/menu-items/`: Handles menu items.

- `/menu-items/<int:pk>`: Handles a single menu item by its primary key.

- `/categories/`: Handles categories.

- `/categories/<int:pk>`: Handles a single category by its primary key.

- `/groups/manager/users`: Handles manager users in the "manager" group.

- `/groups/manager/users/<int:pk>`: Handles a single manager user in the "manager" group by its primary key.

- `/groups/delivery-crew/users`: Handles delivery crew users in the "delivery-crew" group.

- `/groups/delivery-crew/users/<int:pk>`: Handles a single delivery crew user in the "delivery-crew" group by its primary key.

- `/cart/menu-items`: Handles cart items related to menu items.

- `/orders`: Handles orders.

- `/orders/<int:pk>`: Handles updating an order by its primary key.

- `/djoser/`: Authentication token-related endpoints provided by Djoser.

## You can see these url patterns in urls.py file mostly on LittleLemonAPI app section.

## License

This project is licensed under the [MIT License](LICENSE).
```
