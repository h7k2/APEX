#!/bin/bash
python3 -m venv venv                                                                                                                       
source venv/bin/activate
cd /home/h7k2/APEX/apex-backend_2/apex-backend && uvicorn main:app --reload