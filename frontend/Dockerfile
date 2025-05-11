# 1) build stage
FROM node:18-alpine AS builder
WORKDIR /app

# install deps
COPY package.json package-lock.json ./
RUN npm ci

# copy code, including tailwind & Vite config
COPY . .

# you can optionally run a production build here:
# RUN npm run build

# 2) dev stage
FROM node:18-alpine
WORKDIR /app

COPY --from=builder /app /app

EXPOSE 5173

# start Vite dev server (with Tailwind + HMR)
CMD ["npm", "run", "dev"]
