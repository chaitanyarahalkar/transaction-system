<h1 align="center">Welcome to Transaction Management System 👋</h1>
<p>
  <img src="https://img.shields.io/badge/version-1.0.0-blue.svg?cacheSeconds=2592000" />
  <a href="https://github.com/kefranabg/readme-md-generator/graphs/commit-activity">
    <img alt="Maintenance" src="https://img.shields.io/badge/Maintained%3F-yes-green.svg" target="_blank" />
  </a>
  <a href="https://github.com/chaitanyarahalkar/transaction-system/blob/master/LICENSE">
    <img alt="License: MIT" src="https://img.shields.io/badge/License-MIT-yellow.svg" target="_blank" />
  </a>
  <a href="https://twitter.com/chairahalkar">
    <img alt="Twitter: chairahalkar" src="https://img.shields.io/twitter/follow/chairahalkar.svg?style=social" target="_blank" />
  </a>
</p>

> A payment system that can be integrated with E-Commerce site. Featured with a secured REST API to seamlessly use it. 

### 🏠 [Homepage](https://github.com/chaitanyarahalkar/transaction-system)

## Prerequisites


## Install

```sh
python install -r requirements.txt
```

## Configure the Settings

Setup SMTP Servers. By default the server is set to smtp.gmail.com. Add the environment variables EMAIL_HOST_USER, EMAIL_HOST_PASSWORD and SECRET_KEY to the .bashrc. Django uses a secret key (the SECRET_KEY environment variable) as a seed value to generate session identifiers. A secure random secret key can be generated using [this](https://djecrety.ir/). 
Set the environment variables by editing the .bashrc file on Linux / MacOS by running - 

```sh

echo "export SECRET_KEY=the_chosen_key" >> ~/.bashrc
echo "export EMAIL_HOST_USER=john.doe@example.com >> ~/.bashrc
echo "export EMAIL_HOST_PASSWORD=foobar" >> ~/.bashrc
```

If a Gmail account is to be used for sending transaction emails and OTP notifications, the less-secure-apps switch needs to be turned on for the account. This can be enabled [here](https://myaccount.google.com/lesssecureapps).

## Usage

```sh
python manage.py runserver
```

## Author

👤 **Chaitanya Rahalkar**

* Twitter: [@chairahalkar](https://twitter.com/chairahalkar)
* Github: [@chaitanyarahalkar](https://github.com/chaitanyarahalkar)

## 🤝 Contributing

Contributions, issues and feature requests are welcome!<br />Feel free to check [issues page](https://github.com/chaitanyarahalkar/transaction-system/issues).

## Show your support

Give a ⭐️ if this project helped you!

## 📝 License

Copyright © 2019 [Chaitanya Rahalkar](https://github.com/chaitanyarahalkar).<br />
This project is [MIT](https://github.com/chaitanyarahalkar/transaction-system/blob/master/LICENSE) licensed.

***
