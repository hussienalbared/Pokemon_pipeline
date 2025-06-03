# Step 1: Build the app
FROM node:latest AS builder

WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .

# Build both browser and server
RUN npm run build

# Step 2: Run SSR server
FROM node:latest AS runner

WORKDIR /app
COPY --from=builder /app/dist /app/dist
COPY --from=builder /app/node_modules /app/node_modules
COPY --from=builder /app/package.json /app/

EXPOSE 4000
CMD ["node", "dist/frontend/server/server.mjs"]
