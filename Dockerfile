# 构建前端
FROM node:18-alpine as frontend-builder
WORKDIR /app/frontend
RUN npm install -g pnpm
COPY frontend/package.json frontend/pnpm-lock.yaml ./
RUN pnpm install --frozen-lockfile
COPY frontend .
RUN pnpm build

# 构建后端
FROM python:3.11-slim as backend-builder
WORKDIR /app/backend
RUN pip install poetry
COPY backend/pyproject.toml backend/poetry.lock ./
RUN poetry config virtualenvs.create false \
    && poetry install --no-dev --no-interaction --no-ansi
COPY backend .
COPY --from=frontend-builder /app/frontend/dist /app/backend/static

# 最终镜像
FROM python:3.11-slim
WORKDIR /app
COPY --from=backend-builder /app/backend .
COPY --from=backend-builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages

EXPOSE 8000
CMD ["python", "-m", "src.main"] 