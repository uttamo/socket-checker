FROM python:3.8-slim

# Set working dir for the app
WORKDIR /usr/src/app

# Copy all the files to the container
COPY . .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# App will run on this port so publish this (command doesn't actually do anything)
EXPOSE 4045

# App will reload automatically if files are changed
CMD ["uvicorn", "api:app", "--reload", "--host", "0.0.0.0", "--port", "4045"]
