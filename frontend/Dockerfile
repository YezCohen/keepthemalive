# --- BUILD STAGE ---
# Use a Node.js image to build the React project
FROM node:20-alpine AS build

# Set the working directory inside the container
WORKDIR /app

# Copy dependency files and install them
COPY package.json ./
COPY package-lock.json ./
RUN npm install

# Copy all the React source code
COPY . .

# Run the build command, which creates the 'dist' folder
RUN npm run build

# --- SERVE STAGE ---
# Now use a tiny Nginx server image for the final container
FROM nginx:stable-alpine

# Copy the static files from the build stage into the Nginx web root folder
COPY --from=build /app/dist /usr/share/nginx/html

# Tell Docker that the container listens on port 80 (Nginx's default)
EXPOSE 80

# The command to start the Nginx server
CMD ["nginx", "-g", "daemon off;"]