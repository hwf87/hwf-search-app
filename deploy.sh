#!/bin/bash
pwd

set -a
source .env
set +a

cd ./app
uvicorn main:app --reload
