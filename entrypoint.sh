#!/bin/bash

# Запуск приложения
uvicorn app.main:app --reload --host 0.0.0.0