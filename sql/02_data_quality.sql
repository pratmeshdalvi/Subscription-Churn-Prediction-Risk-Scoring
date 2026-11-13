--Task 1: Check total records
SELECT
    (SELECT COUNT(*) FROM customers) AS customers,
    (SELECT COUNT(*) FROM subscriptions) AS subscriptions,
    (SELECT COUNT(*) FROM usage_activity) AS usage_records,
    (SELECT COUNT(*) FROM payments) AS payment_records,
    (SELECT COUNT(*) FROM support_tickets) AS support_records,
    (SELECT COUNT(*) FROM churn_events) AS churn_records;


--Task 2: Find duplicate customers
SELECT
    customer_id,
    COUNT(*) AS duplicate_count
FROM customers
GROUP BY customer_id
HAVING COUNT(*) > 1;

--Task 3: Find missing values
SELECT
    COUNT(*) FILTER (
        WHERE region IS NULL
    ) AS missing_region,

    COUNT(*) FILTER (
        WHERE acquisition_channel IS NULL
    ) AS missing_channel,

    COUNT(*) FILTER (
        WHERE signup_date IS NULL
    ) AS missing_signup_date

FROM customers;

--Task 4: Find invalid subscription values
SELECT *
FROM subscriptions
WHERE monthly_fee < 0
   OR discount_pct < 0
   OR discount_pct > 100
   OR start_date > end_date;

--Task 5: Find orphan customer IDs
SELECT p.*
FROM payments p
LEFT JOIN customers c
    ON p.customer_id = c.customer_id
WHERE c.customer_id IS NULL;

--Task 6: Identify unusual payment values
SELECT *
FROM payments
WHERE amount < 0
  




