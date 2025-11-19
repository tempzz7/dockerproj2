FROM alpine:3.19
RUN apk add --no-cache curl bash
WORKDIR /app
COPY curl-loop.sh ./
RUN chmod +x curl-loop.sh
CMD ["/bin/bash", "./curl-loop.sh"]
