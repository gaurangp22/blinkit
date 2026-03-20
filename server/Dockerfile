FROM node:18-alpine

WORKDIR /app

# Copy package.json to leverage docker caching
COPY package.json package-lock.json* ./
RUN npm install

# Copy source code
COPY . .

# Expose backend port
EXPOSE 8080

# Start server
CMD ["npm", "run", "start"]
