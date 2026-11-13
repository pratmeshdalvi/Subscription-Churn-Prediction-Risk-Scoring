--Task 1: Customer acquisition analysis
SELECT
    acquisition_channel,
    COUNT(*) AS total_customers
FROM customers
GROUP BY acquisition_channel
ORDER BY total_customers DESC;

--Task 2: Customer distribution by region
SELECT
    region,
    COUNT(*) AS total_customers
FROM customers
GROUP BY region
ORDER BY total_customers DESC;

--Task 3: Customer signup trends
SELECT
    DATE_TRUNC('month', signup_date)::DATE AS signup_month,
    COUNT(*) AS new_customers
FROM customers
GROUP BY signup_month
ORDER BY signup_month;

--Task 4: Customer age-group analysis
SELECT
    age_group,
    COUNT(*) AS customers
FROM customers
GROUP BY age_group
ORDER BY customers DESC;


