CREATE TABLE IF NOT EXISTS processed_images (
    id SERIAL PRIMARY KEY,
    date_processed DATE NOT NULL,
    cloud_coverage FLOAT NOT NULL,
    image_path VARCHAR(255) NOT NULL UNIQUE,
    classification_result VARCHAR(255) NOT NULL,
    evaluation_metric FLOAT NOT NULL
);