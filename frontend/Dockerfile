# frontend/Dockerfile
FROM node:22-alpine

WORKDIR /app

# Копируем package.json
COPY package*.json ./

# Устанавливаем зависимости с игнорированием peer-зависимостей
RUN npm install --legacy-peer-deps

# Копируем остальные файлы
COPY . .

EXPOSE 5173

CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0"]