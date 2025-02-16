#!/bin/bash

# Check if Homebrew is installed
if ! command -v brew &> /dev/null; then
    echo "Installing Homebrew..."
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
    
    # Add Homebrew to PATH for Apple Silicon
    echo 'eval "$(/opt/homebrew/bin/brew shellenv)"' >> ~/.zprofile
    eval "$(/opt/homebrew/bin/brew shellenv)"
fi

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo "Installing Node.js..."
    brew install node
fi

# Create project directory
PROJECT_DIR="simple-server"
mkdir -p $PROJECT_DIR
cd $PROJECT_DIR

# Initialize Node.js project if package.json doesn't exist
if [ ! -f "package.json" ]; then
    echo "Initializing Node.js project..."
    npm init -y
    
    # Install Express.js
    npm install express
fi

# Create server file if it doesn't exist
if [ ! -f "server.js" ]; then
    echo "Creating server file..."
    cat > server.js << 'EOL'
const express = require('express');
const app = express();
const port = 3000;

app.get('/', (req, res) => {
    res.send('<html><body style="background: white;"><h1>Server is running!</h1></body></html>');
});

app.listen(port, () => {
    console.log(`Server running at http://localhost:${port}`);
});
EOL
fi

# Start the server
echo "Starting server..."
node server.js
