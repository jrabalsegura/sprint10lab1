FROM python:3.8

# Establecer el directorio de trabajo en el contenedor
WORKDIR /app

# Copiar los requisitos y instalar las dependencias
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el resto de los archivos de la aplicación
COPY . .
RUN chmod +x manage.sh
# Exponer el puerto en el que la aplicación estará disponible
EXPOSE 5000

# Comando para ejecutar la aplicación
CMD ["./manage.sh"]

