<h1 align="center">SendIT</h1> 

## Table of Contents

- [Installation](##Installation)
- [Usage](##Usage)
- [Features](##Features)
- [Contributing](##Contributing)
- [Authors](##Authors)
- [License](#License)

## Introduction

SendIT is a courier service that helps users deliver parcels to different destinations. SendIT provides courier quotes based on weight categories.

## Tech Stack :poodle:

| Tool/Library                           | Version |
| -------------------------------------- | ------- |
| [Python](https://www.rust-lang.org/)   | 3.10    |
| [Flask](https://actix.rs/actix/actix/) | 3.0.3    |
| [Postgresql](https://www.arangodb.com/)| N/A   |


## Installation

1. Clone the repository:
```bash
 git clone https://github.com/Naomie-Jerutoe/SendIt_Backend
```

2. Change into the project directory.

```bash
cd SendIt_Backend
```
3. Install the required dependencies.

```bash
pipenv install && pipenv shell
```

## Usage

To run the project, use the following command:
```bash
python app.py
```
This will start the development server, and you can view the application in your browser at http://localhost:5000.

## Features

- * There are two types of users admin and regular user
- * Users can Register if they have no account or login otherwise
- * Users can create a new parcel delivery order by adding required fields
- * Users can change the destination of their parcels
- * Users can cancel a parcel delivery order
- * Users can see a list of delivery orders they have made if they have made any
- * Admin can change the status of a delivery order
- * Admin can change the location a parcel delivery order

## Contributing
We welcome contributions from the community! To contribute:

1. Fork the repository.
2. Create a new branch: `git checkout -b feature-name`.
3. Make your changes.
4. Push your branch: `git push origin feature-name`.
5. Create a pull request.

All commits must be descriptive, reviewed by two members and the project lead, and all feature branches are to be deleted once the pull request is accepted.

### Backend API
- [Backend API](https://sendit-backend-qhth.onrender.com)
- [Backend Git](https://github.com/Naomie-Jerutoe/SendIt_Backend)

### Frontend link
- [Frontend Git](https://github.com/Naomie-Jerutoe/SendIt_Frontend)

## Authors :black_nib:

- **Naomi Lagat**<[Naomi-Jerutoe](https://github.com/Naomie-Jerutoe)>
- **Levis Ngigi**<[LevisNgigi](https://github.com/LevisNgigi)>
- **Brian Mariga**<[Brian-Mariga](https://github.com/Brian-Mariga)>
- **Brian Kipkirui**<[bryon](https://github.com/bryokn)>
- **Emmanuel Kimwaki** <[ewkimwaki](https://github.com/ewkimwaki)>
- **Denis Rotich** <[Dennis-Rotich](https://github.com/Dennis-Rotich)>

# License

This project is licensed under the [MIT License](LICENSE)
