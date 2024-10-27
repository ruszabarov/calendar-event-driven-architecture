FROM golang:1.23

WORKDIR /app

RUN curl -fLo install.sh https://raw.githubusercontent.com/cosmtrek/air/master/install.sh \
    && chmod +x install.sh && sh install.sh && cp ./bin/air /bin/air

COPY go.mod go.sum ./

RUN go mod download

COPY . .

EXPOSE 8080

CMD ["air", "-c", ".air.toml"]
