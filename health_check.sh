#!/usr/bin/env bash
curl -sf http://localhost:3001/health && echo 'Backend healthy' || echo 'Backend down'
