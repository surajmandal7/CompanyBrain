FROM node:20-bookworm-slim AS frontend-build
WORKDIR /app
COPY package.json pnpm-lock.yaml* ./
RUN npm install --global pnpm@10.15.0 && pnpm install --frozen-lockfile
COPY frontend ./frontend
COPY vite.config.ts tsconfig.json ./
RUN pnpm build

FROM python:3.12-slim
WORKDIR /app
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1 PORT=3000
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY server ./server
COPY --from=frontend-build /app/frontend/dist ./frontend/dist
COPY public ./public
COPY .env.example ./
EXPOSE 3000
CMD ["sh", "-c", "uvicorn server.main:app --host 0.0.0.0 --port ${PORT:-3000}"]
