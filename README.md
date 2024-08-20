# Navya Assignment 📨

## Table of Content

- [Introduction](#introduction)
- [Project Structure](#project-structure)
    - [Template Structure](#template-structure)
- [How to Run](#how-to-run)
  - [Requirements](#requirements)
  - [Initial Setup](#initial-setup)
- [Developer Note](#developer-note)
- [API Documentation](#api-documentation)

# Introduction

Job assignment by Navya Advisor Ltd. Django API server.

# Project Structure

    |- .
        |- manage.py
        |- navya/
        |- core/
        |- auths/

## Template Structure

    |- .
        |- core/
            |- templates/

# How to Run
## Requirements
Docker-less Project Requrirement
- [python@3.11.9](https://www.python.org/downloads/release/python-3119/)

Dockered Requirement
- [Docker Desktop](https://www.docker.com/products/docker-desktop/)

    For MacOS
    - `brew install --cask docker`

## Initial Setup
    Without Docker
    - python3 -m venv venv
    - source ./venv/bin/activate
    - pip install -r requirements.txt
    - python manage.py makemigrations && python manage.py migrate
    - python manage.py collectstatic (Required due to xhtml2pdf)
    - python manage.py runserver
<br />
    
    With Docker
    
    Simple Setup
    - ./setup.sh

    Custom Setup
    - cp ./env_samples/env.txt ./.env
    - docker compose up -- build

# Developer Note
```
python manage.py collectstatic is required for APIs
    - /api/v1/pdf/transaction
    - /api/v1/pdf/transaction/:trans_id

This is due to working of xhtml2pdf library, used to generate pdf for these two APIs.
```
Issues is explained in detail at [`https://github.com/xhtml2pdf/xhtml2pdf/issues/548`](https://github.com/xhtml2pdf/xhtml2pdf/issues/548)

# API Documentation
Postman [Documentation](https://documenter.getpostman.com/view/8411525/2sA3sAgSfr)




