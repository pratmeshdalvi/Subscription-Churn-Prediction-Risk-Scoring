
--Task 1: Payment success and failure
SELECT
    payment_status,
    COUNT(*) AS total_payments
FROM payments
GROUP BY payment_status;

--Task 2: Payment failure rate
SELECT
    ROUND(
        100.0 *
        COUNT(*) FILTER (
            WHERE payment_status = 'Failed'
        ) / NULLIF(COUNT(*), 0),
        2
    ) AS payment_failure_percentage
FROM payments;


--Task 3: Failed payments by payment method
SELECT
    payment_method,
    COUNT(*) FILTER (
        WHERE payment_status = 'Failed'
    ) AS failed_payments,
    COUNT(*) AS total_payments
FROM payments
GROUP BY payment_method;

--Task 4: Customers with multiple payment failures
SELECT
    customer_id,
    COUNT(*) AS failed_payment_count
FROM payments
WHERE payment_status = 'Failed'
GROUP BY customer_id
HAVING COUNT(*) >= 2
ORDER BY failed_payment_count DESC;
