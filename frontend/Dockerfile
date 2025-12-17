FROM node:20-alpine

WORKDIR /app

ENV VITE_API_URL=http://localhost:8000

COPY package.json package-lock.json ./
RUN npm install

COPY . .

RUN npm run build

EXPOSE 4173

CMD ["npm", "run", "preview", "--", "--host"]
