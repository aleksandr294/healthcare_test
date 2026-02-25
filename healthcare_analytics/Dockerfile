FROM healthcare-test-base:latest

WORKDIR /app/healthcare_analytics/

COPY . .

RUN poetry export --without-hashes -f requirements.txt --output requirements.txt \
    && pip install --no-cache-dir -r requirements.txt

ARG POSTGRES_URL
ARG SECRET_KEY

ENV POSTGRES_URL=$POSTGRES_URL
ENV SECRET_KEY=$SECRET_KEY

RUN chmod +x /app/healthcare_analytics/entrypoint.sh  && chown -R appuser:appuser /app

USER appuser

CMD /app/healthcare_analytics/entrypoint.sh