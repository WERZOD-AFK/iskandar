# Bu Dockerfile ixtiyoriy — agar Vercel o'rniga Railway/boshqa hostda
# statik fayl sifatida serve qilmoqchi bo'lsangiz ishlatiladi.
FROM node:20-slim AS build
WORKDIR /app
COPY package.json ./
RUN npm install
COPY . .
RUN npm run build

FROM nginx:alpine
COPY --from=build /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf
EXPOSE 80
