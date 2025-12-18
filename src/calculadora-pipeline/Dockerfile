# Usamos una imagen ligera de Node.js
FROM node:18-slim

# Directorio de trabajo
WORKDIR /app

# Copiar archivos de dependencias
COPY package*.json ./

# Instalar solo dependencias de producción
RUN npm install --only=production

# Copiar el resto del código
COPY . .

# Exponer el puerto (Render usa la variable PORT)
EXPOSE 3000

# Comando para iniciar la aplicación
CMD ["node", "src/app.js"]